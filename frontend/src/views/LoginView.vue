<script setup>
import { ArrowLeft, LockKeyhole } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const loading = ref(false)
const form = ref({ username: 'admin', password: 'admin123' })

const login = async () => {
  loading.value = true
  try { await auth.login(form.value); router.push('/admin') }
  catch (error) { ElMessage.error(error.response?.data?.detail || '登录失败') }
  finally { loading.value = false }
}
</script>

<template>
  <main class="login-page">
    <router-link to="/" class="login-back"><ArrowLeft :size="17" /> 返回博客</router-link>
    <section class="login-panel">
      <div class="login-symbol"><LockKeyhole :size="24" /></div><p class="eyebrow dark"><span></span> Studio access</p><h1>内容工作台</h1><p>登录后管理文章与读者留言。</p>
      <form @submit.prevent="login"><label>用户名<el-input v-model="form.username" size="large" /></label><label>密码<el-input v-model="form.password" type="password" show-password size="large" /></label><el-button native-type="submit" :loading="loading" color="#cf4d35" size="large">进入工作台</el-button></form>
      <small>演示账号：admin / admin123</small>
    </section>
    <div class="login-image"><img src="https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1600&q=85" alt="书桌与笔记本" /></div>
  </main>
</template>

