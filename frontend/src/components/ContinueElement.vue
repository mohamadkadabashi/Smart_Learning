<template>
  <div class="list-item" v-if="!loading && randomTest">
    <div class="text-block">
      <h2 class="title">Weiterlernen</h2>
      <p class="subtitle">{{ randomTest.name }}</p>
    </div>

    <div class="progress-wrapper">
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: progressPercent + '%' }"
        ></div>
      </div>

      <span class="progress-text">
        {{ randomTest.completed }}/{{ randomTest.total }}
      </span>
    </div>

    <button class="primary" @click="openTest">
      Starten
    </button>
  </div>

  <!-- Optional: wenn du nichts anzeigen willst, einfach weglassen -->
  <p v-else-if="!loading && !randomTest">
    Keine Tests zum Weiterlernen verfügbar.
  </p>
</template>

<script>
import { getSubjects } from "@/services/subject";
import { getTestsBySubject } from "@/services/subjectTest";

export default {
  name: "ContinueElement",

  data() {
    return {
      loading: false,
      randomTest: null,
    };
  },

  mounted() {
    this.fetchRandomTest();
  },

  computed: {
    progressPercent() {
      if (!this.randomTest || this.randomTest.total === 0) return 0;
      return Math.min(
        100,
        Math.round((this.randomTest.completed / this.randomTest.total) * 100)
      );
    }
  },

  methods: {
    async fetchRandomTest() {
      this.loading = true;

      try {
        // 1) subjects laden
        const subjects = await getSubjects();
        if (!subjects || subjects.length === 0) {
          this.randomTest = null;
          return;
        }

        // 2) ein paar Versuche, falls ein Subject keine Tests hat
        const MAX_TRIES = Math.min(5, subjects.length);

        for (let i = 0; i < MAX_TRIES; i++) {
          const subject = subjects[Math.floor(Math.random() * subjects.length)];
          const subjectId = Number(subject.id);

          // 3) tests pro subject laden
          const rows = await getTestsBySubject(subjectId);

          const tests = (rows || []).map(t => ({
            id: t.id,
            name: t.name ?? `Test ${t.id}`,
            completed: t.correct_answered ?? 0,
            total: t.total_questions ?? 0,
            attempt_status: t.attempt_status, // in_progress/passed/failed/null
            subject_id: subjectId,
          }));

          if (!tests.length) continue;

          // 4) prefer active
          const active = tests.filter(
            t => !["passed", "failed"].includes(t.attempt_status)
          );
          const pool = active.length ? active : tests;

          // 5) genau EINEN wählen
          this.randomTest = pool[Math.floor(Math.random() * pool.length)];
          return;
        }

        // kein passendes subject mit tests gefunden
        this.randomTest = null;

      } catch (e) {
        console.error("fetchRandomTest failed:", e);
        this.randomTest = null;
      } finally {
        this.loading = false;
      }
    },

    openTest() {
      if (!this.randomTest) return;
      this.$router.push({
        name: "Test",
        params: { id: this.randomTest.id }
      });
    }
  }
};
</script>



<style scoped>
.list-item {
  display: grid;
  grid-template-columns: 280px 1fr auto;
  align-items: center;
  gap: 24px;
  width: 100%;
  min-height: 62px;
  padding: 20px;
  background: #f3f3f3;
  border-radius: 14px;
}

.text-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.title {
  text-align: left;
  font-size: 25px;
  font-weight: 600;
  margin: 0;
}

.subtitle {
  margin: 0;
  font-size: 16px;
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 20px;
}

.progress-bar {
  flex: 1 1 auto;
  min-width: 0;
  height: 12px;
  background: #e8e8e8;
  border-radius: 20px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #dd7a34;
  border-radius: 20px;
  transition: width .3s ease;
}

.primary {
  white-space: nowrap;
  justify-self: end;
  align-self: center;
  width: auto;
  padding-left: 3rem;
  padding-right: 3rem;
}

@media (max-width: 900px) {
  .list-item {
    grid-template-columns: 1fr auto;
    grid-template-areas:
      "text button"
      "progress progress";
    row-gap: 16px;
  }

  .text-block {
    grid-area: text;
  }

  .progress-wrapper {
    grid-area: progress;
    width: 100%;
  }

  .primary {
    grid-area: button;
  }

  .title {
    font-size: 22px;
  }
}

@media (max-width: 520px) {
  .list-item {
    grid-template-columns: 1fr;
    grid-template-areas:
      "text"
      "progress"
      "button";
  }

  .primary {
    justify-self: stretch;
    width: 100%;
    margin-left: 0;
  }

  .list-item {
    padding: 16px;
  }

  .progress-bar {
    height: 10px;
  }
}
</style>