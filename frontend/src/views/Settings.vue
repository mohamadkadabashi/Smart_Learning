<template>
  <div class="settings-page">
    <TopBar />

    <div class="settings-content">
      <div class="settings-wrapper">
        <SettingsProfile />
        <SettingsPassword />
      </div>
    </div>
  </div>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import SettingsProfile from '@/components/SettingsProfile.vue'
import SettingsPassword from '@/components/SettingsPassword.vue'

export default {
  name: 'Settings',
  components: {
    TopBar,
    SettingsProfile,
    SettingsPassword
  }
}
</script>

<style scoped>
.settings-content {
  padding-top: 1.5rem;
  padding-bottom: 4rem;
}

.settings-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;

  display: flex;
  flex-direction: column;
  gap: 4rem;
}
</style>
