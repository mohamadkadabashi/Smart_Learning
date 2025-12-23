<template>
  <div class="settings-section">
    <div class="settings-grid">
      <div class="settings-card">
        <h2>Persönliche Daten ändern</h2>

        <label for="settings-username">Nutzername</label>
        <input
          id="settings-username"
          class="settings-input"
          type="text"
          v-model="username"
        />

        <label for="settings-email">E-Mail-Adresse</label>
        <input
          id="settings-email"
          class="settings-input"
          type="email"
          v-model="email"
        />
      </div>

      <div class="settings-card">
        <h2>Tagesziel anpassen</h2>

        <div class="settings-goal-row">
          <div class="settings-goal-left">
            <label class="settings-inline-label" for="settings-goal">Tests bestehen pro Tag</label>

            <div class="settings-counter">
              <button class="number-minus" type="button" @click="decrease" aria-label="Minus"></button>

              <input
                id="settings-goal"
                class="settings-goal-input"
                type="number"
                v-model.number="goal"
                min="1"
              />

              <button class="number-plus" type="button" @click="increase" aria-label="Plus"></button>
            </div>
          </div>

          <div class="settings-goal-right">
            <label class="settings-inline-label">Streak 🔥</label>

            <label class="settings-switch">
              <input type="checkbox" v-model="streak" />
              <span class="settings-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div class="settings-actions">
        <button class="primary" type="button" @click="save">
          Speichern
        </button>
      </div>
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
      this.goal += 1
    },
    decrease() {
      if (this.goal > 1) this.goal -= 1
    },
    save() {
      console.log('Profile settings saved', this.username, this.email, this.goal, this.streak)
    }
  }
}
</script>
