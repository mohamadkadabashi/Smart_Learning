<template>
  <div class="page">
    <div class="module-header">
      <h2 class="module-info">{{ moduleName }}</h2>
      <div class="module-actions">
        <EditIcon class="EditIcon" alt="Modul bearbeiten" @click="showCreateModule = true" />
        <TrashIcon class="TrashIcon-black" alt="Modul löschen" @click="showDeleteSubjectPopup = true" />
      </div>
      
      <ActionsSubject
        v-if="showCreateModule"
        heading="Modulname bearbeiten"
        label="Neuer Modulname"
        submit-text="Speichern"
        :error="error"
        :loading="loading"
        @submit="updateModuleName"
        @close="showCreateModule = false"
      />

      <DeletePopup
        v-if="showDeleteSubjectPopup"
        heading="Modul wirklich löschen?"
        :error-msg="deleteError"
        :loading="deleteLoading"
        @close="closeDeleteSubject"
        @confirm="onDeleteSubject"
      />
    </div>

    <section class="tests-container">
      <div class="tests-section">
        <p v-if="testsError"> {{ testsError }} </p>
        <h3>Aktive Tests</h3>
        <div class="scroll-area">
          <div class="list-row" v-for="test in activeTests" :key="'active-' + test.id">
            <ListElem
              :name="test.name"
              :completed="test.completed"
              :total="test.total"
              :isSubject="false"
              :showButton="true"
              :showProgressText="true"
              buttonText="Starten"
            />

            <EditIcon
              class="EditIcon-orange"
              alt="Testsname bearbeiten"
              @click="openEditTest(test)"
            />
            <TrashIcon
              class="TrashIcon"
              alt="Test löschen"
              @click="openDeleteTest(test)"
            />
          </div>
        </div>
      </div>

      <div class="tests-section">
        <h3>Abgeschlossene Tests</h3>
        <div class="scroll-area">
          <div class="list-row" v-for="test in completedTests" :key="'done-' + test.id">
            <ListElem
              :name="test.name"
              :completed="test.completed"
              :total="test.total"
              :isSubject="false"
              :showButton="true"
              :showProgressText="true"
              buttonText="Wiederholen"
            />
            <EditIcon
              class="EditIcon-orange"
              alt="Testsname bearbeiten"
              @click="openEditTest(test)"
            />
            <TrashIcon
              class="TrashIcon"
              alt="Test löschen"
              @click="openDeleteTest(test)"
            />
          </div>
        </div>
      </div>

    </section>

    <ActionsSubject
      v-if="editTestName"
      :test-id="selectedTest ? selectedTest.id : null"
      :initial-name="selectedTest ? selectedTest.name : ''"
      heading="Testname bearbeiten"
      submit-text="Speichern"
      @submit="updateTestName"
      @close="closeEdit"
    />

    <DeletePopup
      v-if="showDeleteTestPopup"
      heading="Test wirklich löschen?"
      :error-msg="deleteError"
      :loading="deleteLoading"
      @close="closeDeleteTest"
      @confirm="onDeleteTest"
    />
  </div>
</template>

<script>
import ListElem from "@/components/ListElement";
import TrashIcon from "../../public/assets/images/trash-icon.svg";
import EditIcon from "../../public/assets/images/edit-icon.svg";
import ActionsSubject from "@/components/ActionsSubject";
import DeletePopup from "@/components/DeletePopup";

import { getSubjectById, updateSubject, deleteSubject } from "@/services/subject";
import { greeting, updateTest, deleteTest } from "@/services/subject_tests";

