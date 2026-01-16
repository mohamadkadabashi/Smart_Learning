<template>
  <div class="modal-overlay">
    <div class="modal-container">

      <button class="close-btn" @click="$emit('close')">
        <CloseIcon role="img" alt="Schließen"/>
      </button>

      <h2 class="heading">{{ heading }}</h2>

      <div class="form-group">
        <div class="d-flex flex-column gap-3">
          <label class="name">{{ label }}</label>
          <input class="w-100"
            type="text" 
            id="modulename" 
            v-model="modulename"
            @keyup.enter="onCreate" />
        </div>
      </div>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>

      <button class="mt-5 primary" :disabled="!modulename || loading" @click="onCreate">
        {{ loading ? loadingText : submitText }}
      </button>
    
    </div>
  </div>
</template>

<script>
import CloseIcon from "../../public/assets/images/close-icon.svg";
import { createSubject } from "@/services/subject.js"

export default {
  name: "createModule",
  components: {
    CloseIcon
  },
  props: {
    userId: {type: Number, required: true},
    heading: {type: String, default: "Neues Modul erstellen"},
    label: {type: String, default: "Name des Moduls"},
    loadingText: {type: String, default: "Laden"},
    submitText: {type: String, default: "Modul erstellen"}
  },
  data() {
    return {
      modulename: "",
      loading: false,
      errorMsg: ""
    };
  },
  methods: {
    async onCreate(){
      if (!this.modulename || this.loading) return;

      if (!this.userId) {
        this.$emit("submit", this.modulename);
        this.$emit("close");
        return;
      }

      this.loading = true;
      this.errorMsg = "";

      try {
        const created = await createSubject({
          name: this.modulename,
          user_id: this.userId
        });

        this.$emit("created", created);
        this.$emit("submit", this.modulename)

        this.$emit("close")
      } catch(e){
       if (e?.status === 409) this.errorMsg = "Du hast bereits ein Modul mit diesem Namen.";
        else if (e?.status === 422) this.errorMsg = "User existiert nicht oder Eingaben sind ungültig.";
        else this.errorMsg = e?.detail || "Unbekannter Fehler beim Erstellen.";
      } finally {
        this.loading = false;
      }
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

