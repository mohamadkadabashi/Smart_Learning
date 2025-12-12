<template>
  <div class="settings-card password-card">
    <h3>Passwort ändern</h3>

    <div class="password-row">
      <!-- New password -->
      <div class="password-field">
        <label>Neues Passwort</label>

        <div class="input-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            v-model="password"
          />

          <span class="eye" @click="showPassword = !showPassword">
            <!-- hidden -->
            <svg v-if="!showPassword" viewBox="0 0 24 24">
              <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"
                    fill="none" stroke="currentColor" stroke-width="2"/>
              <line x1="3" y1="21" x2="21" y2="3"
                    stroke="currentColor" stroke-width="2"/>
            </svg>

            <!-- visible -->
            <svg v-else viewBox="0 0 24 24">
              <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"
                    fill="none" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="12" r="3"
                      fill="none" stroke="currentColor" stroke-width="2"/>
            </svg>
          </span>
        </div>
      </div>

      <!-- Repeat -->
      <div class="password-field">
        <label>Neues Passwort wiederholen</label>

        <div class="input-wrapper">
          <input
            :type="showRepeat ? 'text' : 'password'"
            v-model="repeat"
          />

          <span class="eye" @click="showRepeat = !showRepeat">
            <svg v-if="!showRepeat" viewBox="0 0 24 24">
              <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"
                    fill="none" stroke="currentColor" stroke-width="2"/>
              <line x1="3" y1="21" x2="21" y2="3"
                    stroke="currentColor" stroke-width="2"/>
            </svg>

            <svg v-else viewBox="0 0 24 24">
              <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"
                    fill="none" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="12" r="3"
                      fill="none" stroke="currentColor" stroke-width="2"/>
            </svg>
          </span>
        </div>
      </div>
    </div>

    <div class="btn-row">
      <button class="primary-btn" @click="changePassword">
        Passwort ändern
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsPassword',
  data() {
    return {
      password: '',
      repeat: '',
      showPassword: false,
      showRepeat: false
    }
  },
  methods: {
    changePassword() {
      console.log('Password change')
    }
  }
}
</script>

<style scoped>
.settings-card {
  background: #f3f3f3;
  border-radius: 30px;
  padding: 30px;
}

h3 {
  font-weight: 400;
  margin-bottom: 20px;
}

.password-row {
  display: flex;
  gap: 40px;
}

.password-field {
  flex: 1;
}

label {
  font-style: italic;
  margin-bottom: 8px;
  display: block;
}

.input-wrapper {
  position: relative;
}

input {
  width: 100%;
  height: 56px;
  border-radius: 30px;
  border: 3px solid #f08844;
  padding: 0 56px 0 20px;
}

.eye {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #f08844;
}

.eye svg {
  width: 22px;
  height: 22px;
}

.btn-row {
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
