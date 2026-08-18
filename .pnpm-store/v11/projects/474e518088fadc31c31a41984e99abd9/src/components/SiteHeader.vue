<script setup>
import { Menu, Search, X } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const mobileOpen = ref(false)
const searchOpen = ref(false)
const keyword = ref('')
const router = useRouter()

const submitSearch = () => {
  if (!keyword.value.trim()) return
  router.push({ path: '/essays', query: { search: keyword.value.trim() } })
  searchOpen.value = false
  mobileOpen.value = false
}
</script>

<template>
  <header class="site-header">
    <div class="site-header__inner">
      <router-link to="/" class="brand" aria-label="Bamboo 首页">
        <span class="brand__mark">B</span>
        <span><strong>Bamboo</strong><small>AI 运维日志</small></span>
      </router-link>

      <nav :class="['main-nav', { 'is-open': mobileOpen }]" aria-label="主导航">
        <router-link to="/" @click="mobileOpen = false">首页</router-link>
        <router-link to="/essays" @click="mobileOpen = false">随笔</router-link>
        <router-link to="/tools" @click="mobileOpen = false">工具</router-link>
        <router-link to="/about" @click="mobileOpen = false">关于</router-link>
      </nav>

      <div class="header-actions">
        <button class="icon-btn" type="button" title="搜索" @click="searchOpen = !searchOpen"><Search :size="19" /></button>
        <button class="icon-btn menu-btn" type="button" title="菜单" @click="mobileOpen = !mobileOpen">
          <X v-if="mobileOpen" :size="21" /><Menu v-else :size="21" />
        </button>
      </div>

      <form v-if="searchOpen" class="search-panel" @submit.prevent="submitSearch">
        <input v-model="keyword" autofocus aria-label="搜索文章" placeholder="输入关键词，按回车搜索" />
        <button class="icon-btn" type="submit" title="提交搜索"><Search :size="19" /></button>
      </form>
    </div>
  </header>
</template>
