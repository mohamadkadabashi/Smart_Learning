<template>
    <div class="dropdown">
        <button class="dropdown-btn" aria-label="Zu den Nutzereinstellungen" disabled>
            <SettingsIcon /> 
            <span>Einstellungen</span>
        </button>

        <div class="dropdown-btn toggle">
            <ToggleSwitch v-model="darkmode"
                          title="Toggle Darkmode"
                          @change="toggleDarkmode"
                          :disabled="true" />
            <span style="opacity: 0.5;">Darkmode</span>
        </div>

        <button class="dropdown-btn" aria-label="Zur Hilfeseite der Anwendung" disabled>
            <HelpIcon /> 
            <span>Hilfe</span>
        </button>

        <button class="dropdown-btn" @click="logout">
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
    import { logout } from '@/services/auth.js';

    export default {
        name: 'UserDropdown',
        data() {
            return {
                darkmode: document.body.classList.contains('dark')
            };
        },
        methods: {
            toggleDarkmode() {
                document.body.classList.toggle('dark', this.darkmode)
            },
            logout() {
                logout();
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
        z-index: 1;
    }

    .dropdown-btn {
        width: 100%;
        background: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        gap: 10px;
        border: none;
    }

    .dropdown-btn:not(:last-child) {
        border-bottom: 1px solid #B5B2B2;
    }

    .dropdown-btn:not(.toggle){
        cursor: pointer;
    }

        .dropdown-btn:hover:not(:disabled) {
            background: #F3F3F3;
        }

        .dropdown-btn:disabled svg,
        .dropdown-btn:disabled span {
            opacity: 0.5;
            cursor: not-allowed;
        }
</style>