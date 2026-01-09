<template>
  <div class="settings-page">
    <div class="settings-wrapper">
      <div class="settings-grid">
        <SettingsPersonalData 
          :username="form.username"
          @update:username="from.username = $event"
          @update:email="form.email = $event"
        />

        <div class="goal-column">
          <SettingsDailyGoal 
            :goal="form.goal"
            :streak="form.streak"
            @update:goal="form.goal = $event"
            @update:streak="form.streak = $event"
          />
        
          <div class="save-row">
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
import { updateUserMail } from '../services/user';

export default {
  name: 'Settings',
  components: {
    SettingsPersonalData,
    SettingsDailyGoal,
    SettingsPassword
  },
  data() {
    return {
      loading: false,
      error: "",
      success: "",
      userId: null,

      // Originalwerte (damit du "dirty check" + reset machen kannst)
      initial: {
        username: "",
        email: "",
        goal: 0,
        streak: true,
      },

      // Formwerte (werden durch die Childs geändert)
      form: {
        username: "",
        email: "",
        goal: 0,
        streak: true,
      },
    };
  },
  mounted() {

    this.userId = localStorage.getItem("user_id");
    // TODO: hier initiale Werte laden (vom Backend oder aus Store)
    // Beispiel:
    // const me = await getMe();
  },
computed: {
    isDirty() {
      return JSON.stringify(this.form) !== JSON.stringify(this.initial);
    },
  },

  methods: {
    async onSave() {
      this.error = "";
      this.success = "";

      if (!this.userId) {
        this.error = "Kein Benutzer gefunden.";
        return;
      }

      if (this.form.email && !this.form.email.includes("@")) {
        this.error = "Bitte eine gültige E-Mail eingeben.";
        return;
      }
      if (this.form.goal < 0) {
        this.error = "Goal darf nicht negativ sein.";
        return;
      }

      // Nichts geändert? Optional:
      if (!this.isDirty) {
        this.success = "Keine Änderungen zum Speichern.";
        return;
      }

      this.loading = true;
      try {
        // 1) User Patch (username/email) nur senden, wenn sich was geändert hat
        const userPatch = {};
        if (this.form.username !== this.initial.username) userPatch.username = this.form.username;
        if (this.form.email !== this.initial.email) userPatch.email = this.form.email;

        // // 2) Daily goal ggf. eigenes endpoint
        // const goalChanged =
        //   this.form.goal !== this.initial.goal || this.form.streak !== this.initial.streak;

        // // Calls parallel (wenn beide gebraucht)
        const tasks = [];
         if (Object.keys(userPatch).length) tasks.push(updateUserMail(this.userId, userPatch));
        // if (goalChanged) tasks.push(updateDailyGoal({ goal: this.form.goal, streak: this.form.streak }));

        await Promise.all(tasks);

        // Erfolg: initial := form (damit isDirty wieder false ist)
        this.initial = JSON.parse(JSON.stringify(this.form));
        this.success = "Änderungen gespeichert.";
      } catch (e) {
        this.error = e?.response?.data?.detail || "Fehler beim Speichern.";
      } finally {
        this.loading = false;
      }
    },
  },
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
