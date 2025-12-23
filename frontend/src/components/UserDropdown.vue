<template>
    <div class="dropdown" role="menu">
        <button role="menuitem" class="dropdown-btn" aria-label="Zu den Nutzereinstellungen" disabled>
            <SettingsIcon /> 
            <span>Einstellungen</span>
        </button>

        <div role="menuitem">
            <ToggleSwitch v-model="darkmode"
                          title="Toggle Darkmode"
                          disabled="true"
                          @change="toggleDarkmode" />
            <span>Darkmode</span>
        </div>

        <button role="menuitem" class="dropdown-btn" aria-label="Zur Hilfeseite der Anwendung" disabled>
            <HelpIcon /> 
            <span>Hilfe</span>
        </button>

        <button role="menuitem" class="dropdown-btn" @click="logout">
            <LogOutIcon /> 
            <span>Abmelden</span>
        </button>
    </div>
</template>


<script>
    import SettingsIcon from '@/../public/assets/images/settings.svg';
    import LogOutIcon from '@/../public/assets/images/log-out.svg';
    import HelpIcon from '@/../public/assets/images/help.svg';
    import ToggleSwitch from '@/components/ToggleSwitch.vue';

    export default {
        name: 'UserDropdown',
        data() {
            return {
                darkmode: false
            };
        },
        methods: {
            toggleDarkmode() {
                document.body.classList.toggle('dark', this.darkmode);
            },
            logout() {
                this.$router.push({ name: 'Login/Registrierung' });
            }
        },
        components: {
            SettingsIcon,
            LogOutIcon,
            HelpIcon,
            ToggleSwitch
        }
    };
</script>


<style scoped>
    .dropdown {
        position: absolute;
        right: 0;
        top: 75px;
        width: fit-content;
        border-bottom-left-radius: 30px;
        border-top-left-radius: 30px;
        border: 3px solid #B5B2B2;
        overflow: hidden;
    }

    [role=menuitem] {
        width: 100%;
        background: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        gap: 10px;
        border: none;
        border-bottom: 1px solid #B5B2B2;
    }

    .dropdown-btn {
        cursor: pointer;
    }

        .dropdown-btn:hover:not(:disabled) {
            background: #F3F3F3;
        }

        .dropdown-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
</style>