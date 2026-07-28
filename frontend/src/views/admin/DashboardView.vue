<script setup>
import { BookOpen, FolderOpen, MessageSquare, Plus, Tags } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import api from '../../api'
import { formatDate } from '../../utils'

const stats = ref({ articles: 0, categories: 0, tags: 0, comments: 0 })
const articles = ref([])
onMounted(async () => {
  const [statsResponse, articleResponse] = await Promise.all([api.get('/stats'), api.get('/admin/articles')])
  stats.value = statsResponse.data
  articles.value = articleResponse.data.slice(0, 5)
})
</script>

<template>
  <section class="admin-page">
    <div class="admin-title"><div><p>工作台</p><h1>Bamboo，继续写点什么。</h1></div><router-link to="/admin/articles/new" class="primary-action"><Plus :size="18" /> 新建文章</router-link></div>
    <div class="stat-grid"><article><div><span>已发布文章</span><strong>{{ stats.articles }}</strong></div><BookOpen /></article><article><div><span>文章分类</span><strong>{{ stats.categories }}</strong></div><FolderOpen /></article><article><div><span>内容标签</span><strong>{{ stats.tags }}</strong></div><Tags /></article><article><div><span>读者留言</span><strong>{{ stats.comments }}</strong></div><MessageSquare /></article></div>
    <section class="admin-panel"><div class="panel-head"><div><h2>最近编辑</h2><p>按最后更新时间排列</p></div><router-link to="/admin/articles">全部文章</router-link></div><div class="recent-table"><div v-for="article in articles" :key="article.id" class="recent-row"><img :src="article.cover" :alt="article.title" /><div><strong>{{ article.title }}</strong><span>{{ article.category.name }} · {{ formatDate(article.published_at) }}</span></div><el-tag :type="article.published ? 'success' : 'info'" effect="plain">{{ article.published ? '已发布' : '草稿' }}</el-tag><router-link :to="`/admin/articles/${article.id}/edit`">编辑</router-link></div></div></section>
  </section>
</template>
