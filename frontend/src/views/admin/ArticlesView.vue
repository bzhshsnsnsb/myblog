<script setup>
import { Edit3, Eye, Plus, Search, Trash2 } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../../api'
import { formatDate } from '../../utils'

const articles = ref([])
const keyword = ref('')
const loading = ref(true)
const filtered = computed(() => articles.value.filter((item) => item.title.toLowerCase().includes(keyword.value.toLowerCase())))
const load = async () => { loading.value = true; try { articles.value = (await api.get('/admin/articles')).data } finally { loading.value = false } }
const remove = async (article) => {
  try {
    await ElMessageBox.confirm(`确定删除《${article.title}》吗？此操作不可恢复。`, '删除文章', { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' })
    await api.delete(`/admin/articles/${article.id}`)
    articles.value = articles.value.filter((item) => item.id !== article.id)
    ElMessage.success('文章已删除')
  } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') }
}
onMounted(load)
</script>

<template>
  <section class="admin-page"><div class="admin-title"><div><p>内容管理</p><h1>文章</h1></div><router-link to="/admin/articles/new" class="primary-action"><Plus :size="18" /> 新建文章</router-link></div>
    <section class="admin-panel"><div class="table-tools"><div class="admin-search"><Search :size="18" /><input v-model="keyword" placeholder="搜索文章标题" /></div><span>共 {{ filtered.length }} 篇</span></div>
      <el-table v-loading="loading" :data="filtered" class="article-table">
        <el-table-column label="文章" min-width="340"><template #default="{ row }"><div class="table-article"><img :src="row.cover" :alt="row.title" /><div><strong>{{ row.title }}</strong><span>{{ row.excerpt }}</span></div></div></template></el-table-column>
        <el-table-column prop="category.name" label="分类" width="100" />
        <el-table-column label="状态" width="100"><template #default="{ row }"><el-tag :type="row.published ? 'success' : 'info'" effect="plain">{{ row.published ? '已发布' : '草稿' }}</el-tag></template></el-table-column>
        <el-table-column label="发布日期" width="120"><template #default="{ row }">{{ formatDate(row.published_at) }}</template></el-table-column>
        <el-table-column label="操作" width="130" fixed="right"><template #default="{ row }"><div class="row-actions"><router-link v-if="row.published" :to="`/article/${row.slug}`" title="查看"><Eye :size="17" /></router-link><router-link :to="`/admin/articles/${row.id}/edit`" title="编辑"><Edit3 :size="17" /></router-link><button title="删除" @click="remove(row)"><Trash2 :size="17" /></button></div></template></el-table-column>
      </el-table>
    </section>
  </section>
</template>

