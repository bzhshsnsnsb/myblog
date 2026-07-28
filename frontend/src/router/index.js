import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', component: () => import('../views/HomeView.vue') },
  { path: '/article/:slug', component: () => import('../views/ArticleView.vue') },
  { path: '/essays', alias: '/archive', component: () => import('../views/ArchiveView.vue') },
  { path: '/tools', component: () => import('../views/ToolsView.vue') },
  { path: '/tools/:category', component: () => import('../views/ToolsView.vue') },
  { path: '/about', component: () => import('../views/AboutView.vue') },
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  {
    path: '/admin', component: () => import('../layouts/AdminLayout.vue'), meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('../views/admin/DashboardView.vue') },
      { path: 'articles', component: () => import('../views/admin/ArticlesView.vue') },
      { path: 'articles/new', component: () => import('../views/admin/EditorView.vue') },
      { path: 'articles/:id/edit', component: () => import('../views/admin/EditorView.vue') },
      { path: 'comments', component: () => import('../views/admin/CommentsView.vue') },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes, scrollBehavior: () => ({ top: 0 }) })

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return '/login'
  if (to.meta.guest && auth.isAuthenticated) return '/admin'
})

export default router
