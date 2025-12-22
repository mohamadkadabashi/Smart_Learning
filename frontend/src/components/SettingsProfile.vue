<template>
  <div class="settings-profile">
    <div class="cards-row">
      <div class="settings-card">
        <h2>Persönliche Daten ändern</h2>

        <label>Nutzername</label>
        <input type="text" v-model="username" />

        <label>E-Mail-Adresse</label>
        <input type="email" v-model="email" />
      </div>

      <div class="settings-card">
        <h2>Tagesziel anpassen</h2>

        <div class="goal-row">
          <!-- Left -->
          <div class="goal-left">
            <label>Tests bestehen pro Tag</label>

            <div class="counter">
              <button class="number-minus" @click="decrease" />
              <input type="number" v-model.number="goal" />
              <button class="number-plus" @click="increase" />
            </div>
          </div>

          <div class="goal-right">
            <label>Streak 🔥</label>
            <input
              type="checkbox"
              role="checkbox"
              :aria-checked="streak"
              @click="streak = !streak"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="save-row">
      <button class="primary" @click="save">
        Speichern
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsProfile',
  data() {
    return {
      username: '',
      email: '',
      goal: 3,
      streak: true
    }
  },
  methods: {
    increase() {
      this.goal++
    },
    decrease() {
      if (this.goal > 1) this.goal--
    },
    save() {
      console.log('Profile settings saved')
    }
  }
}
</script>

<style scoped>
.settings-profile {
  margin-bottom: 3rem;
}

.cards-row {
  display: flex;
  gap: 3rem;
  flex-wrap: wrap;
}

.settings-card {
  padding: 2rem;
  flex: 1;
  min-width: 320px;
}

.goal-row {
  display: flex;
  align-items: center;
  gap: 6rem;
  margin-top: 1.5rem;
}

.goal-left {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.goal-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.counter {
  display: flex;
  align-items: center;
}

.save-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}
</style>
