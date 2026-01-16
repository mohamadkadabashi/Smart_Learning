<template>
  <div class="modal-overlay">
    <div class="modal-container">
      <button class="close-btn" @click="$emit('close')">
        <CloseIcon role="img" alt="Schließen"/>
      </button>

      <h2 class="heading">{{ heading }}</h2>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

      <div class="button-row">
        <button class="mt-5 primary" :disabled="loading" @click="$emit('confirm')">
          Ja
        </button>
        <button class="mt-5 secondary" :disabled="loading" @click="$emit('close')">
          Nein
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import CloseIcon from "../../public/assets/images/close-icon.svg";

export default {
  name: "DeletePopup",
  components: { CloseIcon },
  props: {
    heading: { type: String, default: "Wirklich löschen?" },
    errorMsg: { type: String, default: "" },
    loading: { type: Boolean, default: false },
  },
};
</script>


<style scoped>
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

.button-row {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 40px;
}
</style>

