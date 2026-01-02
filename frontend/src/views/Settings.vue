<template>
  <div class="settings-page">

    <div class="settings-wrapper">
      <div class="settings-grid">
        <SettingsPersonalData />

        <div class="goal-column">
          <SettingsDailyGoal />

          <div class="save-row">
            <button class="primary" type="button">
              Speichern
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

export default {
  name: 'Settings',
  components: {
    SettingsPersonalData,
    SettingsDailyGoal,
    SettingsPassword
  }
}
</script>

<style scoped>
.settings-page {
  background: #ffffff;
}

.settings-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.settings-grid {
  margin-top: 84px;
  display: grid;
  grid-template-columns: repeat(2, 548px);
  column-gap: 33px;
  row-gap: 48px;
  justify-content: center;
  align-items: start;
}

.goal-column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.save-row {
  display: flex;
  justify-content: flex-end;
}

.save-row .primary {
  width: 161px;
  height: 61px;
  font-size: 28px;
  font-weight: 600;
  border-radius: 30px;
  color: #000;
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
