<template>
  <div>
    <!-- Button for create module popup -->
    <button class="primary create-btn" @click="showCreateModule = true">
      <PlusIcon class="plus-icon" alt="Modul erstellen"/>
    </button>
    <createModule
      v-if="showCreateModule"
      :userId="user_id"
      @close="showCreateModule = false"
    />

    <div class="main-content container-fluid py-5 d-flex flex-column align-items-center gap-4">
      <div class="d-flex gap-3">
        <StatsCard
        v-for="(card, index) in statsCards"
        :key="index"
        :title="card.title"
        :value="card.value"
        :subtitle="card.subtitle"
        :subtitleClass="card.subtitleClass"
        :iconSrc="card.iconSrc"
      />
      
      <p v-if="error" class="text-danger mt-2 mb-0">{{ error }}</p>
      </div>
    </div>

    <div class="card w-100">
      <div
        class="main-content container-fluid py-5 d-flex justify-content-center">
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
  </div>
</template>

<script>
import StatsCard from '@/components/StatsCard.vue';
import CircularProgress from '@/components/CircularProgress.vue';
import CreateTestCard from '@/components/CreateTestCard.vue';
import createModule from "@/components/createModule.vue";
import PlusIcon from "../../public/assets/images/plus-icon.svg";
import {formatSecondsToHM, formatPercentFromRatio, calcPercentChange} from "../../src/utils/calc_stats"

export default {
  name: 'Home',
  components: {
    StatsCard,
    CircularProgress,
    CreateTestCard,
    createModule,
    PlusIcon
  },
  data() {
    return {
      tests: [], showCreateModule: false,
      statsCards: [],
      loading: false,
      error: "",
    }
  },
  async mounted() {
    await this.loadStats();
  },
  created() {
    this.tests = this.$testService.getTests()
  },
  mounted(){
    this.user_id = localStorage.getItem("user_id");
  },
  methods: {
    async loadStats() {
      this.loading = true;
      this.error = "";

      try {
        const ov = await getStatsOverview();

        // Lernzeit + Vorwoche %
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

        // Erfolgsquote (pass_rate_week ist 0..1)
        const successRateValue = formatPercentFromRatio(ov.pass_rate_week);

        // Tests bestanden
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
            iconSrc: "/assets/images/checked-circle.svg",
          },
          {
            title: "Tests bestanden",
            value: testsValue,
            subtitle: "Diese Woche",
            iconSrc: "/assets/images/document-text-sharp.svg",
          },
        ];
      } catch (e) {
        this.error = e?.response?.data?.detail || "Statistiken konnten nicht geladen werden.";
      } finally {
        this.loading = false;
      }
    },
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
