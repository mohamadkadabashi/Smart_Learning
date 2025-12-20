<template class="h-100">
    <div>
        <TopBar />

        <div class="main-content container-fluid py-5 d-flex justify-content-center h-100">
            <TabContainer :tabs="['Login', 'Registrieren']">
                <template #tab-0>
                    <Login />
                </template>

                <template #tab-1>
                    <Registration />
                </template>
            </TabContainer>
        </div>
    </div>
</template>

<script>
    import TopBar from '@/components/TopBar.vue';
    import TabContainer from '@/components/TabContainer.vue';
    import Login from '@/components/Login.vue';
    import Registration from '@/components/Registration.vue';

    export default {
        components: { TopBar, TabContainer, Login, Registration }
    }
</script>

<style scoped>
    .main-content {
        margin-top: 50px;
    }
</style>