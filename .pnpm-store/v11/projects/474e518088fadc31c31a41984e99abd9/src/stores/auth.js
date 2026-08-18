import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({ token: localStorage.getItem('blog_token') || '', username: localStorage.getItem('blog_user') || '' }),
  getters: { isAuthenticated: (state) => Boolean(state.token) },
  actions: {
    async login(credentials) {
      const { data } = await api.post('/auth/login', credentials)
      this.token = data.token
      this.username = data.username
      localStorage.setItem('blog_token', data.token)
      localStorage.setItem('blog_user', data.username)
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('blog_token')
      localStorage.removeItem('blog_user')
    },
  },
})

