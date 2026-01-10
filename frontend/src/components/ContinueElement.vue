<template>
  <div class="list-item">
    <div class="text-block">
        <h2 class="title">Weiterlernen</h2>
        <p class="subtitle">{{ subtitle }}</p>
    </div>

    <div class="progress-wrapper">
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: progress + '%' }"
        ></div>
      </div>
    </div>

    <button
      class="primary"
      @click="$emit('continue')"
    >
      Starten
    </button>
  </div>
</template>

<script>
export default {
  name: "ContinueElement",
  props: {
    subtitle: {
      type: String,
      default: ""
    },
    progress: {
      type: Number,
      default: 0
    }
  }
}
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