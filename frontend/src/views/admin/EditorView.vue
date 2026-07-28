<script setup>
import MarkdownIt from 'markdown-it'
import { ArrowLeft, Eye, Save } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../../api'

const route = useRoute()
const router = useRouter()
const saving = ref(false)
const activeTab = ref('write')
const isEdit = computed(() => Boolean(route.params.id))
const form = ref({ title: '', slug: '', excerpt: '', content: '# 开始记录\n\n描述问题、证据、决策与结果…', cover: '', category: 'AI运维', tags: [], featured: false, published: true })
const md = new MarkdownIt({ html: false, linkify: true, typographer: true })
const preview = computed(() => md.render(form.value.content))

onMounted(async () => {
  if (!isEdit.value) return
  let detail
  try { detail = (await api.get(`/admin/articles/${route.params.id}`)).data }
  catch { return router.push('/admin/articles') }
  form.value = { title: detail.title, slug: detail.slug, excerpt: detail.excerpt, content: detail.content || '', cover: detail.cover, category: detail.category.name, tags: detail.tags.map((tag) => tag.name), featured: detail.featured, published: detail.published }
})

const generateSlug = () => { if (!form.value.slug) form.value.slug = `post-${Date.now().toString().slice(-8)}` }
const save = async () => {
  generateSlug()
  saving.value = true
  try {
    if (isEdit.value) await api.put(`/admin/articles/${route.params.id}`, form.value)
    else await api.post('/admin/articles', form.value)
    ElMessage.success('文章已保存')
    router.push('/admin/articles')
  } catch (error) { ElMessage.error(error.response?.data?.detail || '请检查必填内容') }
  finally { saving.value = false }
}
</script>

<template>
  <section class="editor-page"><header class="editor-header"><div><router-link to="/admin/articles" class="icon-btn" title="返回"><ArrowLeft :size="20" /></router-link><div><p>{{ isEdit ? '编辑文章' : '新建文章' }}</p><span>{{ form.title || '未命名文章' }}</span></div></div><div><el-switch v-model="form.published" inline-prompt active-text="发布" inactive-text="草稿" /><button class="primary-action" @click="save"><Save :size="17" /> {{ saving ? '保存中' : '保存文章' }}</button></div></header>
    <div class="editor-layout">
      <section class="editor-main"><input v-model="form.title" class="title-input" placeholder="输入文章标题" @blur="generateSlug" /><textarea v-model="form.excerpt" class="excerpt-input" maxlength="280" placeholder="写一段简洁的文章摘要…"></textarea><div class="editor-tabs"><button :class="{ active: activeTab === 'write' }" @click="activeTab = 'write'">Markdown</button><button :class="{ active: activeTab === 'preview' }" @click="activeTab = 'preview'"><Eye :size="16" /> 预览</button></div><textarea v-if="activeTab === 'write'" v-model="form.content" class="content-editor" spellcheck="false"></textarea><article v-else class="article-content editor-preview" v-html="preview"></article></section>
      <aside class="editor-aside"><h3>文章设置</h3><label>URL 别名<el-input v-model="form.slug" placeholder="llm-observability" /></label><label>分类<el-input v-model="form.category" placeholder="AI运维" /></label><label>标签<el-select v-model="form.tags" multiple filterable allow-create default-first-option placeholder="输入后回车"><el-option v-for="tag in form.tags" :key="tag" :label="tag" :value="tag" /></el-select></label><label>封面图片 URL<el-input v-model="form.cover" type="textarea" :rows="3" /></label><div v-if="form.cover" class="cover-preview"><img :src="form.cover" alt="封面预览" /></div><label class="switch-label"><span><strong>首页精选</strong><small>作为首页主视觉文章</small></span><el-switch v-model="form.featured" /></label></aside>
    </div>
  </section>
</template>
