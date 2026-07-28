<script setup>
import { Activity, ArrowLeft, Boxes, ChevronRight, CloudCog, Container, Copy, Database, FileSearch, FolderOpen, GitBranch, HardDrive, KeyRound, Search, ServerCog, ShieldCheck, Timer, Users, Wifi } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import PublicLayout from '../layouts/PublicLayout.vue'
import { toolCategories } from '../data/opsTools'

const route = useRoute()
const keyword = ref('')
const iconMap = { users: Users, logs: FileSearch, network: Wifi, database: Database, redis: Boxes, disk: HardDrive, container: Container, cloud: CloudCog, proxy: ServerCog, shield: ShieldCheck, key: KeyRound, git: GitBranch, timer: Timer, activity: Activity, server: ServerCog }
const activeCategory = computed(() => toolCategories.find((item) => item.slug === route.params.category))
const filteredCommands = computed(() => {
  if (!activeCategory.value) return []
  const value = keyword.value.trim().toLowerCase()
  if (!value) return activeCategory.value.commands
  return activeCategory.value.commands.filter((item) => `${item.name} ${item.code} ${item.description}`.toLowerCase().includes(value))
})

watch(() => route.params.category, () => { keyword.value = '' })

const copyCommand = async (code) => {
  await navigator.clipboard.writeText(code)
  ElMessage.success('命令已复制')
}
</script>

<template>
  <PublicLayout>
    <template v-if="!activeCategory">
      <section class="tools-directory">
        <div class="page-width">
          <header class="directory-heading"><span><FolderOpen :size="30" /></span><div><h1>分类归档</h1><p>按运维主题索引的常用命令与排查工具</p></div></header>
          <div class="ops-category-grid">
            <router-link v-for="category in toolCategories" :key="category.slug" :to="`/tools/${category.slug}`" class="ops-category-card">
              <span class="category-tile" :style="{ backgroundColor: category.accent }"><component :is="iconMap[category.icon]" :size="25" /></span>
              <div><h2>{{ category.name }}</h2><p>探索分类 <ChevronRight :size="15" /></p></div>
              <small>{{ category.commands.length }}</small>
            </router-link>
          </div>
        </div>
      </section>
    </template>

    <template v-else>
      <section class="tool-detail-head page-width">
        <router-link to="/tools" class="back-link static"><ArrowLeft :size="17" /> 返回工具箱</router-link>
        <div class="tool-detail-title"><span class="ops-category-icon" :style="{ backgroundColor: activeCategory.accent }"><component :is="iconMap[activeCategory.icon]" :size="25" /></span><div><p>Operations / {{ activeCategory.slug }}</p><h1>{{ activeCategory.name }}</h1><span>{{ activeCategory.description }}</span></div></div>
        <label class="command-search"><Search :size="18" /><input v-model="keyword" placeholder="搜索名称、命令或用途" /></label>
      </section>
      <section class="ops-command-list page-width">
        <article v-for="(command, index) in filteredCommands" :key="command.code">
          <span class="command-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <div class="command-copy"><strong>{{ command.name }}</strong><p>{{ command.description }}</p><code>{{ command.code }}</code></div>
          <el-tooltip content="复制命令" placement="top"><button class="icon-btn copy-button" title="复制命令" @click="copyCommand(command.code)"><Copy :size="18" /></button></el-tooltip>
        </article>
        <el-empty v-if="!filteredCommands.length" description="没有找到匹配的命令" />
      </section>
    </template>
  </PublicLayout>
</template>
