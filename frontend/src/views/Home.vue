<template>
  <div>
    <!-- Button for create module popup -->
    <button class="primary create-btn" @click="showCreateModule = true">
      <PlusIcon class="plus-icon" alt="Modul erstellen" />
    </button>
    <ActionsSubject
      v-if="showCreateModule"
      :userId="user_id"
      @close="showCreateModule = false"
      @created="handleModuleCreated"
    />

    <div class="main-content container-fluid py-5 d-flex flex-column align-items-center gap-4">
      <div class="d-flex gap-3">
        <StatsCard v-for="(card, index) in statsCards" :key="index" :title="card.title" :value="card.value"
          :subtitle="card.subtitle" :subtitleClass="card.subtitleClass" :iconSrc="card.iconSrc" />

        <p v-if="error" class="text-danger mt-2 mb-0">{{ error }}</p>
      </div>
    </div>

    <div class="card w-100">
      <div class="main-content container-fluid py-5 d-flex justify-content-center">
        <div class="card w-100" style="max-width: 60vw;">
          <div class="card-header">
            Tests
          </div>
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
        <div style="position: absolute; right: 3rem;">
          <CircularProgress :value="65" />
        </div>
        <div>
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

import { getMe } from "/src/services/user";
import { getStatsOverview } from "/src/services/stats";
import { getSubjects, getUserSubjects } from "@/services/subject";

import {
  formatSecondsToHM,
  formatPercentFromRatio,
  calcPercentChange
} from "../../src/utils/calc_stats";

export default {
  name: 'Home',
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
.card {
  border-radius: 0.5rem;
}

.card-header {
  font-size: 1.25rem;
  font-weight: 600;
  background-color: #f8f9fa;
}

.table td,
.table th {
  vertical-align: middle;
  padding: 1rem 1.5rem;
}

.table a,
.router-link a {
  color: #007bff;
  text-decoration: none !important;
}

.table a:hover,
.router-link a:hover {
  text-decoration: none !important;
}

.main-content .card {
  max-width: 50vw !important;
}
</style>
