<template>
  <div class="match-page">
    <div class="page-header">
      <h1>对局记录</h1>
      <van-button size="small" type="primary" @click="showImportDialog">导入对局</van-button>
    </div>
    
    <div class="match-list" v-loading="loading">
      <div
        v-for="match in matches"
        :key="match.id"
        class="match-card"
        @click="goToMatchDetail(match.id)"
      >
        <div class="match-header">
          <div class="match-result" :class="match.result">
            {{ getResultLabel(match.result) }}
          </div>
          <div class="match-time">{{ formatTime(match.created_at) }}</div>
        </div>
        
        <div class="match-hero">
          <div class="hero-avatar">{{ match.hero_name?.charAt(0) }}</div>
          <div class="hero-info">
            <div class="hero-name">{{ match.hero_name }}</div>
            <div class="hero-position">{{ match.position }}</div>
          </div>
        </div>
        
        <div class="match-stats">
          <div class="stat-row">
            <span class="stat-label">KDA</span>
            <span class="stat-value">{{ match.kda.toFixed(1) }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">参团率</span>
            <span class="stat-value">{{ (match.participation_rate * 100).toFixed(1) }}%</span>
          </div>
          <div class="stat-row" v-if="match.duration">
            <span class="stat-label">时长</span>
            <span class="stat-value">{{ formatDuration(match.duration) }}</span>
          </div>
        </div>
        
        <div class="match-actions">
          <van-button size="small" @click.stop="analyzeMatch(match.id)">复盘</van-button>
          <van-button size="small" type="danger" plain @click.stop="deleteMatch(match.id)">删除</van-button>
        </div>
      </div>
      
      <van-empty v-if="!loading && matches.length === 0" description="暂无对局记录" />
    </div>
    
    <van-dialog
      v-model:show="showImport"
      title="导入对局"
      show-cancel-button
      @confirm="handleImport"
    >
      <div class="import-form">
        <van-field
          v-model="importForm.hero_name"
          label="英雄名称"
          placeholder="请输入英雄名称"
        />
        <van-field
          v-model="importForm.position"
          label="位置"
          placeholder="请输入位置"
        />
        <van-field
          v-model="importForm.result"
          label="结果"
          placeholder="胜利/失败"
        />
        <van-field
          v-model.number="importForm.kills"
          label="击杀"
          type="number"
        />
        <van-field
          v-model.number="importForm.deaths"
          label="死亡"
          type="number"
        />
        <van-field
          v-model.number="importForm.assists"
          label="助攻"
          type="number"
        />
      </div>
    </van-dialog>
    
    <van-tabbar v-model="activeTab" active-color="#1e88e5">
      <van-tabbar-item name="home" icon="chat-o" @click="$router.push('/home')">对话</van-tabbar-item>
      <van-tabbar-item name="hero" icon="friends-o" @click="$router.push('/hero')">英雄</van-tabbar-item>
      <van-tabbar-item name="match" icon="chart-trending-o" @click="$router.push('/match')">对局</van-tabbar-item>
      <van-tabbar-item name="profile" icon="user-o" @click="$router.push('/profile')">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMatchHistory, deleteMatch as deleteMatchApi, importMatch, analyzeMatch as analyzeMatchApi } from '@/api/match'
import { showToast, showConfirmDialog } from 'vant'

const router = useRouter()
const matches = ref([])
const loading = ref(false)
const showImport = ref(false)
const activeTab = ref('match')

const importForm = ref({
  hero_name: '',
  position: '',
  result: '',
  kills: 0,
  deaths: 0,
  assists: 0
})

onMounted(() => {
  loadMatches()
})

async function loadMatches() {
  loading.value = true
  try {
    const userId = localStorage.getItem('user_id')
    matches.value = await getMatchHistory(userId, 20)
  } catch (error) {
    showToast({ type: 'fail', message: '加载对局记录失败' })
  } finally {
    loading.value = false
  }
}

function showImportDialog() {
  importForm.value = {
    hero_name: '',
    position: '',
    result: '',
    kills: 0,
    deaths: 0,
    assists: 0
  }
  showImport.value = true
}

async function handleImport() {
  try {
    const userId = localStorage.getItem('user_id')
    await importMatch({
      user_id: userId,
      ...importForm.value,
      kda: (importForm.value.kills + importForm.value.assists) / Math.max(importForm.value.deaths, 1),
      participation_rate: 0.5
    })
    showToast({ type: 'success', message: '导入成功' })
    loadMatches()
  } catch (error) {
    showToast({ type: 'fail', message: '导入失败' })
  }
}

async function deleteMatch(matchId) {
  try {
    await showConfirmDialog({
      title: '确认删除',
      message: '确定要删除这条对局记录吗？'
    })
    
    await deleteMatchApi(matchId)
    showToast({ type: 'success', message: '删除成功' })
    loadMatches()
  } catch (error) {
    if (error !== 'cancel') {
      showToast({ type: 'fail', message: '删除失败' })
    }
  }
}

async function analyzeMatch(matchId) {
  try {
    const userId = localStorage.getItem('user_id')
    const result = await analyzeMatchApi({
      match_id: matchId,
      user_id: userId
    })
    router.push(`/analysis/${result.analysis_id}`)
  } catch (error) {
    showToast({ type: 'fail', message: '复盘失败' })
  }
}

function goToMatchDetail(matchId) {
  analyzeMatch(matchId)
}

function getResultLabel(result) {
  const labels = {
    '胜利': '胜利',
    '失败': '失败',
    'win': '胜利',
    'loss': '失败',
    'victory': '胜利',
    'defeat': '失败'
  }
  return labels[result] || result || '未知'
}

function formatTime(dateStr) {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return `${date.getMonth() + 1}/${date.getDate()}`
}

function formatDuration(seconds) {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}
</script>

<style scoped>
.match-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-color);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
}

.page-header h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.match-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.match-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.match-result {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
}

.match-result.胜利,
.match-result.win,
.match-result.victory {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.match-result.失败,
.match-result.loss,
.match-result.defeat {
  background-color: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.match-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.match-hero {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.hero-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 700;
  margin-right: 12px;
}

.hero-info {
  flex: 1;
}

.hero-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 4px;
}

.hero-position {
  font-size: 12px;
  color: var(--text-secondary);
}

.match-stats {
  display: flex;
  justify-content: space-around;
  padding: 12px 0;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 12px;
}

.stat-row {
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  display: block;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.match-actions {
  display: flex;
  gap: 8px;
}

.match-actions .van-button {
  flex: 1;
}

.import-form {
  padding: 16px;
}

.dark-mode .match-card {
  background-color: var(--card-bg);
}
</style>
