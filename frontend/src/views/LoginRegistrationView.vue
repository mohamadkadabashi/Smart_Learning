<template class="h-100">
    <div>
        <div class="main-content container-fluid py-5 d-flex justify-content-center flex-wrap h-100">
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
    import TabContainer from '@/components/TabContainer.vue';
    import Login from '@/components/Login.vue';
    import Registration from '@/components/Registration.vue';

    export default {
        components: { TabContainer, Login, Registration }
    }
</script>