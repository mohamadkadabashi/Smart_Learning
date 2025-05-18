<template>
  <div>
    <TopBar />

    <div class="container py-5 d-flex justify-content-center">
      <div class="w-100" style="max-width: 700px;">
        <h1 class="text-center mb-4" style="padding-top: 50px;">
          {{ test.title }}
        </h1>

        <div v-if="!isReviewMode">
          <!-- Progress Bar (außerhalb der Karte) -->
          <div class="d-flex justify-content-center gap-2 mb-4">
            <button
              v-for="(item, i) in testItems"
              :key="item.identifier"
              class="btn btn-outline-secondary rounded-circle"
              :class="{ 'btn-primary': i === currentIndex }"
              style="width: 40px; height: 40px;"
              disabled
            >
              {{ i + 1 }}
            </button>
          </div>

          <!-- Karte mit Player und Navigation -->
          <div class="card mb-5 p-4 border rounded item-player-card">
            <!-- Question Title -->
            <h2 class="text-center text-uppercase mb-3">
              {{ getTitleFromXml(TC.getItemAtIndex(currentIndex).xml) }}
            </h2>

            <!-- QTI3 Player -->
            <div class="player-wrapper mb-4">
              <Qti3Player
                ref="qti3player"
                @notifyQti3PlayerReady="onPlayerReady"
                @notifyQti3SuspendAttemptCompleted="onItemSaved"
                @notifyQti3EndAttemptCompleted="onItemSaved"
                @notifyQti3ScoreAttemptCompleted="onItemSaved"
              />
            </div>

            <!-- Navigation -->
            <div class="d-flex justify-content-center gap-3 mt-2">
              <button class="btn btn-secondary" @click="prev" :disabled="currentIndex === 0">
                Previous
              </button>
              <button
                v-if="currentIndex < testItems.length - 1"
                class="btn btn-primary"
                @click="next"
                :disabled="!qti3player"
              >
                Next
              </button>
              <button v-else class="btn btn-danger" @click="submitTest" :disabled="!qti3player">
                Submit
              </button>
            </div>
          </div>
        </div>

        <!-- Review Modus -->
        <div v-if="isReviewMode">
          <h2 class="text-center mb-4">Auswertung</h2>
          <div
            v-for="testItem in testItems"
            :key="testItem.guid"
            class="item-player-card mb-5 p-4 border rounded"
          >
            <h2 class="text-center text-uppercase mb-3">
              {{ getTitleFromXml(testItem.xml) }}
            </h2>
            <div class="player-wrapper mb-3">
              <Qti3Player
                :key="`qti-player-container-${testItem.guid}`"
                @notifyQti3PlayerReady="player => onReviewPlayerReady(player, testItem)"
              />
            </div>
            <div>
              <strong>Correct Answer:</strong>
              <span
                :class="{
                  'text-success': getResponseValue(itemStates.get(testItem.guid)) === getCorrectAnswer(testItem.guid),
                  'text-danger': getResponseValue(itemStates.get(testItem.guid)) !== getCorrectAnswer(testItem.guid)
                }"
              >
                {{ getCorrectAnswer(testItem.guid) }}
              </span>
            </div>
          </div>
          <div class="mt-4">
            <router-link
              :to="{ name: 'Home' }"
              class="btn btn-primary"
            >
              Zurück zur Startseite
            </router-link>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>


<script>
import Qti3Player from 'qti3-item-player'
import 'qti3-item-player/dist/qti3Player.css'
import { TestControllerUtilities } from '@/helpers/TestControllerUtilities'
import TopBar from '@/components/TopBar.vue';

