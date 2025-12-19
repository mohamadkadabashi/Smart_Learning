<template>
    <form class="h-100 d-flex flex-column align-items-center justify-content-center">
        <div class="d-flex flex-column gap-2">
            <label for="reg-username">Nutzername</label>
            <input type="text" id="reg-username" />

            <label for="reg-email" class="mt-3">E-Mail-Adresse</label>
            <input type="email" id="reg-email" />

            <label for="reg-pw" class="mt-3">Passwort</label>
            <input type="password" id="reg-pw" />

            <label for="reg-pw-confirm" class="mt-3">Passwort wiederholen</label>
            <input type="password" id="reg-pw-confirm" />
        </div>

        <button class="primary mt-5">Registrieren</button>
    </form>
</template>

<script>
export default {
  name: 'Registration'
};
</script>