<template>
  <div class="modal-overlay">
    <div class="modal-container">

      <button class="close-btn" @click="$emit('close')"></button>

      <h2 class="heading">Neues Modul erstellen</h2>

      <div class="form-group">
        <div class="d-flex flex-column gap-3">
          <label class="name">Name des Moduls</label>
          <input type="text" id="modulename" v-model="modulename" class="w-100" />
        </div>
      </div>

      <button class="mt-5 primary" :disabled="!modulename">Modul erstellen</button>

    </div>
  </div>
</template>

<script>
export default {
  name: "createModule",
  data() {
    return {
      modulename: ""
    }
  }
};
</script>

<style scoped>
.name {
 text-align-last: left;
}
 .modal-overlay {
   position: fixed;

   background: rgba(217, 217, 217, 0.5);
   display: flex;
   align-items: center;
   justify-content: center;
   z-index: 1;
   inset: 0;
   width: 100vw;
   height: 100vh;
 }

.modal-container {
  position: relative;
  background: #ffffff;
  width: 700px;
  max-width: 90%;
  padding: 48px;
  border-radius: 32px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.close-btn {
  position: absolute;
  top: 24px;
  right: 24px;
}

.heading {
  margin-bottom: 48px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 48px;
}
</style>

