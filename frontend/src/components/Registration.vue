<template>
    <form class="h-100 d-flex flex-column align-items-center justify-content-center">
        <div class="d-flex flex-column gap-2">
            <label for="reg-username">Nutzername</label>
            <input type="text" id="reg-username" />

            <label for="reg-email" class="mt-3">E-Mail-Adresse</label>
            <input type="email" id="reg-email" />

            <div class="mt-3">
                <PasswordInput label="Passwort" />
            </div>

            <div class="mt-3">
                <PasswordInput label="Passwort wiederholen" />
            </div>
        </div>

        <button class="primary mt-5">Registrieren</button>
    </form>
</template>

<script>
    import PasswordInput from '@/components/PasswordInput.vue';

    export default {
        name: 'Registration',
        components: {
            PasswordInput
        }
    };
</script>