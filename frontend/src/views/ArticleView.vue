<script setup>
import MarkdownIt from 'markdown-it'
import { ArrowLeft, Clock, MessageCircle } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'
import LoadingState from '../components/LoadingState.vue'
import PublicLayout from '../layouts/PublicLayout.vue'
import { formatDate, readingTime } from '../utils'

const route = useRoute()
const article = ref(null)
const loading = ref(true)
const submitting = ref(false)
const form = ref({ author: '', email: '', content: '' })
const md = new MarkdownIt({ html: false, linkify: true, typographer: true })
const rendered = computed(() => md.render(article.value?.content || ''))

onMounted(async () => {
  try { article.value = (await api.get(`/articles/${route.params.slug}`)).data }
  finally { loading.value = false }
})

const submitComment = async () => {
  submitting.value = true
  try {
    const { data } = await api.post(`/articles/${route.params.slug}/comments`, form.value)
    article.value.comments.push(data)
    form.value = { author: '', email: '', content: '' }
    ElMessage.success('留言已发布')
  } catch (error) { ElMessage.error(error.response?.data?.detail || '请检查留言内容') }
  finally { submitting.value = false }
}
</script>

<template>
  <PublicLayout>
    <LoadingState v-if="loading" />
    <article v-else-if="article" class="article-page">
      <header class="article-head page-width">
        <router-link to="/essays" class="back-link"><ArrowLeft :size="17" /> 返回随笔</router-link>
        <div class="article-head__meta"><span>{{ article.category.name }}</span><time>{{ formatDate(article.published_at, true) }}</time></div>
        <h1>{{ article.title }}</h1>
        <p>{{ article.excerpt }}</p>
        <div class="read-data"><span><Clock :size="16" /> {{ readingTime(article.content) }} 分钟阅读</span><span><MessageCircle :size="16" /> {{ article.comments.length }} 条留言</span></div>
      </header>
      <div class="article-cover"><img :src="article.cover" :alt="article.title" /></div>
      <div class="article-content" v-html="rendered"></div>
      <footer class="article-end">
        <span>写于 {{ formatDate(article.published_at, true) }}</span>
        <div><router-link v-for="tag in article.tags" :key="tag.id" :to="{ path: '/essays', query: { tag: tag.slug } }"># {{ tag.name }}</router-link></div>
      </footer>
      <section class="comments-section">
        <div class="comments-inner">
          <div class="comments-list"><p class="eyebrow dark"><span></span> Conversation</p><h2>留言 {{ article.comments.length }}</h2>
            <article v-for="comment in article.comments" :key="comment.id" class="comment"><strong>{{ comment.author.slice(0, 1) }}</strong><div><p>{{ comment.author }} <time>{{ formatDate(comment.created_at) }}</time></p><span>{{ comment.content }}</span></div></article>
            <p v-if="!article.comments.length" class="empty-copy">还没有留言，来写下第一条吧。</p>
          </div>
          <form class="comment-form" @submit.prevent="submitComment"><h3>留下想法</h3><div class="form-pair"><el-input v-model="form.author" required placeholder="你的称呼" maxlength="40" /><el-input v-model="form.email" required type="email" placeholder="邮箱（不会公开）" /></div><el-input v-model="form.content" required type="textarea" :rows="5" maxlength="500" show-word-limit placeholder="写下你的想法…" /><el-button native-type="submit" :loading="submitting" color="#cf4d35">发布留言</el-button></form>
        </div>
      </section>
    </article>
  </PublicLayout>
</template>
