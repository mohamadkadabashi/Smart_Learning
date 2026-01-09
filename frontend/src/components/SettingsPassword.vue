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

      <p v-if="error" class="text-danger">{{ error }}</p>
      <p v-if="success" class="text-success">{{ success }}</p>
    </div>

    <div class="password-actions">
      <button class="primary" type="button" :disabled="loading || !password" @click="onChangePassword">
        {{ loading ? "..." : "Passwort ändern" }}
      </button>
    </div>
  </section>
</template>

<script>
import PasswordInput from '@/components/PasswordInput.vue'
import { updateUserPassword } from '../services/user';

export default {
  name: 'SettingsPassword',
  components: { PasswordInput },
  data() {
    return {
      password: '',
      repeatPassword: '',
      loading: false,
      error: "",
      success: "",
      userId: null,
    };
  },
  mounted() {
    this.userId = localStorage.getItem("user_id");
  },
  methods: {
        async onChangePassword() {
      this.error = "";
      this.success = "";

      if (!this.userId) {
        this.error = "Kein Benutzer gefunden (Token enthält keine User-ID).";
        return;
      }
      if (this.password !== this.repeatPassword) {
        this.error = "Passwörter stimmen nicht überein.";
        return;
      }
      if (this.password.length < 8) {
        this.error = "Passwort muss mindestens 8 Zeichen haben.";
        return;
      }

      this.loading = true;
      try {
        await updateUserPassword(this.userId, this.password);
        this.success = "Passwort wurde geändert.";
        this.password = "";
        this.repeatPassword = "";
      } catch (e) {
        this.error = e?.response?.data?.detail || "Fehler beim Ändern des Passworts.";
      } finally {
        this.loading = false;
      }
    },
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
  padding: 20px;
  box-sizing: border-box;
}

.password-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px;
  margin-top: 12px;
}

.password-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
  margin-bottom: 16px;
}

@media (max-width: 1200px) {
  .password-grid {
    grid-template-columns: 1fr;
  }
}
</style>
