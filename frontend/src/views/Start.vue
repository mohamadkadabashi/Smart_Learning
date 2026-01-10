<template>
  <div class="container-fluid py-4 px-4">

    <createModule v-if="showCreateModule" @close="showCreateModule = false" />

    <div class="row align-items-center mb-5">
      <div class="col-md-9">
        <h1>Hallo {{ userData.name }}, 🔥 {{ userData.streak }}</h1>
        <p v-if="isLoggedIn" class="secondary-text mt-2">Du hast heute {{ userData.openExercises }} Übungen offen.</p>
        <p v-else class="secondary-text mt-2">Bitte melde dich an.</p>
      </div>
      <div class="col-md-3 d-flex justify-content-end">
        <CircularProgress :value="userData.dailyGoalPercent" />
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-4" v-for="(card, index) in statsCards" :key="index">
        <div class="small-card h-100 w-100 d-flex">
          <StatsCard :title="card.title" :value="card.value" :subtitle="card.subtitle"
            :subtitleClass="card.subtitleClass" :iconSrc="card.iconSrc" />
        </div>
      </div>
    </div>

    <div class="row mb-5">
      <div class="col-12">
        <ContinueElement :subtitle="lastTest.title" :progress="lastTest.progress" @continue="startLearning" />
      </div>
    </div>

    <div class="row mb-5">

      <div class="col-lg">
        <div class="d-flex align-items-center mb-3 gap-3" style="height: 40px;">
          <h2 class="fst-italic mb-0">Deine Module</h2>
          <button class="primary d-flex align-items-center justify-content-center"
            style="width: 30px; height: 30px; padding: 0; min-width: auto; min-height: auto;"
            @click="showCreateModule = true">
            <img src="/assets/images/plus-icon.svg" alt="+" style="width: 15px; filter: brightness(0);" />
          </button>
        </div>

        <div class="module-scroll-container">
          <ListElement v-for="modul in moduleList" :key="modul.id" :name="modul.title" :completed="modul.completed"
            :total="modul.total" :isSubject="true" @open="openModule" />
        </div>
      </div>

      <div class="col-lg-auto">
        <div class="mt-5 pt-2">
          <CreateTestCard />
        </div>
      </div>
    </div>
    <!-- Tests Table -->
    <div class="card-body">
      <div class="table-responsive">
        <table class="table mb-0">
          <thead>
            <tr>
              <th>Test</th>
              <th class="text-end">Questions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="test in tests" :key="test.id">
              <td>
                <router-link :to="{ name: 'Test', params: { id: test.id } }">
                  {{ test.title }}
                </router-link>
              </td>
              <td class="text-end">{{ test.items.length }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- Tests Table -->
    </div>
</template>

<script>
import StatsCard from '@/components/StatsCard.vue';
import CircularProgress from '@/components/CircularProgress.vue';
import createModule from "@/components/createModule.vue";
import ListElement from "@/components/ListElement.vue";
import ContinueElement from '@/components/ContinueElement.vue';
import CreateTestCard from '@/components/CreateTestCard.vue';
import { getCurrentUser, isAuthenticated } from '@/services/auth.js';

export default {
  name: 'Start',
  components: {
    StatsCard,
    CircularProgress,
    createModule,
    ListElement,
    ContinueElement,
    CreateTestCard
  },
  data() {
    return {
      showCreateModule: false,
      isLoggedIn: false,

      // ---------------------------------------------------------
      // MOCK DATA
      // ---------------------------------------------------------
      userData: {
        name: "Gast",
        streak: 0,
        openExercises: 2,
        dailyGoalPercent: 65,
        successRate: 82,
        learningMinutesCurrent: 154,
        learningMinutesLast: 134
      },

      lastTest: {
        title: "Test 3 - Webentwicklung Grundlagen",
        progress: 50
      },

      moduleList: [
        { id: 1, title: "Medieninformatik", completed: 4, total: 10 },
        { id: 2, title: "Datenbanken", completed: 7, total: 10 },
        { id: 3, title: "Mathe", completed: 1, total: 8 },
        { id: 4, title: "Programmieren I", completed: 19, total: 20 },
        { id: 5, title: "Software Engineering", completed: 1, total: 4 }
      ]
    }
  },
  computed: {
    statsCards() {
      const h = Math.floor(this.userData.learningMinutesCurrent / 60);
      const m = this.userData.learningMinutesCurrent % 60;

      return [
        {
          title: 'Lernzeit diese Woche',
          value: `${h}h ${m}min`,
          subtitle: '+15% zur Vorwoche',
          subtitleClass: 'text-success',
          iconSrc: '/assets/images/clock.svg'
        },
        {
          title: 'Erfolgsquote',
          value: this.userData.successRate + '%',
          subtitle: 'Hohe Quote',
          subtitleClass: 'text-success',
          iconSrc: '/assets/images/checked-circle.svg'
        },
        {
          title: 'Tests bestanden',
          value: '3/5 Tests',
          subtitle: 'Diese Woche',
          iconSrc: '/assets/images/document-text-sharp.svg'
        }
      ];
    }
  },
  methods: {
    async loadUsername() {
      // check if logged in ?
      if (isAuthenticated()) {
        try {
          // yes - take username
          const user = await getCurrentUser();
          this.userData.name = user.username;
          this.isLoggedIn = true;
        } catch (error) {
          console.error("Error while loading Username:", error);
          this.userData.name = "Gast";
          this.isLoggedIn = false;
        }
      } else {
        // no - use "Gast"
        this.userData.name = "Gast";
        this.isLoggedIn = false;
      }
    },
    startLearning() {
      console.log("clicked continue learning");
      // code to start learning session
    },
    openModule(moduleName) {
      console.log("Modul öffnen:", moduleName);
    }
  },
  mounted() {
    console.log(this.tests, this.tests.length)
  },
  created() {
    this.tests = this.$testService.getTests();
    this.loadUsername();
  }
}
</script>

<style scoped>
.module-scroll-container {
  max-height: 130px;
  overflow-y: auto;
  padding-right: 10px;
}
</style>