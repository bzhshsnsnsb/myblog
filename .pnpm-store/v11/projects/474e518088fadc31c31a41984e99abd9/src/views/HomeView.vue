<script setup>
import { ArrowDown, ArrowRight } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import api from '../api'
import ArticleCard from '../components/ArticleCard.vue'
import LoadingState from '../components/LoadingState.vue'
import PublicLayout from '../layouts/PublicLayout.vue'
import { formatDate } from '../utils'

const articles = ref([])
const categories = ref([])
const loading = ref(true)
const featured = computed(() => articles.value.find((item) => item.featured) || articles.value[0])
const recent = computed(() => articles.value.filter((item) => item.id !== featured.value?.id).slice(0, 3))

onMounted(async () => {
  try {
    const [articleResponse, categoryResponse] = await Promise.all([api.get('/articles', { params: { page_size: 8 } }), api.get('/categories')])
    articles.value = articleResponse.data.items
    categories.value = categoryResponse.data
  } finally { loading.value = false }
})
</script>

<template>
  <PublicLayout>
    <LoadingState v-if="loading" />
    <template v-else>
      <section v-if="featured" class="home-hero">
        <img :src="featured.cover" :alt="featured.title" />
        <div class="home-hero__shade"></div>
        <div class="home-hero__content page-width">
          <div class="eyebrow"><span></span> 本期精选 · {{ featured.category.name }}</div>
          <h1>{{ featured.title }}</h1>
          <p>{{ featured.excerpt }}</p>
          <router-link :to="`/article/${featured.slug}`" class="hero-link">阅读文章 <ArrowRight :size="19" /></router-link>
        </div>
        <a href="#recent" class="scroll-cue" aria-label="查看近期文章"><ArrowDown :size="18" /></a>
      </section>

      <section id="recent" class="section page-width">
        <div class="section-heading"><div><span class="section-index">01</span><h2>近期实践</h2></div><router-link to="/essays">查看全部 <ArrowRight :size="16" /></router-link></div>
        <div class="article-grid">
          <ArticleCard v-for="article in recent" :key="article.id" :article="article" />
        </div>
      </section>

      <section class="note-band">
        <div class="page-width note-band__inner">
          <div><span class="section-index">02</span><h2>让复杂系统<br />保持可理解</h2></div>
          <p>这里记录 AI 服务从实验走向生产的真实过程：指标怎样设计，告警如何收敛，Agent 在哪里有用，以及每一次故障如何成为下一次自动化的输入。</p>
        </div>
      </section>

      <section class="section page-width categories-section">
        <div class="section-heading"><div><span class="section-index">03</span><h2>按工程主题浏览</h2></div></div>
        <div class="category-list">
          <router-link v-for="(category, index) in categories" :key="category.id" :to="{ path: '/essays', query: { category: category.slug } }">
            <span>0{{ index + 1 }}</span><strong>{{ category.name }}</strong><small>{{ category.count }} 篇文章</small><ArrowRight :size="20" />
          </router-link>
        </div>
      </section>
    </template>
  </PublicLayout>
</template>
