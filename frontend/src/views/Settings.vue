<template>
  <div>
    <TopBar />

    <div
      class="main-content container-fluid py-5 d-flex justify-content-center"
      style="margin-top: 50px;"
    >
      <div class="settings-wrapper w-100">
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
.main-content {
  margin-top: 50px;
}

/* Keep settings content centered and not too wide */
.settings-wrapper {
  max-width: 1200px;
}

/* Optional: spacing between profile + password blocks */
.settings-wrapper > *:not(:last-child) {
  margin-bottom: 40px;
}
</style>
