<template>
  <div class="analysis-detail-page">
    <van-nav-bar
      title="复盘分析"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <div v-loading="loading" class="content">
      <div v-if="analysis">
        <div class="rating-card">
          <div class="rating-label">综合评价</div>
          <div class="rating-value" :class="ratingClass">{{ analysis.overall_rating }}</div>
        </div>
        
        <div class="section">
          <h2 class="section-title">亮点表现</h2>
          <div class="highlight-list">
            <div
              v-for="(item, index) in analysis.highlights"
              :key="index"
              class="highlight-item"
            >
              <van-icon name="success" color="#4caf50" />
              <span>{{ item.text }}</span>
            </div>
            <van-empty v-if="!analysis.highlights || analysis.highlights.length === 0" description="暂无明显亮点" image-size="60" />
          </div>
        </div>
        
        <div class="section">
          <h2 class="section-title">需要改进</h2>
          <div class="mistake-list">
            <div
              v-for="(item, index) in analysis.mistakes"
              :key="index"
              class="mistake-item"
            >
              <van-icon name="warning" color="#ff9800" />
              <span>{{ item.text }}</span>
            </div>
            <van-empty v-if="!analysis.mistakes || analysis.mistakes.length === 0" description="表现良好，暂无问题" image-size="60" />
          </div>
        </div>
        
        <div class="section">
          <h2 class="section-title">改进建议</h2>
          <div class="suggestion-list">
            <div
              v-for="(item, index) in analysis.suggestions"
              :key="index"
              class="suggestion-item"
            >
              <van-icon name="info" color="#1e88e5" />
              <span>{{ item.text }}</span>
            </div>
            <van-empty v-if="!analysis.suggestions || analysis.suggestions.length === 0" description="暂无建议" image-size="60" />
          </div>
        </div>
        
        <div class="section">
          <h2 class="section-title">详细报告</h2>
          <div class="report-card">
            <pre class="report-text">{{ analysis.report }}</pre>
          </div>
        </div>
        
        <div class="action-buttons">
          <van-button type="primary" block @click="askAI">询问AI如何改进</van-button>
          <van-button block @click="shareReport">分享报告</van-button>
        </div>
      </div>
      
      <van-empty v-if="!loading && !analysis" description="分析报告不存在" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAnalysisReport } from '@/api/analysis'
import { useChatStore } from '@/stores/chat'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()

const analysis = ref(null)
const loading = ref(false)

const ratingClass = computed(() => {
  const rating = analysis.value?.overall_rating
  if (rating === '优秀') return 'excellent'
  if (rating === '良好') return 'good'
  return 'need-improve'
})

onMounted(() => {
  loadAnalysis()
})

async function loadAnalysis() {
  loading.value = true
  try {
    analysis.value = await getAnalysisReport(route.params.id)
  } catch (error) {
    showToast({ type: 'fail', message: '加载分析报告失败' })
  } finally {
    loading.value = false
  }
}

async function askAI() {
  router.push('/home')
  await chatStore.sendChatMessage('根据我的对局表现，如何改进？')
}

function shareReport() {
  if (navigator.share) {
    navigator.share({
      title: '王者荣耀对局复盘',
      text: analysis.value?.report || ''
    })
  } else {
    navigator.clipboard.writeText(analysis.value?.report || '')
    showToast({ type: 'success', message: '报告已复制到剪贴板' })
  }
}
</script>

<style scoped>
.analysis-detail-page {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.content {
  padding: 16px;
}

.rating-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 32px 16px;
  text-align: center;
  color: white;
  margin-bottom: 24px;
}

.rating-label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.rating-value {
  font-size: 32px;
  font-weight: 700;
}

.rating-value.excellent {
  color: #4caf50;
}

.rating-value.good {
  color: #ff9800;
}

.rating-value.need-improve {
  color: #f44336;
}

.section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 12px;
}

.highlight-list,
.mistake-list,
.suggestion-list {
  background-color: var(--card-bg);
  border-radius: 12px;
  overflow: hidden;
}

.highlight-item,
.mistake-item,
.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  gap: 8px;
}

.highlight-item:last-child,
.mistake-item:last-child,
.suggestion-item:last-child {
  border-bottom: none;
}

.highlight-item span,
.mistake-item span,
.suggestion-item span {
  flex: 1;
  font-size: 14px;
  color: var(--text-color);
  line-height: 1.5;
}

.report-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.report-text {
  font-size: 14px;
  color: var(--text-color);
  line-height: 1.8;
  white-space: pre-wrap;
  margin: 0;
  font-family: inherit;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.action-buttons .van-button {
  flex: 1;
}

.dark-mode .highlight-list,
.dark-mode .mistake-list,
.dark-mode .suggestion-list,
.dark-mode .report-card {
  background-color: var(--card-bg);
}
</style>
