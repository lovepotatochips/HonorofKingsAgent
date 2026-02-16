<template>
  <div class="hero-page">
    <div class="search-bar">
      <van-search
        v-model="searchKeyword"
        placeholder="搜索英雄"
        shape="round"
        background="transparent"
        @search="handleSearch"
      />
    </div>
    
    <div class="filter-tabs">
      <van-tabs v-model:active="activePosition" @change="handleFilterChange">
        <van-tab title="全部" name="" />
        <van-tab title="坦克" name="tank" />
        <van-tab title="战士" name="warrior" />
        <van-tab title="刺客" name="assassin" />
        <van-tab title="法师" name="mage" />
        <van-tab title="射手" name="archer" />
        <van-tab title="辅助" name="support" />
      </van-tabs>
    </div>
    
    <div class="hero-list" v-loading="loading">
      <div
        v-for="hero in heroes"
        :key="hero.id"
        class="hero-card"
        @click="goToHeroDetail(hero.id)"
      >
        <div class="hero-avatar">
          <img v-if="hero.image_url" :src="hero.image_url" :alt="hero.name" @error="handleImageError" />
          <div v-else class="avatar-placeholder">{{ hero.name[0] }}</div>
        </div>
        <div class="hero-info">
          <div class="hero-name">{{ hero.name }}</div>
          <div class="hero-title">{{ hero.title }}</div>
          <div class="hero-meta">
            <span class="meta-tag position">{{ getPositionLabel(hero.position) }}</span>
            <span class="meta-tag difficulty">{{ getDifficultyLabel(hero.difficulty) }}</span>
          </div>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-label">胜率</span>
            <span class="stat-value win-rate">{{ (hero.win_rate * 100).toFixed(1) }}%</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">登场</span>
            <span class="stat-value">{{ (hero.pick_rate * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>
      
      <van-empty v-if="!loading && heroes.length === 0" description="暂无英雄数据" />
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getHeroList } from '@/api/hero'
import { showToast } from 'vant'

const router = useRouter()
const heroes = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const activePosition = ref('')
const activeTab = ref('hero')

const positionLabels = {
  tank: '坦克',
  warrior: '战士',
  assassin: '刺客',
  mage: '法师',
  archer: '射手',
  support: '辅助'
}

const difficultyLabels = {
  easy: '简单',
  medium: '中等',
  hard: '困难'
}

onMounted(() => {
  loadHeroes()
})

async function loadHeroes() {
  loading.value = true
  try {
    heroes.value = await getHeroList({
      position: activePosition.value || undefined,
      search: searchKeyword.value || undefined
    })
  } catch (error) {
    showToast({ type: 'fail', message: '加载英雄列表失败' })
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  loadHeroes()
}

function handleFilterChange() {
  loadHeroes()
}

function goToHeroDetail(heroId) {
  router.push(`/hero/${heroId}`)
}

function getPositionLabel(position) {
  return positionLabels[position] || position
}

function getDifficultyLabel(difficulty) {
  return difficultyLabels[difficulty] || difficulty
}

function handleImageError(event) {
  event.target.style.display = 'none'
  event.target.nextElementSibling.style.display = 'flex'
}
</script>

<style scoped>
.hero-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-color);
}

.search-bar {
  padding: 12px 16px;
  background-color: var(--card-bg);
}

.filter-tabs {
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
}

.hero-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.hero-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  margin-bottom: 12px;
  background-color: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.hero-card:active {
  transform: scale(0.98);
}

.hero-avatar {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  margin-right: 12px;
  flex-shrink: 0;
  background-color: #f5f5f5;
}

.hero-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: none;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  color: #999;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-info {
  flex: 1;
}

.hero-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 4px;
}

.hero-title {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.hero-meta {
  display: flex;
  gap: 8px;
}

.meta-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: white;
}

.meta-tag.position {
  background-color: #4caf50;
}

.meta-tag.difficulty {
  background-color: #ff9800;
}

.hero-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.stat-item {
  text-align: right;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
}

.stat-value.win-rate {
  color: #4caf50;
}

.dark-mode .hero-card {
  background-color: var(--card-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
</style>
