<template>
  <div class="modal-overlay">
    <div class="modal-container">

      <button class="close-btn" @click="$emit('close')">
        <CloseIcon role="img" alt="Schließen"/>
      </button>

      <h2 class="heading">{{ heading }}</h2>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

      <div class="button-row">
        <button class="mt-5 primary">
          Ja
        </button>
        <button class="mt-5 secondary" @click="onCreate">
          Nein
        </button>
      </div>

    </div>
  </div>
</template>

<script>
import CloseIcon from "../../public/assets/images/close-icon.svg";

export default {
  name: "deletePopup",
  components: {
    CloseIcon
  },
  props: {
    userId: {type: Number, required: true},
    heading: {type: String, default: "Wirklich löschen?"}
  },
  data() {
    return {
      errorMsg: ""
    };
  },
  methods: {
    async onCreate(){
      this.errorMsg = "";

      try {
        this.$emit("close")
      } catch(e){
        if (e?.status === 409) this.errorMsg = "Löschen nicht möglich.";
        else if (e?.status === 422) this.errorMsg = "User existiert nicht oder Eingaben sind ungültig.";
        else this.errorMsg = e?.detail || "Unbekannter Fehler";
      }
    }
  }
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

