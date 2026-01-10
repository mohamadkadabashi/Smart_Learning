import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
import Dashboard from '../views/Home.vue'
import Test from '../views/test.vue'
import Login from '../views/LoginRegistrationView.vue'
import Settings from '../views/Settings.vue'
import Testlist from "@/views/Testlist";
import Test from '../views/test'
import Start from '../views/Start.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/start',
    name: 'Start',
    component: Start,
    meta: {
      title: 'SmartLearning',
      requiresAuth: false
    }
  },
  {
    path: '/',
    name: 'Landing',
    component: Landing,
    meta: {
      title: 'Willkommen',
      guestOnly: true
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: 'SmartLearning',
      requiresAuth: false
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: {
      title: 'Einstellungen',
      headerTitle: 'Einstellungen',
      requiresAuth: true
    }
  },
  {
    path: '/test/:id',
    name: 'Test',
    component: () =>
      import(/* webpackChunkName: "test" */ '../views/TestRunner.vue'),
    meta: {
      title: 'Test Runner',
      headerTitle: 'Lernen',
      requiresAuth: true
    }
  },
  {
    path: '/create',
    name: 'TestErstellen',
    component: Test,
    props: true,
    meta: {
      title: 'Test erstellen',
      headerTitle: 'Neuen Test anlegen',
      requiresAuth: false // später leicht änderbar
    }
  },
  {
    path: '/login-or-register',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Login / Registrierung',
      guestOnly: true
    }
  },
  {
    path: '/test-overview/:subject_id',
    name: 'TestListe',
    component: Testlist,
    props: true,
    meta: {
      title: 'Test Liste',
      headerTitle: 'Testübersicht',
      requiresAuth: false
    }
  }
  ,
  { path: '*', redirect: '/' }
]


const publicPath =
  process.env.NODE_ENV === 'production'
    ? '/testrunner/'
    : '/'

const router = new VueRouter({
  mode: 'history',
  base: publicPath,
  routes
})

function isTokenExpired(token) {
  try {
    const payloadPart = token.split('.')[1]
    const payloadJson = atob(payloadPart.replace(/-/g, '+').replace(/_/g, '/'))
    const payload = JSON.parse(payloadJson)

    if (!payload.exp) return false

    const now = Math.floor(Date.now() / 1000)
    return payload.exp <= now
  } catch (e) {
    return true
  }
}

router.beforeEach((to, from, next) => {
  document.title = to.meta?.title || 'SmartLearning'

  const token = localStorage.getItem('access_token')

  if (token && isTokenExpired(token)) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('access_token_expires_at')
  }

  const isAuthenticated = !!localStorage.getItem('access_token')

  if (to.matched.some(r => r.meta.requiresAuth) && !isAuthenticated) {
    return next({
      path: '/login-or-register',
      query: { returnTo: to.fullPath }
    })
  }

  if (to.matched.some(r => r.meta.guestOnly) && isAuthenticated) {
    return next('/dashboard')
  }

  next()
})

export default router
