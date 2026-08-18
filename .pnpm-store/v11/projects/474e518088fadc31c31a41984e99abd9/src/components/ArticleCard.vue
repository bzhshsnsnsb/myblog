<script setup>
import { ArrowUpRight } from 'lucide-vue-next'
import { formatDate } from '../utils'

defineProps({ article: { type: Object, required: true }, large: Boolean })
</script>

<template>
  <article :class="['article-card', { 'article-card--large': large }]">
    <router-link :to="`/article/${article.slug}`" class="article-card__image">
      <img :src="article.cover" :alt="article.title" loading="lazy" />
    </router-link>
    <div class="article-card__body">
      <div class="article-meta"><span>{{ article.category.name }}</span><time>{{ formatDate(article.published_at) }}</time></div>
      <h2><router-link :to="`/article/${article.slug}`">{{ article.title }}</router-link></h2>
      <p>{{ article.excerpt }}</p>
      <router-link :to="`/article/${article.slug}`" class="text-link">继续阅读 <ArrowUpRight :size="16" /></router-link>
    </div>
  </article>
</template>

