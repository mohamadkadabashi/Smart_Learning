<template>
    <header class="top-bar d-flex align-items-center">
        <div class="home-section">
            <div role="button" 
                 v-if="showHomeIcon" 
                 @click="navigateToHome" 
                 style="cursor: pointer;"
                 aria-label="Zur�ck zur Startseite">
                <HomeIcon role="presentation" />
            </div>
        </div>
        <h1 class="app-name">{{ headerTitle }}</h1>

        <div class="user-section">
            <div role="button" 
                 v-if="showUserIcon" 
                 style="cursor: pointer;"
                 aria-label="�ffne die Nutzereinstellungen">
                <UserIcon role="presentation" />
            </div>
        </div>
    </header>
</template>

<script>
    import HomeIcon from '@/../public/assets/images/home.svg';
    import UserIcon from '@/../public/assets/images/person-sharp.svg';

    export default {
        name: 'TopBar',
        computed: {
            headerTitle() {
                return this.$route.meta.headerTitle || 'SmartLearning'
            },
            showUserIcon() {
                return this.$route.name !== 'Login/Registrierung';
            },
            showHomeIcon() {
                return this.showUserIcon && this.$route.name !== 'Home';
            }
        },
        methods: {
            navigateToHome() {
                this.$router.push({ name: 'Home' });
            }
        },
        components: {
            HomeIcon,
            UserIcon
        },
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

@media (max-width: 600px) {
  .app-name {
    font-size: 26px;
  }
}
</style>
