<template>
  <section class="settings-password-section">
    <div class="settings-password-card">
      <h2>Passwort ändern</h2>

      <div class="password-grid">
        <div class="password-item">
          <PasswordInput
            label="Neues Passwort"
            v-model="password"
          />
        </div>

        <div class="password-item">
          <PasswordInput
            label="Neues Passwort wiederholen"
            v-model="repeatPassword"
          />
        </div>
      </div>
    </div>

    <div class="password-actions">
      <button class="primary" type="button">
        Passwort ändern
      </button>
    </div>
  </section>
</template>

<script>
import PasswordInput from '@/components/PasswordInput.vue'

export default {
  name: 'SettingsPassword',
  components: { PasswordInput },
  data() {
    return {
      password: '',
      repeatPassword: ''
    }
  }
}
</script>

<style scoped>
.settings-password-section {
  margin-top: 0;
}

.settings-password-card {
  background: #f3f3f3;
  border-radius: 30px;
  padding: 24px;
  box-sizing: border-box;
}

.password-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px;
  margin-top: 12px;
}

.password-item {
  width: 100%;
  min-width: 0;
  max-width: 100%;
}

:deep(.password-field),
:deep(.password-field .input-wrapper),
:deep(.password-field input) {
  width: 100%;
  max-width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.password-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

.password-actions .primary {
  width: 262px;
  height: 61px;
  font-size: 28px;
  font-weight: 600;
}

@media (max-width: 1200px) {
  .password-grid {
    grid-template-columns: 1fr;
  }
}
</style>
