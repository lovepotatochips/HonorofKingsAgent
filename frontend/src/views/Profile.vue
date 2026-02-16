<template>
  <div class="profile-page">
    <div class="profile-header">
      <div class="avatar">
        {{ userStore.nickname?.charAt(0) || 'U' }}
      </div>
      <div class="user-info">
        <h2>{{ userStore.nickname || '玩家' }}</h2>
        <p>{{ userStore.rank || '未设置段位' }} {{ userStore.stars > 0 ? `${userStore.stars}星` : '' }}</p>
      </div>
      <van-button size="small" @click="$router.push('/settings')">设置</van-button>
    </div>
    
    <div class="stats-section">
      <div class="stat-card">
        <span class="stat-value">{{ favoriteHeroesCount }}</span>
        <span class="stat-label">常用英雄</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">{{ chatMessagesCount }}</span>
        <span class="stat-label">对话次数</span>
      </div>
      <div class="stat-card">
        <span class="stat-value">{{ matchesCount }}</span>
        <span class="stat-label">对局记录</span>
      </div>
    </div>
    
    <div class="menu-section">
      <van-cell-group>
        <van-cell title="清除对话历史" is-link @click="clearChatHistory" />
        <van-cell title="清除所有数据" is-link @click="clearAllData" />
        <van-cell title="关于我们" is-link @click="showAbout" />
      </van-cell-group>
    </div>
    
    <van-tabbar v-model="activeTab" active-color="#1e88e5">
      <van-tabbar-item name="home" icon="chat-o" @click="$router.push('/home')">对话</van-tabbar-item>
      <van-tabbar-item name="hero" icon="friends-o" @click="$router.push('/hero')">英雄</van-tabbar-item>
      <van-tabbar-item name="match" icon="chart-trending-o" @click="$router.push('/match')">对局</van-tabbar-item>
      <van-tabbar-item name="profile" icon="user-o" @click="$router.push('/profile')">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { getMatchHistory } from '@/api/match'
import { showToast, showConfirmDialog } from 'vant'

const userStore = useUserStore()
const chatStore = useChatStore()
const activeTab = ref('profile')
const matchesCount = ref(0)

const favoriteHeroesCount = computed(() => userStore.favoriteHeroes?.length || 0)
const chatMessagesCount = computed(() => Math.ceil(chatStore.messages.length / 2))

onMounted(() => {
  loadMatchesCount()
})

async function loadMatchesCount() {
  try {
    const userId = localStorage.getItem('user_id')
    const matches = await getMatchHistory(userId, 100)
    matchesCount.value = matches.length
  } catch (error) {
    console.error('加载对局数量失败', error)
  }
}

async function clearChatHistory() {
  try {
    await showConfirmDialog({
      title: '确认清除',
      message: '确定要清除所有对话历史吗？'
    })
    
    await chatStore.clearHistory()
    showToast({ type: 'success', message: '清除成功' })
  } catch (error) {
    if (error !== 'cancel') {
      showToast({ type: 'fail', message: '清除失败' })
    }
  }
}

async function clearAllData() {
  try {
    await showConfirmDialog({
      title: '确认清除',
      message: '确定要清除所有数据吗？此操作不可恢复！'
    })
    
    await showConfirmDialog({
      title: '再次确认',
      message: '再次确认：所有数据将被清除！'
    })
    
    userStore.clearData()
    chatStore.clearLocalMessages()
    matchesCount.value = 0
    
    showToast({ type: 'success', message: '清除成功，请刷新页面' })
  } catch (error) {
    if (error !== 'cancel') {
      showToast({ type: 'fail', message: '清除失败' })
    }
  }
}

function showAbout() {
  showToast({ type: 'success', message: '王者荣耀智能助手 v1.0.0' })
}
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-color);
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 32px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  margin-right: 16px;
}

.user-info {
  flex: 1;
}

.user-info h2 {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.user-info p {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

.stats-section {
  display: flex;
  justify-content: space-around;
  padding: 20px 16px;
  margin-top: -20px;
}

.stat-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  flex: 1;
  margin: 0 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
  display: block;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.menu-section {
  padding: 16px;
}

.dark-mode .stat-card {
  background-color: var(--card-bg);
}
</style>
