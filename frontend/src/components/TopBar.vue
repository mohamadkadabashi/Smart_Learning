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
    import HomeIcon from '@/../public/assets/images/home.svg';
    import UserIcon from '@/../public/assets/images/person-sharp.svg';
    import LoginIcon from '@/../public/assets/images/log-in.svg';
    import UserDropdown from '@/components/UserDropdown.vue';
    import { isAuthenticated } from '@/services/user.js';

    const ROUTE_HOME = 'Home';
    const ROUTE_LOGIN = 'Login/Registrierung';

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
            isHomeRoute() {
                return this.$route.name === ROUTE_HOME;
            },
            isLoginRoute() {
                return this.$route.name === ROUTE_LOGIN;
            },
            showHomeIcon() {
                return !this.isHomeRoute;
            },
            showUserIcon() {
                return !this.isLoginRoute && isAuthenticated();
            },
            showLoginIcon() {
                return this.isHomeRoute && !isAuthenticated();
            }
        },
        methods: {
            navigateToHome() {
                this.$router.push({ name: ROUTE_HOME });
            },
            navigateToLogin() {
                this.$router.push({ name: ROUTE_LOGIN });
            },
            toggleDropdown() {
                this.showUserDropdown = !this.showUserDropdown;
            }
        },
        components: {
            HomeIcon,
            UserIcon,
            LoginIcon,
            UserDropdown
        },
        watch: {
            $route() {
                this.showUserDropdown = false
            }
        }
    };
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
