<template>
  <div class="list-item" :class="{ 'weiterlernen-layout': isWeiterlernen }">

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

      <div v-if="isWeiterlernen" class="progress-wrapper weiterlernen-progress">
        <div class="progress-bar">
          <div class="progress-fill"
               :style="{ width: progressPercent + '%' }">
          </div>
        </div>
      </div>
    </div>

    <div v-if="!isWeiterlernen" class="progress-wrapper weiterlernen-progress">
      <div class="progress-bar">
        <div class="progress-fill"
             :style="{ width: progressPercent + '%' }">
        </div>
      </div>
    </div>

    <div class="progress-wrapper" v-if="showProgressText">
      <span class="progress-text">
        {{ completed }}/{{ total }} Tests
      </span>
    </div>

    <button v-if="showButton" class="primary" @click="$emit('open')">
      {{ buttonText }}
    </button>

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
      return Math.min(100, Math.round((this.completed / this.total) * 100));
    },
    isWeiterlernen() {
      return this.testName === "Weiterlernen";
    }
  }
}
</script>

<style scoped>
.weiterlernen-progress {
  margin-top: 12px;
  width: 100%;
}

.weiterlernen-layout {
  grid-template-columns: 1fr auto;
  align-items: center;
}

.weiterlernen-progress .progress-bar {
  display: flex;
  width: 100%;
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
  gap: 24px;
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

.progress-wrapper {
  width: 100%;
}

.progress-bar {
  width: 100%;
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

.primary {
  white-space: nowrap;
}
</style>