import Vue from 'vue'
import App from './App.vue'
import router from './router'

// 1) Importiere unseren neu erstellten TestService
import { TestService } from '@/helpers/TestService'

Vue.config.productionTip = false

// 2) Instanz erstellen
const testService = new TestService()

// 3) Bevor Vue gemountet wird: Alle XMLs laden
async function bootstrap() {
  // Hier musst du die genauen Dateinamen angeben, die unter public/qti/ liegen.
  // Beispiel: ['test1.xml', 'test2.xml', 'meinTestDrei.xml']
  const filenames = [
    'test1.xml',
    'test2.xml',
    'cloud_computing_test.xml'
    // … alle anderen QTI-XMLs
  ]

  // parse & fülle testService.tests
  await testService.loadAllTests(filenames)

  // 4) TestService global zur Verfügung stellen
  Vue.prototype.$testService = testService

  // 5) App mounten
  new Vue({
    router,
    render: h => h(App)
  }).$mount('#app')
}

// Starte den Bootstrapping-Prozess
bootstrap()
