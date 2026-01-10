<template>
  <div>
    <!-- Button for create module popup -->
    <button class="primary" @click="showCreateModule = true">
      <PlusIcon role="img" alt="Modul erstellen"/>
    </button>
    <createModule v-if="showCreateModule" @close="showCreateModule = false"/>

    <div class="main-content container-fluid py-5 d-flex flex-column align-items-center gap-4">
      <div class="d-flex gap-3">
        <StatsCard v-for="(card, index) in statsCards" :key="index" :title="card.title" :value="card.value"
          :subtitle="card.subtitle" :subtitleClass="card.subtitleClass" :iconSrc="card.iconSrc" />
      </div>
    </div>

    <div class="card w-100">
      <div
        class="main-content container-fluid py-5 d-flex justify-content-center">
        <div class="card w-100" style="max-width: 60vw;">
          <div class="card-header">
            Tests
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table mb-0">
                <thead>
                  <tr>
                    <th>Test</th>
                    <th class="text-end">Questions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="test in tests" :key="test.id">
                    <td>
                      <router-link :to="{ name: 'Test', params: { id: test.id } }">
                        {{ test.title }}
                      </router-link>
                    </td>
                    <td class="text-end">{{ test.items.length }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div style="position: absolute; right: 3rem;">
          <CircularProgress value="65" />
        </div>
        <div>
          <CreateTestCard />
        </div>
      </div>
    </div>

    <div>
      <ListElem
          v-for="module in modules"
          :key="'module-' + module.name"
          :name="module.name"
          :completed="module.completed"
          :total="module.total"
          :isSubject="module.isSubject"
          :showButton="module.showButton"
          :showProgressText="module.showProgressText"
          buttonText="Übersicht"
      />

        <ListElem
          v-for="test in testdetails"
          :key="'test-' + test.name"
          :name="test.name"
          :completed="test.completed"
          :total="test.total"
          :isSubject="test.isSubject"
          :showButton="test.showButton"
          :showProgressText="test.showProgressText"
          buttonText="Starten"
      />
    </div>

  </div>
</template>

<script>
import StatsCard from '@/components/StatsCard.vue';
import CircularProgress from '@/components/CircularProgress.vue';
import CreateTestCard from '@/components/CreateTestCard.vue';
import createModule from "@/components/createModule.vue";
import PlusIcon from "../../public/assets/images/plus-icon.svg";
import ListElem from '@/components/ListElement.vue'

export default {
  name: 'Home',
  components: {
    StatsCard,
    CircularProgress,
    CreateTestCard,
    createModule,
    PlusIcon,
    ListElem
  },
  data() {
    return {
      modules: [
        { name: "BDP", completed: 4, total: 6, isSubject: true},
        { name: "OOP", completed: 2, total: 4, isSubject: true}
      ],
      testdetails: [
        { name: "Test1", completed: 2, total: 4, isSubject: false},
      ],
      statsCards: [
        {
          title: 'Lernzeit diese Woche',
          value: '2h 34min',
          subtitle: '+15% zur Vorwoche',
          subtitleClass: 'subtitle-positive',
          iconSrc: '/assets/images/clock.svg'
        },
        {
          title: 'Erfolgsquote',
          value: '82%',
          subtitle: 'Durchschnitliche Erfolgsquote',
          iconSrc: '/assets/images/checked-circle.svg'
        },
        {
          title: 'Tests bestanden',
          value: '3/5 Tests',
          subtitle: '27 u. 4 Prüfungen',
          iconSrc: '/assets/images/document-text-sharp.svg'
        }
      ]
    }
  },
  mounted() {
    console.log(this.tests, this.tests.length)
  },
  created() {
    this.tests = this.$testService.getTests()
  }
}
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
}

.card-header {
  font-size: 1.25rem;
  font-weight: 600;
  background-color: #f8f9fa;
}

.table td,
.table th {
  vertical-align: middle;
  padding: 1rem 1.5rem;
}

.table a,
.router-link a {
  color: #007bff;
  text-decoration: none !important;
}

.table a:hover,
.router-link a:hover {
  text-decoration: none !important;
}

.main-content .card {
  max-width: 50vw !important;
}
</style>
