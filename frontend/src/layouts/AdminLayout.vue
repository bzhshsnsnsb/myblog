<script setup>
import { FileText, LayoutDashboard, LogOut, MessageSquare, PanelLeftClose, PanelLeftOpen } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const collapsed = ref(false)
const auth = useAuthStore()
const router = useRouter()
const logout = () => { auth.logout(); router.push('/') }
</script>

<template>
  <div :class="['admin-shell', { collapsed }]">
    <aside class="admin-sidebar">
      <router-link to="/" class="admin-brand"><span>B</span><strong>Bamboo</strong></router-link>
      <nav>
        <router-link to="/admin" exact-active-class="active"><LayoutDashboard :size="19" /><span>概览</span></router-link>
        <router-link to="/admin/articles"><FileText :size="19" /><span>文章</span></router-link>
        <router-link to="/admin/comments"><MessageSquare :size="19" /><span>留言</span></router-link>
      </nav>
      <button class="admin-logout" @click="logout"><LogOut :size="18" /><span>退出登录</span></button>
    </aside>
    <main class="admin-main">
      <header class="admin-topbar"><button class="icon-btn" title="切换侧栏" @click="collapsed = !collapsed"><PanelLeftOpen v-if="collapsed" :size="20" /><PanelLeftClose v-else :size="20" /></button><div><span class="status-dot"></span> 内容服务正常</div><strong>Bamboo</strong></header>
      <div class="admin-content"><router-view /></div>
    </main>
  </div>
</template>
