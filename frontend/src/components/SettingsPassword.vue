<template>
  <div class="settings-card password-card">
    <h3>Passwort ändern</h3>

    <label>Neues Passwort</label>
    <input type="password" v-model="password" />

    <label>Neues Passwort wiederholen</label>
    <input type="password" v-model="repeat" />

    <div class="btn-row">
      <button class="primary-btn" @click="changePassword">
        Passwort ändern
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsPassword',
  data() {
    return {
      password: '',
      repeat: ''
    }
  },
  methods: {
    changePassword() {
      console.log('Password change')
    }
  }
}
</script>

<style scoped>
.settings-card {
  background: #f3f3f3;
  border-radius: 30px;
  padding: 30px;
}

h3 {
  font-weight: 400;
  margin-bottom: 20px;
}

label {
  font-style: italic;
  margin-top: 15px;
  display: block;
}

input {
  width: 100%;
  height: 56px;
  border-radius: 30px;
  border: 3px solid #f08844;
  padding: 0 20px;
}

.btn-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
}

.primary-btn {
  background: #f08844;
  border-radius: 30px;
  padding: 12px 30px;
  font-size: 22px;
  font-weight: 600;
  border: none;
}
</style>
