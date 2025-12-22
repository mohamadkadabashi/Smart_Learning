<template>
  <div class="list-item">

    <!-- Name of module, clickable -->
    <button class="module-name" @click="$emit('open', moduleName)">
      test
      {{ moduleName }}
    </button>

    <!-- progressbar -->
    <div class="progress-wrapper">
      <div class="progress-bar">
        <div class="progress-fill"
             :style="{ width: progressPercent + '%' }">
        </div>
      </div>
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
    completed: {
      type: Number,
      default: 0
    },
    total: {
      type: Number,
      default: 1
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
.list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 62px;
  max-width: 1100px;
  padding: 12px 20px;
  background: #f3f3f3;
  border-radius: 14px;
  margin: 20px;
}

/* Modulname klickbar */
.module-name {
  font-family: "Open Sans";
  font-size: 20px;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
}

/* Fortschrittsbereich */
.progress-wrapper {
  width: 50%;
}

/* Balken */
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
</style>
