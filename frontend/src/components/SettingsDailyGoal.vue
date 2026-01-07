<template>
  <div class="card">
    <h2>Tagesziel anpassen</h2>

    <div class="goal-grid">
      <label class="label-left">
        Tests bestehen pro Tag
      </label>

      <label class="label-streak">
        Streak 🔥
      </label>

      <div class="controls">
        <input
          type="number"
          min="1"
          :value="localGoal"
          @input="onInputGoal"
        />

        <button
          class="number-plus"
          type="button"
          @click="onPlus"
        ></button>

        <button
          class="number-minus"
          type="button"
          @click="onMinus"
        ></button>
      </div>

      <div class="toggle">
        <ToggleSwitch
          :value="localStreak"
          @input="onToggleStreak"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ToggleSwitch from '@/components/ToggleSwitch.vue'

export default {
  name: 'SettingsDailyGoal',

  components: {
    ToggleSwitch
  },

  props: {
    goal: { type: Number, default: 0 },
    streak: { type: Boolean, default: true }
  },

  emits: ['update:goal', 'update:streak'],

  data() {
    return {
      localGoal: this.goal,
      localStreak: this.streak
    }
  },

  watch: {
    goal(v) {
      this.localGoal = v
    },
    streak(v) {
      this.localStreak = v
    }
  },

  methods: {
    onInputGoal(e) {
      const v = Number(e.target.value) || 0
      this.localGoal = v
      this.$emit('update:goal', v)
    },
    onPlus() {
      this.localGoal++
      this.$emit('update:goal', this.localGoal)
    },
    onMinus() {
      this.localGoal = Math.max(0, this.localGoal - 1)
      this.$emit('update:goal', this.localGoal)
    },
    onToggleStreak(v) {
      this.localStreak = v
      this.$emit('update:streak', v)
    }
  }
}
</script>

<style scoped>
.card {
  width: 548px;
  min-height: 294px;
  max-width: 100%;
  background: #f3f3f3;
  border-radius: 30px;
  padding: 22px 20px;
  box-sizing: border-box;
}

.goal-grid {
  display: grid;
  grid-template-columns: 1fr 120px;
  grid-template-areas:
    "label-left   label-streak"
    "controls     toggle";
  column-gap: 16px;
  row-gap: 6px;
  align-items: center;
}

.label-left {
  grid-area: label-left;
}

.label-streak {
  grid-area: label-streak;
  white-space: nowrap;
}

.controls {
  grid-area: controls;
  display: flex;
  align-items: center;
}

.toggle {
  grid-area: toggle;
}

.controls input {
  text-align: center;
}


@media (max-width: 480px) {
  .goal-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "label-left"
      "controls"
      "label-streak"
      "toggle";
    row-gap: 8px;
  }
}

@media (max-width: 1200px) {
  .card {
    width: 100%;
  }
}
</style>
