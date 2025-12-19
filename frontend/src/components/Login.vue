<template>
    <form class="h-100 d-flex flex-column align-items-center justify-content-center">
        <div class="d-flex flex-column gap-3">
            <label for="login-userinfo">Nutzername/E-Mail-Adresse</label>
            <input type="text" id="login-userinfo" />

            <div class="mt-3">
                <PasswordInput label="Passwort" />
            </div>
        </div>
            
        <button class="mt-5 primary">Einloggen</button>
    </form>
</template>

<script>
    import PasswordInput from '@/components/PasswordInput.vue';

    export default {
        name: 'Login',
        components: {
            PasswordInput
        }
    };
</script>