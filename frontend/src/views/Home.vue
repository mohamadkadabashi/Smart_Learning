<template>
  <div class="container-fluid py-4 px-4">
    <!-- Popup: Modul erstellen -->
    <ActionsSubject
      v-if="showCreateModule"
      :userId="user_id"
      @close="handleCloseCreateModule"
      @created="handleModuleCreated"
    />

    <!-- Header -->
    <div class="row align-items-center mb-5">
      <div class="col-md-9">
        <h1>Hallo {{ me.username }}, 🔥 {{ me.streak }}</h1>
        <p v-if="isLoggedIn" class="secondary-text mt-2">
          Du hast heute {{ me.openExercises }} Übungen offen.
        </p>
        <p v-else class="secondary-text mt-2">Bitte melde dich an.</p>
      </div>

      <div class="col-md-3 d-flex justify-content-end">
        <CircularProgress :value="65" />
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-4" v-for="(card, index) in statsCards" :key="index">
        <div class="small-card h-100 w-100 d-flex">
          <StatsCard
            :title="card.title"
            :value="card.value"
            :subtitle="card.subtitle"
            :subtitleClass="card.subtitleClass"
            :iconSrc="card.iconSrc"
          />
        </div>
      </div>
    </div>

    <!-- Continue -->
    <div class="row mb-5">
      <div class="col-12">
        <ContinueElement />
      </div>
    </div>

    <!-- Module + Create Test -->
    <div class="row mb-5">
      <div class="col-lg">
        <div class="d-flex align-items-center mb-3 gap-3" style="height: 40px;">
          <h2 class="fst-italic mb-0">Deine Module</h2>
          <button
            class="primary d-flex align-items-center justify-content-center"
            style="width: 30px; height: 30px; padding: 0; min-width: auto; min-height: auto;"
            @click="showCreateModule = true"
            type="button"
          >
            <img
              src="/assets/images/plus-icon.svg"
              alt="+"
              style="width: 15px; filter: brightness(0);"
            />
          </button>
        </div>

        <div class="module-scroll-container">
          <ListElement v-for="subject in subjects" 
            :key="'module-' + subject.id" 
            :name="subject.name"
            :completed="subject.completed" 
            :total="subject.total" 
            :isSubject="subject.isSubject"
            :showButton="subject.showButton" 
            :showProgressText="subject.showProgressText" 
            buttonText="Übersicht" 
            @click.native="goToSubject(subject.id)"
          />
        </div>
      </div>

      <div class="col-lg-auto">
        <div class="mt-5 pt-2">
          <CreateTestCard />
        </div>
      </div>
    </div>

    <!-- Tests Table -->
    <div v-if="hidden" class="card w-100">
      <div class="card-header">Tests</div>
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
                <td class="text-end">{{ (test.items && test.items.length) || 0 }}</td>
              </tr>
              <tr v-if="!tests.length">
                <td colspan="2" class="text-muted">Keine Tests vorhanden.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StatsCard from "@/components/StatsCard.vue";
import CircularProgress from "@/components/CircularProgress.vue";
import CreateTestCard from "@/components/CreateTestCard.vue";
import ActionsSubject from "@/components/ActionsSubject.vue";
import ListElement from "@/components/ListElement.vue";
import ContinueElement from "@/components/ContinueElement.vue";

import { getMe } from "/src/services/user";
import { getStatsOverview } from "/src/services/stats";
import { getSubjects } from "@/services/subject";

import {
  formatSecondsToHM,
  formatPercentFromRatio,
  calcPercentChange,
} from "../../src/utils/calc_stats";

export default {
  name: "Start",
  components: {
    StatsCard,
    CircularProgress,
    CreateTestCard,
    ActionsSubject,
    ListElement,
    ContinueElement,
  },
  data() {
    return {
      user_id: null,
      me: {
        username: "",
        streak: 0,
        openExercises: 0,
      },
      isLoggedIn: false,
      subjects: [],
      showCreateModule: false,
      statsCards: [],
      loading: false,
      error: "",

      hidden: false,
    
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
      console.log("ME", me);

      this.me = {
        username: me?.username || "",
        streak: me?.streak || 4,
        openExercises: me?.openExercises || 2,
      };

      this.user_id = me?.id ?? null;
      this.isLoggedIn = !!this.user_id;

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