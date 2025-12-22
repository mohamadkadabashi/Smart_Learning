<template>
  <div class="settings-password-wrapper">
    <!-- Grey card -->
    <div class="settings-card">
      <h2>Passwort ändern</h2>

      <div class="password-row">
        <PasswordInput
          label="Neues Passwort"
          v-model="password"
        />

        <PasswordInput
          label="Neues Passwort wiederholen"
          v-model="repeat"
        />
      </div>
    </div>

    <div class="btn-row">
      <button class="primary" @click="changePassword">
        Passwort ändern
      </button>
    </div>
  </div>
</template>

<script>
import PasswordInput from '@/components/PasswordInput.vue'

export default {
  name: 'SettingsPassword',
  components: {
    PasswordInput
  },
  data() {
    return {
      password: '',
      repeat: ''
    }
  },
  methods: {
    changePassword() {
      console.log('Password change', this.password, this.repeat)
    }
  }
}
</script>

<style scoped>
/* wrapper spacing only */
.settings-password-wrapper {
  margin-top: 3rem;
}

.settings-card {
  padding: 2rem;
}

.password-row {
  display: flex;
  gap: 3rem;
  margin-top: 1.5rem;
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style>
