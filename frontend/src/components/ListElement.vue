<template>
  <div class="list-item">

    <div class="text-block">
      <button class="module-name" @click="$emit('open', moduleName)" v-if="showModuleButton">
        {{ moduleName }}
      </button>

      <label class="primary-text" v-if="showTestName">
        {{ testName }}
      </label>

      <p class="secondary-text" v-if="showText">
        {{ textarea }}
      </p>
    </div>

    <div v-if="!isWeiterlernen">
      <div class="progress-bar">
        <div class="progress-fill"
             :style="{ width: progressPercent + '%' }">
        </div>
      </div>
    </div>

    <div v-if="showProgressText && !isWeiterlernen">
      <span class="progress-text">
        {{ completed }}/{{ total }} {{ progressLabel }}
      </span>
    </div>

    <button v-if="showButton" class="primary" @click="$emit('open')">
      {{ buttonText }}
    </button>

    <div v-if="isWeiterlernen" class="weiterlernen-progress">
      <div class="progress-bar">
        <div class="progress-fill"
             :style="{ width: progressPercent + '%' }">
        </div>
      </div>
      <span class="progress-text">
        {{ completed }}/{{ total }} {{ progressLabel }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListElement",

  props: {
    moduleName: {
      type: String,
      required: true
    },
    showModuleButton: {
      type: Boolean,
      default: false
    },
    testName: {
      type: String,
      default: ""
    },
    showTestName: {
      type: Boolean,
      default: false
    },
    showProgressText: {
      type: Boolean,
      default: false
    },
    showButton: {
      type: Boolean,
      default: false
    },
    buttonText: {
      type: String,
      default: "Starten"
    },
    completed: {
      type: Number,
      default: 0
    },
    total: {
      type: Number,
      default: 1
    },
    showText: {
      type: Boolean,
      default: false
    },
    textarea: {
      type: String,
      default: ""
    }
  },

  computed: {
    progressPercent() {
      if (this.total === 0) return 0;
      return Math.min(100, Math.round((this.completed / this.total) * 100));
    },
    isWeiterlernen() {
      return this.textarea === "Weiterlernen";
    },
    progressLabel() {
      if (this.showModuleButton) {
        return "Tests"
      }
      if (this.showTestName || this.isWeiterlernen()) {
        return "Fragen"
      }
      return ""
    }
  }
}
</script>

<style scoped>
.weiterlernen-progress {
  grid-column: 1 / 4;
  display: flex;
  align-items: center;
  gap: 5px;
}

.weiterlernen-progress .progress-bar {
  flex: 1;
}

.text-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.list-item {
  display: grid;
  grid-template-columns: 220px 1fr auto auto;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
  min-height: 62px;
  padding: 20px;
  background: #f3f3f3;
  border-radius: 14px;
  margin: 20px auto;
}

.module-name {
  text-align: left;
  font-size: 25px;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: #e8e8e8;
  border-radius: 20px;
  overflow: hidden;
  margin-right: 24px;
}

.progress-fill {
  height: 100%;
  background: #dd7a34;
  transition: width .3s ease;
}

.primary {
  white-space: nowrap;
  justify-self: end;
  align-self: center;
  width: auto;
  margin-left: 24px;
}

.progress-text {
  font-size: 18px;
  white-space: nowrap;
  margin-left: 24px;
}
</style>