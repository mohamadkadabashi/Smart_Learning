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
          <Qti3Player ref="qti3player" @notifyQti3PlayerReady="onPlayerReady"
            @notifyQti3SuspendAttemptCompleted="onItemSaved" @notifyQti3EndAttemptCompleted="onItemSaved"
            @notifyQti3ScoreAttemptCompleted="onItemSaved" />
        </div>

        <!-- correct answer -->
        <div v-if="isReviewMode && !isCorrect(currentIndex)" class="my-4">
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
            <button class="primary" @click="prev" :disabled="!qti3player || currentIndex === 0">
              Zurück
            </button>

            <button v-if="currentIndex < testItems.length - 1" class="primary" @click="next" :disabled="!qti3player">
              Weiter
            </button>
            <button v-else-if="!isReviewMode" class="primary" @click="submitTest" :disabled="!qti3player">
              Überprüfen
            </button>
            <button v-else class="primary" @click="navigateToHome">
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
import { getTestById } from "@/services/subjectTest";
import { startAttempt, finishAttempt } from "@/services/attempts";


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
      playerReady: false,
      attemptId: null,
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

  async mounted() {
    await this.loadTest(this.$route.params.id);
  },

  methods: {
    async loadTest(id) {
      const testId = Number(id);

      // 1) Test laden
      const st = await getTestById(testId);

      // ✅ wichtig, sonst v-if="test" bleibt false
      this.test = {
        title: st.test_name ?? st.name ?? `Test ${st.id}`,
      };

      // 2) Attempt starten oder resume (wenn du Backend auf start-or-resume geändert hast)
      const attempt = await startAttempt({ subject_test_id: testId });
      this.attemptId = attempt.id;

      // 3) Falls Test noch generiert wird
      if (!st.test) {
        this.testItems = [];
        this.itemsLoaded = true;
        return;
      }

      // Minimal: ein Item aus XML
      this.testItems = [{
        guid: `st-${st.id}`,
        xml: st.test
      }];

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

async onItemSaved(data) {
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

        // ✅ Hier finish callen
        if (this.attemptId) {
          const { correct, total } = this.computeScoreFromStates();

          try {
            await finishAttempt(this.attemptId, {
              correct_answered: correct,
              total_questions: total
              // finished_at optional
            });
          } catch (e) {
            console.error("finishAttempt failed:", e);
          }
        }
        break;
    }
  },
  computeScoreFromStates() {
    let total = this.testItems.length;
    let correct = 0;

    for (const item of this.testItems) {
      const state = this.itemStates.get(item.guid);
      if (!state) continue;

      const responseId = this.getResponseIdentifier(item.xml);
      const rv = state.responseVariables?.find(v => v.identifier === responseId);
      if (!rv) continue;

      const actual = rv.value;
      const expected = rv.correctResponse;

      if (Array.isArray(expected)) {
        if (Array.isArray(actual) &&
            expected.length === actual.length &&
            expected.every(id => actual.includes(id))) {
          correct++;
        }
      } else {
        if (actual && expected &&
            String(actual).toLowerCase() === String(expected).toLowerCase()) {
          correct++;
        }
      }
    }

    return { correct, total };
  },

  getResponseIdentifier(xmlString) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(xmlString, 'text/xml');

      // meistens ist es RESPONSE_1, RESPONSE_2, ...
      const decl = doc.querySelector('qti-response-declaration');
      return decl?.getAttribute('identifier') || 'RESPONSE_1';
  },
  isCorrect(idx) {
    const item = this.testItems[idx];
    const state = this.itemStates.get(item.guid);
    if (!state) return false;

    const responseId = this.getResponseIdentifier(item.xml);
    const rv = state.responseVariables.find(v => v.identifier === responseId);
    if (!rv) return false;

    const actual = rv.value;
    const correct = rv.correctResponse;

    if (Array.isArray(correct)) {
      if (!Array.isArray(actual)) return false;
      if (correct.length !== actual.length) return false;
      return correct.every(id => actual.includes(id));
    }

    if (!actual) return false;
    return String(actual).toLowerCase() === String(correct).toLowerCase();
  },


    getTitleFromXml(xmlString) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(xmlString, 'text/xml');
      return doc.querySelector('qti-assessment-item')?.getAttribute('title') || '';
    },
    getResponseValue(state) {
      return state.responseVariables.find(v => v.identifier === 'RESPONSE')?.value;
    },
    getCorrectAnswer(guid) {
      const item = this.testItems.find(i => i.guid === guid);
      if (!item?.xml) return null;

      const state = this.itemStates.get(guid);
      if (!state) return null;

      const responseId = this.getResponseIdentifier(item.xml);
      const respVar = state.responseVariables.find(v => v.identifier === responseId);
      if (!respVar || respVar.correctResponse == null) return null;

      const ids = Array.isArray(respVar.correctResponse)
        ? respVar.correctResponse
        : [respVar.correctResponse];

      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(item.xml, 'text/xml');

      const texts = ids.map(id => {
        const choice = xmlDoc.querySelector(`qti-simple-choice[identifier="${id}"]`);
        return choice ? choice.textContent.trim() : id;
      });

      return Array.isArray(respVar.correctResponse) ? texts : texts[0];
    },
    // KaTeX Rendern
    renderMath() {
      this.$nextTick(() => {

        if (window.renderMathInElement) {
          window.renderMathInElement(this.$el, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false },
              { left: '\\(', right: '\\)', display: false },
              { left: '\\[', right: '\\]', display: true }
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
        // text entry
        if (this.isTextEntry) {
          const input = this.$el.querySelector('.text-entry-default-label');
          if (!input) return;

          input.classList.remove('choice-correct', 'choice-wrong');
          input.classList.add(
            this.isCorrect(this.currentIndex)
              ? 'choice-correct'
              : 'choice-wrong'
          );
          return;
        }

        // single/multiple choice
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
}
</script>

<style scoped>
.container {
  padding-bottom: 4rem;
  padding-top: 4rem;
}

@media (max-width: 550px) {
  .nav-btn-container>div {
    flex-direction: column;
  }
}
</style>
