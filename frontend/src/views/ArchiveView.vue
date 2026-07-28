<script setup>
import { Search, X } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import LoadingState from '../components/LoadingState.vue'
import PublicLayout from '../layouts/PublicLayout.vue'
import { formatDate } from '../utils'

const route = useRoute()
const router = useRouter()
const articles = ref([])
const categories = ref([])
const loading = ref(true)
const error = ref('')
const search = ref(route.query.search || '')
const activeCategory = computed(() => route.query.category || '')

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/articles', { params: { page_size: 50, category: activeCategory.value || undefined, tag: route.query.tag || undefined, search: route.query.search || undefined } })
    articles.value = data.items
  } catch {
    articles.value = []
    error.value = '暂时无法获取随笔内容，请检查服务后重试。'
  } finally { loading.value = false }
}

const submit = () => router.push({ query: { ...route.query, search: search.value.trim() || undefined } })
const clearSearch = () => {
  search.value = ''
  submit()
}
const selectCategory = (slug) => router.push({ query: { ...route.query, category: slug || undefined } })

onMounted(async () => {
  await Promise.allSettled([
    api.get('/categories').then(({ data }) => { categories.value = data }),
    load(),
  ])
})
watch(() => route.query, load, { deep: true })
watch(() => route.query.search, (value) => { search.value = value || '' })
</script>

<template>
  <PublicLayout>
    <section class="archive-hero page-width">
      <p class="eyebrow dark"><span></span> Essays</p>
      <div><h1>随笔</h1><p>记录 LLMOps、自动化与可靠性工程实践。</p></div>
      <form class="archive-search" @submit.prevent="submit"><button type="submit" title="搜索" aria-label="搜索"><Search :size="19" /></button><input v-model="search" placeholder="搜索标题或摘要" aria-label="搜索文章" @keydown.enter.prevent="submit" /><button v-if="search" type="button" title="清除" aria-label="清除搜索" @click="clearSearch"><X :size="17" /></button></form>
    </section>
    <section class="archive-body page-width">
      <div class="filter-row">
        <button :class="{ active: !activeCategory }" @click="selectCategory('')">全部</button>
        <button v-for="category in categories" :key="category.id" :class="{ active: activeCategory === category.slug }" @click="selectCategory(category.slug)">{{ category.name }} <span>{{ category.count }}</span></button>
      </div>
      <LoadingState v-if="loading" />
      <el-result v-else-if="error" icon="error" title="加载失败" :sub-title="error"><template #extra><el-button @click="load">重新加载</el-button></template></el-result>
      <div v-else-if="articles.length" class="archive-list">
        <article v-for="article in articles" :key="article.id">
          <time>{{ formatDate(article.published_at) }}</time>
          <div><p>{{ article.category.name }}</p><h2><router-link :to="`/article/${article.slug}`">{{ article.title }}</router-link></h2><span>{{ article.excerpt }}</span></div>
          <img :src="article.cover" :alt="article.title" loading="lazy" />
        </article>
      </div>
      <el-empty v-else description="没有找到相关文章" />
    </section>
  </PublicLayout>
</template>
