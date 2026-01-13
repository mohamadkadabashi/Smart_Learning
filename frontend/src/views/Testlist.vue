<template>
  <div class="page">

    <div class="module-header">
      <h2 class="module-info">
        {{ moduleName }}
      </h2>
      <div class="module-actions">
        <EditIcon class="EditIcon" alt="Modul bearbeiten" @click="showCreateModule = true"/>
        <TrashIcon class="TrashIcon-black" alt="Modul löschen" @click="showDeletePopup = true"/>
      </div>
      <createModule
          v-if="showCreateModule"
          :userId="user_id"
          heading="Modulname bearbeiten"
          label="Neuer Modulname"
          submit-text="Speichern"
          @submit="updateModuleName"
          @close="showCreateModule = false"
      />
      <DeletePopup
          v-if="showDeletePopup"
          :user-id="user_id"
          heading="Modul wirklich löschen?"
          @close="showDeletePopup = false"
      />
    </div>
    <section class="tests-container">
      <div class="tests-section">
        <h3>Aktive Tests</h3>
        <div class="scroll-area">
          <div class="list-row" v-for="(test) in activeTests" :key="'active-' + test.name">
              <ListElem
                  :name="test.name"
                  :completed="test.completed"
                  :total="test.total"
                  :isSubject="test.isSubject"
                  :showButton="test.showButton"
                  :showProgressText="test.showProgressText"
                  buttonText="Starten"
              />
            <TrashIcon class="TrashIcon" alt="Test löschen" @click="removeTest(test.name)"/>
          </div>
        </div>
      </div>

      <div class="tests-section">
        <h3>Abgeschlossene Tests</h3>
        <div class="scroll-area">
          <div class="list-row" v-for="(test) in completedTests" :key="'done-' + test.name">
              <ListElem
                  :name="test.name"
                  :completed="test.completed"
                  :total="test.total"
                  :isSubject="test.isSubject"
                  :showButton="test.showButton"
                  :showProgressText="test.showProgressText"
                  buttonText="Wiederholen"
              />
            <TrashIcon class="TrashIcon" alt="Test löschen" @click="removeTest(test.name)"/>
          </div>
        </div>
      </div>

    </section>
  </div>
</template>

<script>
import ListElem from '@/components/ListElement';
import TrashIcon from "../../public/assets/images/trash-icon.svg";
import EditIcon from "../../public/assets/images/edit-icon.svg";
import CreateModule from "@/components/createModule";
import DeletePopup from "@/components/deletePopup";

export default {
  components: { ListElem, TrashIcon, EditIcon, CreateModule, DeletePopup },
  data() {
    return {
      showCreateModule: false,
      showDeletePopup: false,
      testdetails: [
        {name: "Test1", completed: 2, total: 4, isSubject: false},
        {name: "Test2", completed: 2, total: 4, isSubject: false},
        {name: "Test3", completed: 2, total: 4, isSubject: false},
        {name: "Test4", completed: 4, total: 4, isSubject: false},
        {name: "Test5", completed: 4, total: 4, isSubject: false},
        {name: "Test6", completed: 4, total: 4, isSubject: false},
      ],
      moduleName: "Medieninformatik"
    }
  },
  methods: {
    removeTest(name) {
      this.testdetails = this.testdetails.filter(
          t => t.name !== name
      )
    },
    updateModuleName(newName) {
      this.moduleName = newName
    }
  },
  computed: {
    activeTests() {
      return this.testdetails.filter(
          test => test.completed < test.total
      )
    },
    completedTests() {
      return this.testdetails.filter(
          test => test.completed === test.total
      )
    }
  }
}
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

.TrashIcon:hover{
  opacity: 0.7;
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
</style>