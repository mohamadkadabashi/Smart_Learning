<template>
  <div class="card">
    <h2>Tagesziel anpassen</h2>

    <div class="labels-row">
      <label>Tests bestehen pro Tag</label>
      <label>Streak 🔥</label>
    </div>

    <div class="controls-row">
      <div class="left-group">
        <input
          type="number"
          min="1"
          :value="goal"
          @input="$emit('update:goal', toNumber($event.target.value))"
        />

        <button
          class="number-plus"
          type="button"
          @click="$emit('update:goal', goal + 1)"
        />

        <button
          class="number-minus"
          type="button"
          @click="$emit('update:goal', Math.max(1, goal - 1))"
        />
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
  min-height: 310px;
  background: #f3f3f3;
  border-radius: 30px;
  padding: 22px 20px;
  box-sizing: border-box;
}

h2 {
  margin: 0 0 12px;
  font-weight: 400;
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
}

.left-group input {
  width: 150px;
  height: 56px;
  text-align: center;
}

.switch {
  width: 66px;
  height: 30px;
  position: relative;
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
  background: #ffffff;
  border-radius: 50%;
  top: 5px;
  left: 6px;
  transition: transform 0.2s;
}

.switch input:checked + .slider::before {
  transform: translateX(33px);
}

@media (max-width: 480px) {
  .labels-row label:last-child {
    display: none;
  }

  .controls-row {
    flex-wrap: wrap;
    gap: 12px;
  }

  .left-group {
    width: 100%;
    justify-content: space-between;
  }

  .left-group input {
    width: 120px;
  }

  .switch {
    margin-left: auto;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
  }

  .switch::before {
    content: "Streak 🔥";
    font-style: italic;
    font-size: 24px;
    white-space: nowrap;
  }

  .slider {
    position: relative;
    width: 66px;
    height: 30px;
  }
}

@media (max-width: 1200px) {
  .card {
    width: 100%;
  }
}
</style>
