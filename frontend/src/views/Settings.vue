<template>
  <div>
    <TopBar />

    <div class="main-content container-fluid py-5 d-flex justify-content-center">
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
/* space below fixed TopBar */
.main-content {
  margin-top: 3rem;
}

/* center settings and limit width */
.settings-wrapper {
  max-width: 1200px;
}

/* vertical spacing between sections */
.settings-wrapper > *:not(:last-child) {
  margin-bottom: 3rem;
}
</style>