export default {
  name: 'Test',
  components: { Qti3Player, TopBar },
  data() {
    return {
      //TC = TestControllerUtilities, saves item states and handles items (questions
      TC: null,
      qti3player: null,
      testItems: [],
      currentIndex: 0,
      test: null,
      itemStates: new Map(),
      isReviewMode: false,

      itemsLoaded: false,
      playerReady: false
    }
  },
  methods: {
    //called through mounted() when DOM ready
    //calls TestController to retrieve test item by id
    //then TestController calls ItemFactory and loads items.
    async loadTest(id) {
      this.test = this.TC.getTestById(id)
      if (!this.test) return

      await this.TC.loadItems(this.test.items)
      this.testItems = this.TC.getItems()
      //this.loadCurrentItem()

      this.itemsLoaded = true
      this.tryLoadItem()

    },
    //event handler, called upon loading qti3player
    onPlayerReady(player) {
      this.qti3player = player
      //this.loadCurrentItem()

      this.playerReady = true
      this.$nextTick(() => this.tryLoadItem());   
    },

    //makes sure that items and itemPlayer is ready before items are loaded into player
    tryLoadItem() {
      if (this.playerReady && this.itemsLoaded) {
        this.loadCurrentItem();
      }
    },

    //loads the item at the current index
    //checks if question already answered and loads save itemState into item player
    //calls qti3player.loadItemFromXML
    loadCurrentItem() {
      const item = this.TC.getItemAtIndex(this.currentIndex)
      if (!item || !this.qti3player) return

      const config = {
        guid: item.guid,
        status: 'interacting'
        // Possible status values for QTI3 Item Player:
        //
        // 'initial'
        //   → The item is freshly loaded, no interaction has started
        //
        // 'interacting'
        //   → Normal mode – candidate can interact with the item (e.g., during the test)
        //
        // 'closed'
        //   → The item has been submitted/completed – no further interaction allowed
        //
        // 'review'
        //   → Read-only mode, used to review answers after the test (answers visible, not editable)
        //
        // 'solution'
        //   → The item displays correct answers or solution paths (e.g., during feedback phase)
      }

      //check if question already answered -> if yes: add it to config
      if (this.itemStates.has(item.guid)) {
        config.state = this.itemStates.get(item.guid)
      }

      this.qti3player.loadItemFromXml(item.xml, config)
    },


    //called upon press of NEXT button
    next() {
      if (this.currentIndex < this.testItems.length - 1) {
        this.qti3player.suspendAttempt('next')
      }
    },

    //called upon press of prev button
    prev() {
      if (this.currentIndex > 0) {
        this.qti3player.suspendAttempt('prev')
      }
    },

    //called upon press of SUBMIT button
    submitTest() {
      console.log("[SAVED ITEM STATES:]")
      const obj = Object.fromEntries(this.itemStates);
      console.log(JSON.stringify(obj, null, 2));
      this.qti3player.suspendAttempt('end')
    },

    //event handler of qti3itemplayer suspendAttempt and end attempt
    //data object has a property "target" which is the target string of function call
    //qti3player.suspendAttempt('end') -> data{..., target: "end"}

    //data is the current state of the item (question) along with its correct answer and current answer
    onItemSaved(data) {
      //save state of the current item (question) in map --> saves current answer
      console.log( JSON.stringify(data.state, null, 2) );
      this.itemStates.set(data.state.guid, data.state)

      switch (data.target) {
        case 'next':
          this.currentIndex++
          this.loadCurrentItem()
          break
        case 'prev':
          this.currentIndex--
          this.loadCurrentItem()
          break
        case 'end':
          this.finalizeTest()
          break
      }
    },

    finalizeTest() {
      this.TC.setItemStates(this.itemStates)

      this.isReviewMode = true
    },

    onReviewPlayerReady(player, testItem) {
      var playerState = this.itemStates.get(testItem.guid)
      console.log("[ON REVIEW PLAYER READY ITEM:]")
      console.log(JSON.stringify(testItem, null, 2));
      console.log("REVIEW PLAYER READY STATE")
      console.log(JSON.stringify(playerState, null, 2));

      const config = {
        guid: testItem.guid,
        status: 'review',
        state: playerState
      }

      player.loadItemFromXml(testItem.xml, config)

    },






    loadReviewItem(player, item) {
      const guid = item.guid
      const state = this.itemStates.get(guid)

      if (!state) return

      const config = {
        guid: guid,
        status: 'review',
        state: state
      }

      player.loadItemFromXml(item.xml, config)
    },
    getItemFromTest(identifier) {
      const item = this.testItems.find(item => item.identifier === identifier)
      return item
    },

    getTitleFromXml(xmlString) {
      const parser = new DOMParser();
      const xml = parser.parseFromString(xmlString, "text/xml");
      const item = xml.querySelector("qti-assessment-item");
      return item?.getAttribute("title") || "Kein Titel";
    },

    getPromptFromXml(xmlString) {
      const parser = new DOMParser();
      const xml = parser.parseFromString(xmlString, "text/xml");
      const prompt = xml.querySelector("qti-prompt");
      return prompt?.textContent?.trim() || "Kein Fragetext";
    },

    getResponseValue(itemState) {
      const response = itemState.responseVariables.find(v => v.identifier === "RESPONSE");
      return response?.value || null;
    },

    getCorrectAnswer(guid) {
      var itemState = this.itemStates.get(guid)
      console.log( JSON.stringify(itemState, null, 2) )
      const response = itemState.responseVariables.find(v => v.identifier === "RESPONSE");
      return response?.correctResponse || "Unbekannt";
    },
  },
  created() {
    this.TC = new TestControllerUtilities()
  },
  mounted() {
    this.loadTest(this.$route.params.id)
  }
}
</script>
<style scoped>
.item-player-card {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
::v-deep(.player-wrapper *) {
  background-color: #f8f9fa;

}
</style>