<template>
  <div class="card">
    <h2>Tagesziel anpassen</h2>

    <div class="labels-row">
      <span class="label-italic">Tests bestehen pro Tag</span>
      <span class="label-italic">Streak 🔥</span>
    </div>

    <div class="controls-row">
      <div class="left-group">
        <input
          class="goal-input"
          type="number"
          min="1"
          :value="goal"
          @input="$emit('update:goal', toNumber($event.target.value))"
        />

        <button class="btn" @click="$emit('update:goal', goal + 1)">+</button>
        <button class="btn" @click="$emit('update:goal', Math.max(1, goal - 1))">−</button>
      </div>

      <label class="switch">
        <input
          type="checkbox"
          :checked="streak"
          @change="$emit('update:streak', $event.target.checked)"
        />
        <span class="slider"></span>
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsDailyGoal',
  props: {
    goal: { type: Number, default: 3 },
    streak: { type: Boolean, default: true }
  },
  emits: ['update:goal', 'update:streak'],
  methods: {
    toNumber(v) {
      const n = Number(v)
      return Number.isFinite(n) && n >= 1 ? n : 1
    }
  }
}
</script>

<style scoped>
.card {
  width: 548px;
  min-height: 271px;
  background: #f3f3f3;
  border-radius: 30px;
  padding: 22px 20px;
  box-sizing: border-box;
}

h2 {
  margin: 0 0 12px;
  font-size: 28px;
  font-weight: 400;
}

.label-italic {
  font-style: italic;
  font-size: 24px;
}

.labels-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.left-group {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
}

.goal-input {
  flex: 0 0 150px;
  width: 150px;
  min-width: 0;
  height: 56px;

  background: #ffffff;
  border: 3px solid var(--primary-color);
  border-radius: 30px;
  text-align: center;
}

.btn {
  width: 40px;
  height: 40px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #d9d9d9;
  border-radius: 5px;
  border: none;

  font-size: 28px;
  font-weight: 600;
  line-height: 1;
  padding: 0;

  cursor: pointer;
}

.switch {
  width: 66px;
  height: 30px;
  position: relative;
  flex: 0 0 auto;
}

.switch input {
  opacity: 0;
}

.slider {
  position: absolute;
  inset: 0;
  background: var(--primary-color);
  border-radius: 30px;
}

.slider::before {
  content: "";
  position: absolute;
  width: 21px;
  height: 20px;
  background: white;
  border-radius: 50%;
  top: 5px;
  left: 6px;
  transition: transform 0.2s;
}

.switch input:checked + .slider::before {
  transform: translateX(33px);
}

@media (max-width: 480px) {
  .labels-row span:last-child {
    display: none;
  }

  .controls-row {
    flex-wrap: wrap;
    gap: 12px;
  }

  .left-group {
    width: 100%;
    justify-content: space-between;
    gap: 10px;
  }

  .goal-input {
    flex: 0 0 120px;
    width: 120px;
  }

  .switch {
    margin-left: auto;
    width: 66px;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
    position: relative;
  }

  .switch::before {
    content: "Streak 🔥";
    font-style: italic;
    font-size: 24px;
    line-height: 1.2;
    white-space: nowrap;
  }

  .slider {
    position: relative;
    inset: auto;
    width: 66px;
    height: 30px;
  }

  .switch input {
    position: absolute;
    width: 0;
    height: 0;
    opacity: 0;
  }
}

@media (max-width: 1200px) {
  .card {
    width: 100%;
  }
}
</style>
