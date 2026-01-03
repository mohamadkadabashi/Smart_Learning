<template>
  <section class="profile-section">
    <div class="profile-grid">
      <SettingsPersonalData
        :username="username"
        :email="email"
        @update:username="username = $event"
        @update:email="email = $event"
      />

      <SettingsDailyGoal
        :goal="goal"
        :streak="streak"
        @update:goal="goal = $event"
        @update:streak="streak = $event"
      />

      <div class="profile-actions">
        <button class="primary" type="button">
          Speichern
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import SettingsPersonalData from '@/components/SettingsPersonalData.vue'
import SettingsDailyGoal from '@/components/SettingsDailyGoal.vue'

export default {
  name: 'SettingsProfile',
  components: {
    SettingsPersonalData,
    SettingsDailyGoal
  },
  data() {
    return {
      username: '',
      email: '',
      goal: 3,
      streak: true
    }
  }
}
</script>

<style scoped>
.profile-section {
  margin-top: 84px;
}

.profile-grid {
  display: grid;
  grid-template-columns: 548px 548px;
  column-gap: 33px;
  row-gap: 12px;

  grid-template-areas:
    "personal goal"
    ".        save";

  justify-content: center;

  align-items: stretch;
}

.profile-grid > :nth-child(1) {
  grid-area: personal;
}

.profile-grid > :nth-child(2) {
  grid-area: goal;
}

.profile-grid > :nth-child(1),
.profile-grid > :nth-child(2) {
  height: 100%;
}

.profile-actions {
  grid-area: save;
  display: flex;
  justify-content: flex-end;
}

.profile-actions .primary {
  width: 161px;
  height: 61px;
  font-size: 28px;
  font-weight: 600;
  border-radius: 30px;
  color: #000;
}

@media (max-width: 1200px) {
  .profile-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "personal"
      "goal"
      "save";
    row-gap: 24px;
  }

  .profile-grid > :nth-child(1),
  .profile-grid > :nth-child(2) {
    height: auto;
  }
}
</style>
