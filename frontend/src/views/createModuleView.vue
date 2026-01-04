<script>
import TabContainer from '@/components/TabContainer.vue';
import createModule from '@/components/createModule.vue';

export default {
  // eslint-disable-next-line vue/no-unused-components
  components: { TabContainer, createModule }
}
</script>

<template>
  <div>
    <div class="main-content container-fluid py-5 d-flex justify-content-center flex-wrap h-100">
      <TabContainer :tabs="['Modul erstellen']">
        <template #tab-0>
          <create-module />
        </template>
      </TabContainer>
    </div>
  </div>
</template>
