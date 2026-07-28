<script setup>
import { Activity, ArrowUpRight, BrainCircuit, ServerCog } from 'lucide-vue-next'
import PublicLayout from '../layouts/PublicLayout.vue'
</script>

<template>
  <PublicLayout>
    <section class="about-hero">
      <div class="about-portrait"><img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1400&q=85" alt="数据中心服务器机柜" /></div>
      <div class="about-intro"><p class="eyebrow dark"><span></span> About Bamboo</p><h1>你好，<br />我是 Bamboo。</h1><p>一名专注 LLMOps、智能可观测性与云原生平台工程的 AI 运维工程师，让模型在生产环境里稳定、透明、可控。</p></div>
    </section>
    <section class="about-copy page-width">
      <div><span class="section-index">01</span><h2>关于这份<br />“智维日志”</h2></div>
      <div class="prose"><p>Bamboo 的智维日志记录 AI 系统进入生产环境后的另一半工作：容量、延迟、成本、可观测性，以及凌晨两点真正会触发的那些告警。</p><p>这里没有脱离场景的工具清单。每篇实践尽量从问题和证据出发，说明架构选择、失败路径、自动化边界与最终结果，并附上可复用的指标或操作方法。</p><p>目标很简单：让复杂系统保持可理解，让每次故障都推动平台向前一步。</p></div>
    </section>
    <section class="interests page-width"><article><BrainCircuit /><strong>LLMOps</strong><p>模型网关、评估、Tracing 与成本治理。</p></article><article><ServerCog /><strong>平台工程</strong><p>Kubernetes、GPU 调度与交付自动化。</p></article><article><Activity /><strong>可靠性</strong><p>SLO、智能告警与故障响应。</p></article></section>
    <section class="contact-band"><div class="page-width"><p>讨论生产环境里的真实问题。</p><a href="mailto:hello@aiopslab.dev">hello@aiopslab.dev <ArrowUpRight :size="22" /></a></div></section>
  </PublicLayout>
</template>
