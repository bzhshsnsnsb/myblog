<template>
  <footer class="site-footer">
    <div class="site-footer__inner">
      <div><strong>Bamboo</strong><p>把模型变成服务，把告警变成答案。</p></div>
      <div class="footer-links">
        <router-link to="/essays">随笔</router-link>
        <router-link to="/tools">工具</router-link>
        <router-link to="/about">关于作者</router-link>
        <router-link to="/login">管理入口</router-link>
      </div>
      <p class="copyright">© {{ new Date().getFullYear() }} Bamboo</p>
    </div>
  </footer>
</template>
