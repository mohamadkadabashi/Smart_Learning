<template>
  <div v-if="test" class="d-flex">
    <div class="container w-75 d-flex flex-column" style="min-height: 90vh">
      <div style="flex: 1">

        <!-- test information -->
        <div class="d-flex justify-content-between">
          <div>
            <h2>{{ test.title }}</h2>
            <p class="primary-text">
              {{ getTitleFromXml(currentItem.xml) }}
            </p>
          </div>

          <p v-if="!isReviewMode" class="secondary-text my-3">
            {{ currentIndex }} von {{ testItems.length }} abgeschlossen
          </p>
          <p v-else class="secondary-text my-3">
            {{ currentIndex + 1 }} / {{ testItems.length }}
          </p>
        </div>

        <!-- QTI3 player -->
        <div class="my-5 player-wrapper">
          <Qti3Player ref="qti3player"
                      @notifyQti3PlayerReady="onPlayerReady"
                      @notifyQti3SuspendAttemptCompleted="onItemSaved"
                      @notifyQti3EndAttemptCompleted="onItemSaved"
                      @notifyQti3ScoreAttemptCompleted="onItemSaved" />
        </div>

        <!-- correct answer -->
        <div v-if="isReviewMode && isTextEntry && !isCorrect(currentIndex)" class="my-4">
          <label class="primary-text">
            <span class="fw-normal">Richtige Antwort:</span>
            <span class="text-danger">
              {{ getCorrectAnswer(currentItem.guid) }}
            </span>
          </label>
        </div>
      </div>
      <!-- navigation -->
      <div class="nav-btn-container w-100">
        <div class="d-flex gap-3 my-2 justify-content-between">
          <div class="d-flex gap-2">
            <button class="primary"
                    @click="prev"
                    :disabled="!qti3player || currentIndex === 0">
              Zurück
            </button>

            <button v-if="currentIndex < testItems.length - 1"
                    class="primary"
                    @click="next"
                    :disabled="!qti3player">
              Weiter
            </button>
            <button v-else-if="!isReviewMode"
                    class="primary"
                    @click="submitTest"
                    :disabled="!qti3player">
              Überprüfen
            </button>
            <button v-else
                    class="primary"
                    @click="navigateToHome">
              Zur Startseite
            </button>

          </div>

          <div>
	          <button class="secondary">
		          Fortschritt speichern
	          </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Qti3Player from 'qti3-item-player'
import 'qti3-item-player/dist/qti3Player.css'
import '@/../public/assets/css/styles.css'

