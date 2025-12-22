<script setup>
import { ref } from 'vue'

// eslint-disable-next-line no-unused-vars
const value = ref(1)
</script>

<template>
  <div class="formular-container">

    <form class="form-grid">

      <div class="column">
        <!-- module -->
        <div class="form-group">
          <label>Modul</label>
          <select title="Modul wählen" id="module-input">
            <option value="">Bitte auswählen</option>
            <option>Medieninformatik</option>
            <option>Beispiel</option>
            <option>Beispiel</option>
          </select>
        </div>

        <!-- upload file -->
        <div class="form-group">
          <label>Skript hochladen</label>
          <label for="file-upload" class="upload-btn"></label>
          <form>
            <input type="file" id="file-upload" name="file-upload" class="upload">
          </form>
        </div>

        <!-- task type -->
        <div class="form-group">
          <label for="task-type-input">Aufgabentyp</label>
          <select title="Aufgabentyp wählen" id="task-type-input">
            <option value="">Bitte auswählen</option>
            <option>Single Choice</option>
            <option>Multiple Choice</option>
            <option>Freitext</option>
          </select>
        </div>
      </div>

      <div class="column">
        <!-- test name -->
        <div class="form-group">
          <label for="test-name-input">Name des Tests</label>
          <input type="text" placeholder="Gib einen Testnamen ein" id="test-name-input" />
        </div>

        <div class="form-group">
        <!-- count of tasks -->
          <label for="num-input">Anzahl der Fragen</label>
          <div class="number-wrapper">
            <input id="num-input" type="number" min="0" placeholder="z. B. 10" v-model.number="value"/>
            <button type="button" 
                    class="number-minus" 
                    @click="value--" 
                    :disabled="value <= 0"
                    aria-label="Minimiere die Anzahl der Fragen" />
            <button  type="button" 
                    class="number-plus" 
                    @click="value++" 
                    aria-label="Erhöhe die Anzahl der Fragen" />
          </div>
        </div>

      </div>

    </form>

      <button type="button" class="primary">
        Test erstellen
      </button>

  </div>
</template>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 100px;
  padding: 100px;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.formular-container {
  margin: 0 auto;
  padding: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
}

.form-group input:focus,
.form-group select:focus {
}

.number-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.primary {
  margin: 32px auto 0;
  display: block;
  padding: 12px 28px;
  position: center;
}

.number-minus:disabled {
    opacity: 0.5;
}
</style>
