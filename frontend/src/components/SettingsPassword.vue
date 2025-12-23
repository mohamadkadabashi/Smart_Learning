<template>
  <div class="settings-password-wrapper">
    <div class="settings-card settings-card-wide">
      <h2>Passwort ändern</h2>

      <div class="settings-password-row">
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

    <div class="settings-password-actions">
      <button class="primary" type="button" @click="changePassword">
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