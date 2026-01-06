<template>
  <div>
    <ListElem
        v-for="(module, index) in modules"
        :key="index"
        :moduleName="module.name"
        :completed="module.completed"
        :total="module.total"
        :test-name="tests[index]?.name"
        :show-progress-text="true"
        :show-button="true"
        :button-text="Starten"
        :show-test-name ="false"
        :show-module-button="true"
        :show-text="false"
        :textarea="'Test'"
    />
  </div>
</template>

<script>
import ListElem from '@/components/ListElement.vue'

export default {
  components: { ListElem },

  data() {
    return {
      modules: [
        { name: "Medieninformatik", completed: 2, total: 5 },
        { name: "Mathematik",        completed: 4, total: 8 },
        { name: "Programmierung",    completed: 1, total: 6 }
      ],
      tests: [
        { name: "Medieninformatik" },
        { name: "Mathe" },
        { name: "Programmierung"}
      ]
    }
  }
}
</script>