export default {
  name: 'Test',
  components: { Qti3Player },
  data() {
    return {
      qti3player: null,
      test: null,
      testItems: [],
      itemStates: new Map(),
      currentIndex: 0,
      isReviewMode: false,
      itemsLoaded: false,
      playerReady: false
    }
  },
  computed: {
    currentItem() {
      return this.testItems[this.currentIndex] || {};
    },
    currentState() {
      return this.itemStates.get(this.currentItem.guid) || null;
    },
    isTextEntry() {
      return this.getItemType() === 'textEntry';
    }
  },
  methods: {
    async loadTest(id) {
      this.test = this.$testService.getTestById(id)
      this.testItems = await this.$testService.loadQuestionItems(this.test.items);
      this.itemsLoaded = true;
      this.tryLoadItem();
    },
    onPlayerReady(player) {
      this.qti3player = player;
      this.playerReady = true;
      this.tryLoadItem();
    },
    tryLoadItem() {
      if (!this.playerReady || !this.itemsLoaded) return;
      this.loadCurrentItem();
    },
    loadCurrentItem() {
      const item = this.currentItem;
      if (!item.guid || !this.qti3player) return;

      const config = {
        guid: item.guid,
        status: this.isReviewMode ? 'review' : 'interacting',
        ...(this.currentState && { state: this.currentState })
      };

      this.qti3player.loadItemFromXml(item.xml, config);

      this.colorizeAnswers();
      // KaTeX Rendern aufrufen
      this.renderMath();
    },

    next() {
      if (this.currentIndex < this.testItems.length - 1) {
        this.qti3player.suspendAttempt('next');
      }
    },
    prev() {
      if (this.currentIndex > 0) {
        this.qti3player.suspendAttempt('prev');
      }
    },
    submitTest() {
      this.qti3player.suspendAttempt('end');
    },

    onItemSaved(data) {
      this.itemStates.set(data.state.guid, data.state);

      switch (data.target) {
        case 'next':
          this.currentIndex++;
          this.loadCurrentItem();
          break;
        case 'prev':
          this.currentIndex--;
          this.loadCurrentItem();
          break;
        case 'end':
          this.isReviewMode = true;
          this.currentIndex = 0;
          this.loadCurrentItem();
          break;
      }
    },

    // Prüft, ob Antwort richtig war
    isCorrect(idx) {
    const item  = this.testItems[idx];
    const state = this.itemStates.get(item.guid);
    if (!state) return false;

    // responseVariable zur RESPONSE
    const rv = state.responseVariables.find(v => v.identifier === 'RESPONSE');
    if (!rv) return false;

    const actual  = rv.value;           // kann String oder Array sein
    const correct = rv.correctResponse; // kann String oder Array sein

    // Multiple Choice?
    if (Array.isArray(correct)) {
      // actual muss auch Array sein
      if (!Array.isArray(actual)) return false;
      // Längen gleich?
      if (correct.length !== actual.length) return false;
      // jede korrekte ID muss im actual-Array vorkommen
      return correct.every(id => actual.includes(id));
    }

    // Single Choice: einfacher Vergleich
    return actual === correct;
  },

    getTitleFromXml(xmlString) {
      const parser = new DOMParser();
      const doc    = parser.parseFromString(xmlString, 'text/xml');
      return doc.querySelector('qti-assessment-item')?.getAttribute('title') || '';
    },
    getResponseValue(state) {
      return state.responseVariables.find(v => v.identifier === 'RESPONSE')?.value;
    },
    getCorrectAnswer(guid) {
    // 1) correctResponse aus dem State
    const state = this.itemStates.get(guid);
    const respVar = state
      ?.responseVariables
      .find(v => v.identifier === 'RESPONSE');
    if (!respVar || respVar.correctResponse == null) {
      return null;
    }

    // sorgen, dass wir immer mit einem Array weiterarbeiten
    const ids = Array.isArray(respVar.correctResponse)
      ? respVar.correctResponse
      : [respVar.correctResponse];

    // 2) XML parsen
    const item = this.testItems.find(i => i.guid === guid);
    if (!item?.xml) {
      // kein XML? dann gib die rohen IDs zurück
      return Array.isArray(respVar.correctResponse)
        ? [...ids]
        : ids[0];
    }
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(item.xml, 'text/xml');

    // 3) für jede ID den Text ermitteln
    const texts = ids.map(id => {
      const choice = xmlDoc.querySelector(`qti-simple-choice[identifier="${id}"]`);
      return choice
        ? choice.textContent.trim()
        : id;  // Fallback auf die ID
    });

    // Single vs. Multiple
    return Array.isArray(respVar.correctResponse)
      ? texts
      : texts[0];
  },

  // KaTeX Rendern
renderMath() {
      this.$nextTick(() => {
        
        if (window.renderMathInElement) {
          window.renderMathInElement(this.$el, {
            delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false},
              {left: '\\(', right: '\\)', display: false},
              {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
          });
        }
      });
    },

    getItemType() {
      if (!this.currentItem?.xml) return null;

      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(this.currentItem.xml, 'text/xml');

      if (xmlDoc.querySelector('qti-text-entry-interaction')) return 'textEntry';
      if (xmlDoc.querySelector('qti-choice-interaction')) return 'choice';

      return 'unknown';
    },

    navigateToHome() {
      this.$router.push({ name: 'Home' });
    },

    colorizeAnswers() {
      if (!this.isReviewMode) return;

      this.$nextTick(() => {
        const state = this.itemStates.get(this.currentItem.guid);
        if (!state) return;

        const rv = state.responseVariables.find(v => v.identifier === 'RESPONSE');
        if (!rv) return;

        const correct = Array.isArray(rv.correctResponse)
          ? rv.correctResponse
          : [rv.correctResponse];

        const actual = Array.isArray(rv.value)
          ? rv.value
          : [rv.value];

        if (this.isTextEntry) {
          const input = this.$el.querySelector('.text-entry-default-label');
          if (!input) return;

          input.classList.remove('choice-correct', 'choice-wrong');
          input.classList.add(
            this.isCorrect(this.currentIndex)
              ? 'choice-correct'
              : 'choice-wrong'
          );
          console.log("text");
          return;
        }

        const choices = this.$el.querySelectorAll('[data-identifier]');
        choices.forEach(choice => {
          const id = choice.getAttribute('data-identifier');

          choice.classList.remove('choice-correct', 'choice-wrong', 'choice-missed');

          if (correct.includes(id)) {
            choice.classList.add('choice-correct');
          }

          if (actual.includes(id) && !correct.includes(id)) {
            choice.classList.add('choice-wrong');
          }

          if (!actual.includes(id) && correct.includes(id)) {
            choice.classList.add('choice-missed');
          }
        });
      });
    }
  },
  created() {
    //
  },
  mounted() {
    this.loadTest(this.$route.params.id);
  }
}
</script>

<style scoped>
.container {
  padding-bottom: 4rem;
  padding-top: 4rem;
}

@media (max-width: 550px) {
  .nav-btn-container > div {
    flex-direction: column;
  }
}
</style>
