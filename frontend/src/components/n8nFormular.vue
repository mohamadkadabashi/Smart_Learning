<script setup>
import { ref } from 'vue'

// eslint-disable-next-line no-unused-vars
const value = ref(1)
// eslint-disable-next-line no-unused-vars
function hello(){
console.log("Hallo");
}
</script>

<template>
  <div class="formular-container">
    <h2 class="title">Test erstellen</h2>

    <form class="form">

      <!-- Modul -->
      <div class="form-group">
        <label>Modul</label>
        <select>
          <option value="">Bitte auswählen</option>
          <option>Medieninformatik</option>
          <option>Beispiel</option>
          <option>Beispiel</option>
        </select>
      </div>

      <!-- Testname -->
      <div class="form-group">
        <label>Name des Tests</label>
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
        <input type="number" placeholder="z. B. 10" v-model.number="value"/>
      </div>

      <div>
        <button type="button" class="number-minus" @click="value--"></button>
        <button  type="button" class="number-plus" @click="value++"></button>
      </div>

      <!-- Skript hochladen -->
      <div class="form-group">
        <label>Skript hochladen</label>
        <label for="file-upload" class="upload-btn"></label>
        <form>
          <input type="file" id="file-upload" name="file-upload" class="upload">
        </form>
      </div>

      <!-- Button -->
      <button type="button" class="primary" @click="hello">
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
}

.form-group input:focus,
.form-group select:focus {
}

</style>
