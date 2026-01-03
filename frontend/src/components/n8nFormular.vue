<script setup>
    /* eslint-disable no-unused-vars */
    import { ref, computed } from 'vue'
    import DeleteIcon from '@/../public/assets/images/delete.svg'

    const value = ref(1)
    const file = ref(null)

    function showFileName(event) {
        file.value = event.target.files[0] || null
    }

    function removeFile() {
        file.value = null
        document.getElementById('file-upload').value = ''
    }

    const fileName = computed(() => file.value?.name || '')
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
            <input type="file" id="file-upload" class="upload" @change="showFileName" title="Skript hochladen">
            <label for="file-upload" class="upload-btn"></label>
            <div v-if="fileName" class="d-flex gap-2 align-items-center">
                <span class="file-text">{{ fileName }}</span>
                <button type="button" class="delete-btn" @click="removeFile"><DeleteIcon /></button>
            </div>
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
            <input id="num-input" type="number" min="1" placeholder="z. B. 10" v-model.number="value"/>
            <button type="button" 
                    class="number-minus" 
                    @click="value--" 
                    :disabled="value <= 1"
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
  padding: 3vw;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.formular-container {
  margin: 0 auto;
  padding: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  min-height: 125px;
}

.form-group input,
.form-group select {
  padding: 10px 12px;
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

.delete-btn {
    border: none;
    background-color: transparent;
}

.delete-btn svg {
  width: 20px;
  height: 20px;
  transition: transform 0.2s ease;
}

.delete-btn:hover svg {
  transform: scale(1.1);
}

.file-text {
    max-width: 34vw;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

@media (max-width: 890px) {
    .form-grid {
        display: block;
    }

    .column {
        gap: 0;
    }

    .form-group {
        margin-bottom: 1rem;
    }
}
</style>
