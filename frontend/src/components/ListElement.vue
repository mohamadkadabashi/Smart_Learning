<template>
  <div class="list-item">
    <div class="text-block">
      <button
        v-if="isSubject"
        class="module-name"
        @click="emitOpen"
      >
        {{ name }}
      </button>

      <label v-else class="module-name module-name--static">
        {{ name }}
      </label>
    </div>

    <div class="progress-wrapper">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>

      <span class="progress-text">
        {{ completed }}/{{ total }} {{ progressLabel }}
      </span>
    </div>

    <button
      v-if="showButton"
      class="primary"
      @click="emitOpen"
    >
      {{ buttonText }}
    </button>
  </div>
</template>

<script>
export default {
  name: "ListElement",
  props: {
    name: { type: String, required: true },
    buttonText: { type: String, default: "Starten" },
    completed: { type: Number, default: 0 },
    total: { type: Number, default: 1 },
    isSubject: { type: Boolean, default: false },

    // ✅ neu: optional payload (z.B. { id: test.id })
    payload: { type: [Object, String, Number], default: null },

    // ✅ neu: Button optional (du verwendest das ja schon im Parent)
    showButton: { type: Boolean, default: true },
  },

  computed: {
    progressPercent() {
      if (this.total === 0) return 0;
      return Math.min(100, Math.round((this.completed / this.total) * 100));
    },
    progressLabel() {
      return this.isSubject ? "Tests" : "Fragen";
    }
  },

  methods: {
    emitOpen() {
      // ✅ abwärtskompatibel: wenn payload nicht gesetzt ist -> name wie bisher
      this.$emit("open", this.payload ?? this.name);
    }
  }
};
</script>


<style scoped>
.text-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.list-item {
  display: grid;
  grid-template-columns: 220px 1fr auto;
  align-items: center;
  gap: 24px;
  width: 100%;
  max-width: 1100px;
  min-height: 62px;
  padding: 20px;
  background: #f3f3f3;
  border-radius: 14px;
  margin: 20px;
}


.module-name {
  text-align: left;
  font-size: 25px;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}

.module-name--static {
  text-decoration: none;
  cursor: default;
  pointer-events: none;
}

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: nowrap;
  min-width: 0;
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
  transition: width .3s ease;
}

.progress-text {
  white-space: nowrap;
  font-size: 18px;
  flex-shrink: 0;
}

.primary {
  white-space: nowrap;
  justify-self: end;
  align-self: center;
  width: auto;
  margin-left: 24px;
}

@media (max-width: 900px) {
  .list-item {
    grid-template-columns: 1fr auto;
    grid-template-areas:
      "name button"
      "progress progress";
    row-gap: 12px;
  }

  .text-block {
    grid-area: name;
  }

  .progress-wrapper {
    grid-area: progress;
    width: 100%;
  }

  .primary {
    grid-area: button;
    margin-left: 0;
  }

  .module-name {
    font-size: 22px;
  }

  .progress-text {
    font-size: 16px;
  }
}

@media (max-width: 520px) {
  .list-item {
    grid-template-columns: 1fr;
    grid-template-areas:
      "name"
      "progress"
      "button";
  }

  .primary {
    justify-self: stretch;
    width: 100%;
  }

  .list-item {
    padding: 16px;
    gap: 12px;
  }

  .progress-bar {
    height: 10px;
  }
}
</style>
