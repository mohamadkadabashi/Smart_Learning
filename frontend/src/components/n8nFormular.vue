<template>
  <div class="formular-container">

    <form class="form-grid">

      <div class="column">
        <!-- module -->
        <div class="form-group">
          <label>Modul</label>
          <select title="Modul wählen" id="module-input" v-model="subject">
            <option value="" disable hidden>Bitte auswählen</option>
            <option
              v-for="modul in user_subjects"
              :key="modul.id"
              :value="modul.id">
              {{ modul.name }}
            </option>
          </select>
        </div>

        <!-- task type -->
        <div class="form-group">
          <label for="task-type-input">Aufgabentyp</label>
          <select title="Aufgabentyp wählen" id="task-type-input" v-model="question_typ">
            <option value="" disable hidden>Bitte auswählen</option>
            <option>Single Choice</option>
            <option>Multiple Choice</option>
            <option>Freitext</option>
          </select>
        </div>

          
        <!-- upload file -->
        <FileUpload @update-files="files = $event"/>
      </div>

      <div class="column">
        <!-- test name -->
        <div class="form-group">
          <label for="test-name-input">Name des Tests</label>
          <input type="text" placeholder="Gib einen Testnamen ein" id="test-name-input" v-model="testname" />
        </div>

        <div class="form-group">
        <!-- count of tasks -->
          <label for="num-input">Anzahl der Fragen</label>
          <div class="number-wrapper">
            <input id="num-input" type="number" min="1" max="10" placeholder="z. B. 10" v-model.number="question_count"/>
            <button type="button" 
                    class="number-minus" 
                    @click="question_count--" 
                    :disabled="question_count <= 1"
                    aria-label="Minimiere die Anzahl der Fragen" />
            <button type="button" 
                    class="number-plus" 
                    @click="question_count++" 
                    :disabled="question_count >= 10"
                    aria-label="Erhöhe die Anzahl der Fragen" />
          </div>
        </div>

      </div>

    </form>

      <button type="button"
              class="primary"
              @click="onSubmit">
        Test erstellen
      </button>

  </div>
</template>

<script>
    import FileUpload from '@/components/FileUpload.vue'
    import { createSubjectTest } from "@/services/subjectTest.js"
    import { getUserSubjects } from '../services/subject.js';

    export default {
        components: {
            FileUpload
        },

        data() {
            return {
                question_count: 1,
                files: [],
                testname: "",
                subject: "",
                question_typ: "",
                error: "",
                user_subjects: [],
            }
        },

        async created() {
          try {
            const user_id = 1;
            const response = await getUserSubjects({user_id});
            this.user_subjects = response.data;
          } catch (e) {
            this.error = e?.response?.data?.detail || "Konnte User-Subjects nicht laden.";
          }
        },

        methods: {
          async onSubmit() {
            console.log("TESTDATEN", this.testname, this.subject, this.question_typ, this.question_count, this.files[0]);
            this.error = "";

            try{
                await createSubjectTest(this.files[0], this.testname, this.subject, this.question_typ, this.question_count);
                //this.$router.push("/")
            } catch(err){
                this.error =
                    err?.response?.data?.detail ||
                    err?.message ||
                    "n8n konnte nicht beginnen";
            }
          }
        }
    }
</script>

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

.number-minus:disabled, 
.number-plus:disabled {
    opacity: 0.5;
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
