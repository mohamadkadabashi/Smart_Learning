<template>
    <div id="app">
        <TopBar />
        <transition name="fade" mode="out-in">
            <router-view class="full-height" />
        </transition>
    </div>
</template>

<script>
    import TopBar from '@/components/TopBar.vue';
    export default {
        components: { TopBar }
    }
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.full-height {
    height: calc(100vh - 80px);
    position: absolute;
    bottom: 0;
    width: 100%;
    overflow: auto;
}
</style>


