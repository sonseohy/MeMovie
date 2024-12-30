<template>
  <header>
    <Navbar  />
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
</script>

<style scoped>
header {
  margin: 30px;
}
</style>
