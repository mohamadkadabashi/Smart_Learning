<template>
  <div class="page">

    <p class="module-info">
      {{ name }}
    </p>

    <section class="tests-container">

      <div class="tests-section">
        <h3>Aktive Tests</h3>
        <div class="scroll-area">
          <div class="list-row" v-for="test in testdetails" :key="'test-' + test.name">
            <ListElem
                :name="test.name"
                :completed="test.completed"
                :total="test.total"
                :isSubject="test.isSubject"
                :showButton="test.showButton"
                :showProgressText="test.showProgressText"
                buttonText="Starten"
            />
            <TrashIcon class="TrashIcon" alt="Test löschen" @click="removeTest(index)"/>
          </div>
        </div>
      </div>

      <div class="tests-section">
        <h3>Abgeschlossene Tests</h3>
        <div class="scroll-area">
          <div class="list-row" v-for="test in testdetails" :key="'test-' + test.name">
            <ListElem
                :name="test.name"
                :completed="test.completed"
                :total="test.total"
                :isSubject="test.isSubject"
                :showButton="test.showButton"
                :showProgressText="test.showProgressText"
                buttonText="Wiederholen"
            />
            <TrashIcon class="TrashIcon" alt="Test löschen" @click="removeTest(index)"/>
          </div>
        </div>
      </div>

    </section>
  </div>
</template>

<script>
import ListElem from '@/components/ListElement';
import TrashIcon from "../../public/assets/images/trash-icon.svg";

export default {
  components: { ListElem, TrashIcon },
  data() {
    return {
      testdetails: [
        {name: "Test1", completed: 2, total: 4, isSubject: false},
        {name: "Test2", completed: 2, total: 4, isSubject: false},
        {name: "Test3", completed: 2, total: 4, isSubject: false},
        {name: "Test4", completed: 2, total: 4, isSubject: false},
        {name: "Test5", completed: 2, total: 4, isSubject: false},
      ]
    }
  },
  methods: {
    removeTest(index) {
      this.testdetails.splice(index, 1)
    }
  }
}
</script>

<style scoped>
.list-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page {
  display: flex;
  flex-direction: column;
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
</style>