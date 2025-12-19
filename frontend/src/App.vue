<template>
  <div id="app" class="h-100">
    <transition name="fade" mode="out-in">
      <router-view class="h-100"/>
    </transition>
  </div>


</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>


