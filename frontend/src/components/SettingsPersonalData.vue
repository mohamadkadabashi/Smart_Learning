<template>
  <div class="card">
    <h2>Persönliche Daten ändern</h2>

    <label for="settings-username">Nutzername</label>
    <input
      id="settings-username"
      class="input"
      type="text"
      :value="username"
      @input="$emit('update:username', $event.target.value)"
    />

    <label for="settings-email">E-Mail-Adresse</label>
    <input
      id="settings-email"
      class="input"
      type="email"
      :value="email"
      @input="$emit('update:email', $event.target.value)"
    />
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
  background: #f3f3f3;
  border-radius: 30px;
  padding: 22px 20px;
  box-sizing: border-box;
}

h2 {
  margin: 0 0 12px 0;
  font-weight: 400;
  font-size: 28px;
}

label {
  display: block;
  margin: 0 0 6px 0;
  font-style: italic;
  font-weight: 400;
  font-size: 24px;
  line-height: 33px;
  color: #000;
}

.input {
  width: 507px;
  min-width: 0;
  height: 56px;
  box-sizing: border-box;

  background: #ffffff;
  border: 3px solid var(--primary-color);
  border-radius: 30px;

  padding: 0 18px;
  margin: 0 0 18px 0;
}

.input:last-of-type {
  margin-bottom: 0;
}

@media (max-width: 1200px) {
  .card {
    width: 100%;
  }
  .input {
    width: 100%;
  }
}
</style>
