<template>
  <div class="settings-page">
    <div class="settings-wrapper">
      <div class="settings-grid">

        
        <SettingsPersonalData
          :username="form.username"
          :email="form.email"
          @update:username="form.username = $event"
          @update:email="form.email = $event"
        />

        <div class="goal-column">
          <SettingsDailyGoal
            :goal="form.daily_goal"
            :streak="form.streak_enabled"
            @update:goal="form.daily_goal = $event"
            @update:streak="form.streak_enabled = $event"
          />
        
          <div class="save-row">
            <p v-if="error" class="text-danger mb-0">{{ error }}</p>
            <p v-if="success" class="text-success mb-0">{{ success }}</p> 
            <button class="primary" :disabled="loading" @click="onSave">
              {{ loading ? "Speichere..." : "Speichern" }}
            </button>
          </div>
        </div>

        <div class="password-grid-item">
          <SettingsPassword />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SettingsPersonalData from '@/components/SettingsPersonalData.vue'
import SettingsDailyGoal from '@/components/SettingsDailyGoal.vue'
import SettingsPassword from '@/components/SettingsPassword.vue'
import { patchUser, getMe } from '../services/user';

export default {
  name: 'Settings',
  components: {
    SettingsPersonalData,
    SettingsDailyGoal,
    SettingsPassword
  },
 data() {
    return {
      userId: null,
      loading: false,
      error: "",
      success: "",
      initial: { username: "", email: "", daily_goal: 1, streak_enabled: true },
      form:    { username: "", email: "", daily_goal: 1, streak_enabled: true },
    };
  },

  async mounted() {
    try {
      const me = await getMe();
      this.userId = me.id;

      this.initial = {
        username: me.username,
        email: me.email,
        daily_goal: me.daily_goal,
        streak_enabled: me.streak_enabled,
      };
      this.form = { ...this.initial };
    } catch (e) {
      this.error = e?.response?.data?.detail || "Konnte User-Daten nicht laden.";
    }
  },

  methods: {
    async onSave() {
      this.error = "";
      this.success = "";

      if (!this.userId) {
        this.error = "Kein Benutzer gefunden.";
        return;
      }

      const payload = {};
      if (this.form.username !== this.initial.username) payload.username = this.form.username;
      if (this.form.email !== this.initial.email) payload.email = this.form.email;
      if (this.form.daily_goal !== this.initial.daily_goal) payload.daily_goal = this.form.daily_goal;
      if (this.form.streak_enabled !== this.initial.streak_enabled) payload.streak_enabled = this.form.streak_enabled;

      if (!Object.keys(payload).length) {
        this.success = "Keine Änderungen.";
        return;
      }

      this.loading = true;
      try {
        const updated = await patchUser(this.userId, payload);

        // sync state
        this.initial = {
          username: updated.username,
          email: updated.email,
          daily_goal: updated.daily_goal,
          streak_enabled: updated.streak_enabled,
        };
        this.form = { ...this.initial };

        this.success = "Einstellungen gespeichert.";
      } catch (e) {
        this.error = e?.response?.data?.detail || "Fehler beim Speichern.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.settings-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px 4px;
}

.settings-grid {
  margin: 10px;
  display: grid;
  grid-template-columns: repeat(2, 548px);
  column-gap: 33px;
  row-gap: 20px;
  justify-content: center;
  align-items: start;
}

.settings-page {
  overflow-x: hidden;
}

.goal-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.save-row {
  display: flex;
  justify-content: flex-end;
  gap: 8px; 
  align-items: center;  
}

.password-grid-item {
  grid-column: 1 / -1;
}

@media (max-width: 1200px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }

  .password-grid-item {
    grid-column: auto;
  }
}
</style>
