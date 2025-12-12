<template>
  <div class="settings-profile">
    <div class="cards-row">
      <!-- Personal Data -->
      <div class="settings-card">
        <h3>Persönliche Daten ändern</h3>

        <label>Nutzername</label>
        <input type="text" v-model="username" />

        <label>E-Mail-Adresse</label>
        <input type="email" v-model="email" />
      </div>

      <!-- Daily Goal -->
      <div class="settings-card">
        <h3>Tagesziel anpassen</h3>

        <div class="goal-row">
          <!-- Left block -->
          <div class="goal-left">
            <span class="goal-label">Tests bestehen pro Tag</span>

            <div class="counter">
              <button @click="decrease">−</button>
              <input type="number" v-model.number="goal" />
              <button @click="increase">+</button>
            </div>
          </div>

          <!-- Right block -->
          <div class="goal-right">
            <span class="goal-label">Streak 🔥</span>
            <label class="switch">
              <input type="checkbox" v-model="streak" />
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Save button -->
    <div class="save-row">
      <button class="primary-btn" @click="save">
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
/* layout */
.settings-profile {
  margin-bottom: 40px;
}

.cards-row {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
}

/* cards */
.settings-card {
  background: #f3f3f3;
  border-radius: 30px;
  padding: 30px;
  flex: 1;
  min-width: 320px;
}

/* titles */
h3 {
  font-weight: 400;
  margin-bottom: 20px;
}

/* inputs */
label {
  font-style: italic;
  margin-top: 15px;
  display: block;
}

input {
  width: 100%;
  height: 56px;
  border-radius: 30px;
  border: 3px solid #f08844;
  padding: 0 20px;
  margin-bottom: 10px;
}

/* --- Daily goal layout --- */
.goal-row {
  display: flex;
  align-items: center;
  margin-top: 20px;
  gap: 100px; /* 🔥 controls horizontal distance (Figma-like) */
}

.goal-left {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.goal-right {
  display: flex;
  flex-direction: column;   /* label above toggle */
  align-items: center;
  gap: 8px;
}

.goal-label {
  font-style: italic;
}

/* counter */
.counter {
  display: flex;
  gap: 10px;
  align-items: center;
}

.counter button {
  width: 40px;
  height: 40px;
  background: #d9d9d9;
  border-radius: 5px;
  border: none;
  font-size: 24px;
}

.counter input {
  width: 80px;
  height: 40px;
  text-align: center;
  margin: 0;
}

/* toggle */
.switch {
  position: relative;
  width: 60px;
  height: 30px;
}

.switch input {
  opacity: 0;
}

.slider {
  position: absolute;
  inset: 0;
  background: #f08844;
  border-radius: 30px;
}

.slider::before {
  content: '';
  position: absolute;
  width: 22px;
  height: 22px;
  background: #fff;
  border-radius: 50%;
  top: 4px;
  left: 4px;
  transition: 0.3s;
}

.switch input:checked + .slider::before {
  transform: translateX(30px);
}

/* save button */
.save-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

.primary-btn {
  background: #f08844;
  border-radius: 30px;
  padding: 12px 30px;
  font-size: 22px;
  font-weight: 600;
  border: none;
}
</style>