export default {
  name: "TestList",
  components: {
    ListElem,
    TrashIcon,
    EditIcon,
    ActionsSubject,
    DeletePopup,
  },

  props: {
    subject_id: { type: [Number, String], required: true },
  },

  data() {
    return {
      // subject
      moduleName: "",
      loading: false,
      error: "",
      success: "",
      showCreateModule: false,

      // delete popups
      showDeleteSubjectPopup: false,
      showDeleteTestPopup: false,
      deleteLoading: false,
      deleteError: "",


      // tests
      editTestName: false,
      selectedTest: null,
      testdetails: [],
      testsLoading: false,
      testsError: ""

      // Demo Daten: wichtig -> id muss existieren!
      // testdetails: [
      //   { id: 1, name: "Test1", completed: 2, total: 4 },
      //   { id: 2, name: "Test2", completed: 2, total: 4 },
      //   { id: 3, name: "Test3", completed: 2, total: 4 },
      //   { id: 4, name: "Test4", completed: 4, total: 4 },
      //   { id: 5, name: "Test5", completed: 4, total: 4 },
      //   { id: 6, name: "Test6", completed: 4, total: 4 },
      // ],
    };
  },
  async mounted() {
    try {
      const subject = await getSubjectById(Number(this.subject_id));
      this.moduleName = subject?.name || "";

      await fetchTests();
    
    } catch (e) {
      this.error = e?.response?.data?.detail || "Modul konnte nicht geladen werden.";
    }
  },

  computed: {
    activeTests() {
      return this.testdetails.filter(t => t.status !== "passed");
    },
    completedTests() {
      return this.testdetails.filter(t => t.status === "passed");
    }
  },

  methods: {
    // ---------- SUBJECT ----------
    async updateModuleName(newName) {
      this.error = "";
      this.success = "";
      this.loading = true;

      try {
        const updated = await updateSubject(Number(this.subject_id), { name: newName });
        this.moduleName = updated.name;
        this.success = "Modulname wurde gespeichert.";
        this.showCreateModule = false;
      } catch (e) {
        const status = e?.response?.status;
        const detail = e?.response?.data?.detail;

        if (status === 409) this.error = detail || "Dieses Modul existiert bereits.";
        else if (status === 404) this.error = detail || "Modul nicht gefunden.";
        else if (status === 422) this.error = detail || "Ungültige Eingabe.";
        else this.error = detail || "Update fehlgeschlagen.";
      } finally {
        this.loading = false;
      }
    },

    closeDeleteSubject() {
      this.showDeleteSubjectPopup = false;
      this.deleteError = "";
    },

    async onDeleteSubject() {
      this.deleteError = "";
      this.deleteLoading = true;

      try {
        await deleteSubject(Number(this.subject_id));
        this.showDeleteSubjectPopup = false;

        // redirect
        this.$router.push({ name: "Dashboard" }).catch(() => {});
      } catch (e) {
        const status = e?.response?.status;
        const detail = e?.response?.data?.detail;

        if (status === 403) this.deleteError = detail || "Keine Berechtigung.";
        else if (status === 404) this.deleteError = detail || "Modul nicht gefunden.";
        else this.deleteError = detail || "Löschen fehlgeschlagen.";
      } finally {
        this.deleteLoading = false;
      }
    },

    openEditTest(test) {
      this.selectedTest = test;
      this.editTestName = true;
    },

    closeEdit() {
      this.editTestName = false;
      this.selectedTest = null;
    },

    async updateTestName(newName) {
      if (!this.selectedTest) return;

      try {
        const updated = await updateTest(this.selectedTest.id, { name: newName });

        this.selectedTest.name = updated.name;

        this.closeEdit();
      } catch (e) {
        console.error("Update test failed:", e);
      }
    },

    openDeleteTest(test) {
      this.selectedTest = test;
      this.deleteError = "";
      this.showDeleteTestPopup = true;
    },

    closeDeleteTest() {
      this.showDeleteTestPopup = false;
      this.selectedTest = null;
      this.deleteError = "";
    },

    async onDeleteTest() {
      if (!this.selectedTest) return;

      this.deleteError = "";
      this.deleteLoading = true;

      try {
        await deleteTest(this.selectedTest.id);

        this.testdetails = this.testdetails.filter((t) => t.id !== this.selectedTest.id);

        this.closeDeleteTest();
      } catch (e) {
        const detail = e?.response?.data?.detail;
        this.deleteError = detail || "Test konnte nicht gelöscht werden.";
      } finally {
        this.deleteLoading = false;
      }
    },
    async fetchTests() {
      this.testsError = "";
      this.testsLoading = true;
      await greeting(Number(this.subject_id));

      try {

        const rows = await greeting(Number(this.subject_id));

        console.log(rows);

        this.testdetails = rows.map(t => ({
          id: t.id,
          name: t.name ?? `Test ${t.id}`,
          completed: t.correct_answered ?? 0,
          total: t.total_questions ?? 0,
          status: t.status ?? "in_progress",
          isSubject: false,
          showButton: true,
          showProgressText: true,
        }));

        if (this.testdetails.length === 0) {
          this.testsError = "Keine Tests vorhanden.";
        }
      } catch (e) {
        this.testsError =
          e?.response?.data?.detail ||
          "Tests konnten nicht geladen werden.";
      } finally {
        this.testsLoading = false;
      }
    }
  },
};
</script>

<style scoped>
.list-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

.page {
  display: flex;
  flex-direction: column;
  padding-left: 100px;
  padding-right: 100px;
}

.module-info {
  padding: 16px;
  flex-shrink: 0;
}

.tests-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
  min-height: 0;
}

.tests-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.tests-section h3 {
  margin-bottom: 12px;
  flex-shrink: 0;
}

.scroll-area {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.TrashIcon {
  cursor: pointer;
  flex-shrink: 0;
}

.TrashIcon:hover {
  opacity: 0.7;
}

.EditIcon-orange path {
  fill: var(--primary-color);
  cursor: pointer;
  flex-shrink: 0;
}

.EditIcon-orange:hover {
  opacity: 0.7;
  ;
}


.EditIconpath {
  fill: black;
  cursor: pointer;
}

.TrashIcon-black path {
  fill: black;
  cursor: pointer;
}

.TrashIcon-black path:hover {
  fill: #afafaf;
}

.EditIcon {
  cursor: pointer;
}

.EditIcon path:hover {
  fill: #afafaf;
}

.module-header {
  display: flex;
  align-items: center;
  padding-top: 30px;
}

.module-info {
  margin: 0;
  font-weight: 600;
}

.module-actions {
  display: flex;
  gap: 12px;
}

@media (max-width: 900px) {
  .page {
    padding-left: 32px;
    padding-right: 32px;
  }
}

@media (max-width: 600px) {
  .page {
    padding-left: 16px;
    padding-right: 16px;
  }

  .module-info {
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 8px;
  }

  .module-actions {
    flex-shrink: 0;
  }

  /* list stays in a row, but doesn't overflow */
  .list-row {
    gap: 12px;
    min-width: 0;
  }
}

/* ultra-small phones */
@media (max-width: 380px) {
  .page {
    padding-left: 12px;
    padding-right: 12px;
  }

  .list-row {
    gap: 10px;
  }
}
</style>