<template>
  <div class="container-fluid py-4 px-4">

    <ActionsSubject v-if="showActionsSubject" @close="showActionsSubject = false" />

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
            @click="showActionsSubject = true">
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

    <div>
      <ListElem v-for="subject in subjects" :key="'module-' + subject.id" :name="subject.name"
        :completed="subject.completed" :total="subject.total" :isSubject="subject.isSubject"
        :showButton="subject.showButton" :showProgressText="subject.showProgressText" buttonText="Übersicht" 
        @click.native="goToSubject(subject.id)"
      />
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
    </div>
    </div>
</template>

<script>
import StatsCard from '@/components/StatsCard.vue';
import CircularProgress from '@/components/CircularProgress.vue';
import CreateTestCard from '@/components/CreateTestCard.vue';
import ActionsSubject from "@/components/ActionsSubject.vue";
import PlusIcon from "../../public/assets/images/plus-icon.svg";
import ListElem from '@/components/ListElement.vue'
import createModule from "@/components/createModule.vue";
import ListElement from "@/components/ListElement.vue";
import ContinueElement from '@/components/ContinueElement.vue';
import CreateTestCard from '@/components/CreateTestCard.vue';

import { getMe, getCurrentUser, isAuthenticated } from "/src/services/user";
import { getStatsOverview } from "/src/services/stats";
import { getSubjects } from "@/services/subject";

import {
  formatSecondsToHM,
  formatPercentFromRatio,
  calcPercentChange
} from "../../src/utils/calc_stats";

export default {
  name: 'Start',
  components: {
    StatsCard,
    CircularProgress,
    CreateTestCard,
    ActionsSubject,
    PlusIcon,
    ListElem
  },
  data() {
    return {
      user_id: null,
      subjects: [],
      showCreateModule: false,
      statsCards: [],
      loading: false,
      error: "",
    };
  },
  created() {
    this.tests = this.$testService.getTests();
  },
  async mounted() {
    this.loading = true;
    this.error = "";

    try {
      const me = await getMe();
      this.user_id = me?.id ?? null;

      if (this.user_id) {
        await this.loadStats();
        await this.fetchSubjects();
        console.log("user_id: " + this.user_id)
      } else {
        this.error = "User nicht authentifiziert.";
      }
    } catch (e) {
      this.error =
        e?.response?.data?.detail ||
        "User oder Statistiken konnten nicht geladen werden.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async handleModuleCreated() {
      this.showCreateModule = false;
      await this.fetchSubjects();
      await this.loadStats(); // optional
    },
    async loadStats() {
      try {

        const ov = await getStatsOverview();
        console.log("OVERVIEW", ov);

        const change = calcPercentChange(
          ov.study_time_week_seconds,
          ov.study_time_prev_week_seconds
        );

        const studySubtitle =
          change === null
            ? "Keine Daten zur Vorwoche"
            : `${change >= 0 ? "+" : ""}${change}% zur Vorwoche`;

        const studySubtitleClass =
          change === null ? "" : (change >= 0 ? "subtitle-positive" : "subtitle-negative");

        const successRateValue = formatPercentFromRatio(ov.pass_rate_week);
        const testsValue = `${ov.tests_passed_week}/${ov.tests_total_week} Tests`;

        this.statsCards = [
          {
            title: "Lernzeit diese Woche",
            value: formatSecondsToHM(ov.study_time_week_seconds),
            subtitle: studySubtitle,
            subtitleClass: studySubtitleClass,
            iconSrc: "/assets/images/clock.svg",
          },
          {
            title: "Erfolgsquote",
            value: successRateValue,
            subtitle: "Durchschnittliche Erfolgsquote",
            subtitleClass: "",
            iconSrc: "/assets/images/checked-circle.svg",
          },
          {
            title: "Tests bestanden",
            value: testsValue,
            subtitle: "Diese Woche",
            subtitleClass: "",
            iconSrc: "/assets/images/document-text-sharp.svg",
          },
        ];
      } catch (e) {
        console.error("getStatsOverview failed:", e);
        console.error("status:", e?.response?.status);
        console.error("data:", e?.response?.data);
        throw e;
      }
    },
    async fetchSubjects() {
      try {
        const subjects = await getSubjects();
        console.log("SUBJECTS", subjects);

        this.subjects = subjects.map(s => ({
          id: s.id,
          name: s.name,
          completed: s.passed_tests ?? 0,
          total: s.total_tests ?? 0,
          isSubject: true,
          showButton: true,
          showProgressText: true,
        }));
      } catch (e) {
        console.error("getSubjects failed:", e);
      }
    },
    goToSubject(subjectId) {
      this.$router.push({
        name: "TestListe",
        params: { subject_id: subjectId }
      });
    }
  },
};
</script>

<style scoped>
.module-scroll-container {
  max-height: 130px;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 10px;
}
:deep(.list-item) {
  margin-left: 0 !important;
  margin-right: 0 !important;
  width: 100% !important;
  margin-top: 5px !important;
  margin-bottom: 15px !important;
  box-sizing: border-box; 
}
</style>