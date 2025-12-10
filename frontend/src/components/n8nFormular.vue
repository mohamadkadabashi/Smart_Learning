<script setup>
// keine Funktionen – nur Layout
// eslint-disable-next-line no-unused-vars
function hello(){
console.log("Hallo");

}
</script>

<template>
  <div class="formular-container">
    <h2 class="title">Test erstellen</h2>

    <form class="form">

      <!-- Testname -->
      <div class="form-group">
        <label>Testname</label>
        <input type="text" placeholder="Gib einen Testnamen ein" />
      </div>

      <!-- Aufgabentyp -->
      <div class="form-group">
        <label>Aufgabentyp</label>
        <select>
          <option value="">Bitte auswählen</option>
          <option>Single Choice</option>
          <option>Multiple Choice</option>
          <option>Freitext</option>
        </select>
      </div>

      <!-- Anzahl -->
      <div class="form-group">
        <label>Anzahl</label>
        <input type="number" placeholder="z. B. 10" />
      </div>

      <!-- Themengebiet -->
      <div class="form-group">
        <label>Thema</label>
        <input type="text" placeholder="z. B. Funktionen, Vektoren…" />
      </div>

      <!-- Schwierigkeit -->
      <div class="form-group">
        <label>Schwierigkeit</label>
        <select>
          <option value="">Bitte auswählen</option>
          <option>Einfach</option>
          <option>Mittel</option>
          <option>Schwer</option>
        </select>
      </div>

      <!-- Button -->
      <button type="button" class="btn" @click="hello">
        Test erstellen
      </button>

    </form>
  </div>
</template>

<style scoped>
.formular-container {
  max-width: 480px;
  margin: 0 auto;
  padding: 24px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  font-family: Arial, sans-serif;
}

.title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 20px;
  text-align: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #4d8ff7;
}

.btn {
  margin-top: 10px;
  padding: 12px;
  font-size: 16px;
  background: #4d8ff7;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn:hover {
  background: #3c7ae0;
}
</style>
