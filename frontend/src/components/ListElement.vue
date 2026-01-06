<template>
  <div class="list-item">

    <div class="text-block">
      <button class="module-name" @click="$emit('open', moduleName)" v-if="showModuleButton">
        {{ moduleName }}
      </button>

      <label class="test-name" v-if="showTestName">
        {{ testName }}
      </label>

      <p class="text-area" v-if="showText">
        {{ textarea }}
      </p>
    </div>

    <div class="progress-wrapper">
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
    }
  }
}
</script>

<style scoped>
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
  font-family: "Open Sans";
  font-size: 20px;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
}

.test-name {
  font-style: normal;
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

.text-area {
  font-family: "Open Sans";
  font-size: 15px;
  margin-top: 4px;
}

.primary {
  white-space: nowrap;
}
</style>
