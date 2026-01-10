<template>
    <div>
        <header class="top-bar d-flex align-items-center">
            <div class="home-section">
                <button v-if="showHomeIcon"
                        @click="navigateToHome"
                        aria-label="Zurück zur Startseite">
                    <HomeIcon role="presentation" />
                </button>
            </div>
            <h1 class="app-name">{{ headerTitle }}</h1>

            <div class="user-section d-flex gap-3">
                <button v-if="showLoginIcon"
                        @click="navigateToLogin"
                        aria-label="Zur Anmeldung/Registrierung">
                    <LoginIcon role="presentation" />
                </button>
                <button v-if="showUserIcon"
                        @click="toggleDropdown"
                        aria-label="Öffne die Nutzereinstellungen">
                    <UserIcon role="presentation" />
                </button>
            </div>
        </header>

        <!-- User Icon Dropdown -->
        <UserDropdown v-if="showUserDropdown" />
    </div>
</template>


<script>
import HomeIcon from '@/../public/assets/images/home.svg'
import UserIcon from '@/../public/assets/images/person-sharp.svg'
import LoginIcon from '@/../public/assets/images/log-in.svg'
import UserDropdown from '@/components/UserDropdown.vue'
import { isAuthenticated } from '@/services/user.js'

const ROUTE_DASHBOARD = 'Dashboard'
const ROUTE_LOGIN = 'Login'

export default {
  name: 'TopBar',
  data() {
    return {
      showUserDropdown: false
    };
  },
  computed: {
    headerTitle() {
      return this.$route.meta.headerTitle || 'SmartLearning'
    },
    isAuthenticated() {
      return isAuthenticated()
    },
    isDashboard() {
      return this.$route.name === ROUTE_DASHBOARD
    },
    isGuestOnlyRoute() {
      return this.$route.matched.some(r => r.meta.guestOnly)
    },
    showHomeIcon() {
      return !this.isDashboard && this.isAuthenticated
    },
    showUserIcon() {
      return this.isAuthenticated && !this.isGuestOnlyRoute
    },
    showLoginIcon() {
      return !this.isAuthenticated && this.isGuestOnlyRoute
    }
  },
  methods: {
    navigateToHome() {
      this.$router.push({ name: ROUTE_DASHBOARD })
    },
    navigateToLogin() {
      this.$router.push({ name: ROUTE_LOGIN })
    },
    toggleDropdown() {
      this.showUserDropdown = !this.showUserDropdown
    }
  },
  watch: {
    $route() {
      this.showUserDropdown = false
    }
  },
  components: {
    HomeIcon,
    UserIcon,
    LoginIcon,
    UserDropdown
  }
}
</script>


<style scoped>
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: var(--primary-color);
  padding: 0 2rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  height: 75px;
}

.home-section {
  width: 5rem; 
}

.user-section {
    right: 2rem;
    position: absolute;
}

.icon {
    width: 28px;
    height: 28px;
}

.app-name {
  white-space: nowrap;
}

button {
    width: fit-content;
    padding: .3rem;
    background-color: transparent;
    border: none;
}

@media (max-width: 600px) {
  .app-name {
    font-size: 26px;
  }
}
</style>
