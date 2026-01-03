<template>
  <div>
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
    </div>
  </div>
</template>

<script>
    import CircularProgress from '@/components/CircularProgress.vue';

    export default {
        name: 'Home',
        components: {
            CircularProgress
        },
        data() {
            return {
                tests: []
            }
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

