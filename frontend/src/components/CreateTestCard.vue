<template>
    <div class="small-card d-flex flex-column align-items-center">
        <div class="title">
            Neuen Test erstellen
        </div>

        <button class="primary create-btn" 
                type="button" 
                @click="navigateToCreateTestForm">
            <PlusIcon class="plus-icon" />
        </button>
    </div>
</template>

<script>
    import PlusIcon from '@/../public/assets/images/plus-icon.svg';

    export default {
        name: "CreateTestCard",

        components: {
            PlusIcon
        },

        methods: {
            navigateToCreateTestForm() {
                this.$router.push({ path: '/create' });
            }
        }
    };
</script>

<style scoped>
    .title {
        font-size: 22px;
        margin-bottom: 16px;
    }

</style>
