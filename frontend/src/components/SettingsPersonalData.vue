<template>
  <div class="card">
    <h2>Persönliche Daten ändern</h2>

    <div class="row">
      <label for="settings-username">Nutzername</label>
      <input
        id="settings-username"
        type="text"
        :value="username"
        @input="$emit('update:username', $event.target.value)"
      />
    </div>

    <div class="row">
      <label for="settings-email">E-Mail-Adresse</label>
      <input
        id="settings-email"
        type="email"
        :value="email"
        @input="$emit('update:email', $event.target.value)"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsPersonalData',
  props: {
    username: { type: String, default: '' },
    email: { type: String, default: '' }
  },
  emits: ['update:username', 'update:email']
}
</script>

<style scoped>
.card {
  width: 548px;
  min-height: 260px;
  background: #f3f3f3;
  border-radius: 30px;
  padding: 22px 20px;
  box-sizing: border-box;
}

.row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.row:last-child {
  margin-bottom: 0;
}

@media (max-width: 1200px) {
  .card {
    width: 100%;
  }
}
</style>
