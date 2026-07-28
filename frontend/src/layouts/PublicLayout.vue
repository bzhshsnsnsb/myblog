<template>
  <div class="public-shell">
    <SiteHeader />
    <main><slot /></main>
    <SiteFooter />
  </div>
</template>

<script setup>
import SiteHeader from '../components/SiteHeader.vue'
import SiteFooter from '../components/SiteFooter.vue'
</script>

