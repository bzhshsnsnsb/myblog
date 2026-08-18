<script setup>
import { Eye, EyeOff, Trash2 } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../../api'
import { formatDate } from '../../utils'

const comments = ref([])
const loading = ref(true)
const load = async () => { try { comments.value = (await api.get('/admin/comments')).data } finally { loading.value = false } }
const toggle = async (comment) => { const { data } = await api.patch(`/admin/comments/${comment.id}`); Object.assign(comment, data); ElMessage.success(data.approved ? '留言已显示' : '留言已隐藏') }
const remove = async (comment) => { try { await ElMessageBox.confirm('确定永久删除这条留言吗？', '删除留言', { type: 'warning' }); await api.delete(`/admin/comments/${comment.id}`); comments.value = comments.value.filter((item) => item.id !== comment.id); ElMessage.success('留言已删除') } catch (error) { if (error !== 'cancel') ElMessage.error('删除失败') } }
onMounted(load)
</script>

<template>
  <section class="admin-page"><div class="admin-title"><div><p>互动管理</p><h1>读者留言</h1></div></div><section v-loading="loading" class="admin-panel comment-admin-list"><article v-for="comment in comments" :key="comment.id"><strong>{{ comment.author.slice(0, 1) }}</strong><div><div><b>{{ comment.author }}</b><span>{{ comment.email }}</span><time>{{ formatDate(comment.created_at, true) }}</time></div><p>{{ comment.content }}</p></div><el-tag :type="comment.approved ? 'success' : 'info'" effect="plain">{{ comment.approved ? '显示中' : '已隐藏' }}</el-tag><div class="row-actions"><button :title="comment.approved ? '隐藏' : '显示'" @click="toggle(comment)"><EyeOff v-if="comment.approved" :size="18" /><Eye v-else :size="18" /></button><button title="删除" @click="remove(comment)"><Trash2 :size="18" /></button></div></article><el-empty v-if="!loading && !comments.length" description="还没有读者留言" /></section></section>
</template>

