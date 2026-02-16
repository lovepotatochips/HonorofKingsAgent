<template>
  <div class="hero-detail-page">
    <van-nav-bar
      title="英雄详情"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <div v-loading="loading" class="content">
      <div v-if="hero">
        <div class="hero-header">
          <div class="hero-image">
            <img v-if="hero.image_url" :src="hero.image_url" :alt="hero.name" @error="handleImageError" />
            <div v-else class="image-placeholder">{{ hero.name[0] }}</div>
          </div>
          <h1 class="hero-name">{{ hero.name }}</h1>
          <p class="hero-title">{{ hero.title }}</p>
          <div class="hero-tags">
            <span class="tag position">{{ getPositionLabel(hero.position) }}</span>
            <span class="tag difficulty">{{ getDifficultyLabel(hero.difficulty) }}</span>
          </div>
        </div>
        
        <div class="stats-card">
          <div class="stat-row">
            <div class="stat-item">
              <span class="stat-value">{{ (hero.win_rate * 100).toFixed(1) }}%</span>
              <span class="stat-label">胜率</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ (hero.pick_rate * 100).toFixed(1) }}%</span>
              <span class="stat-label">登场率</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ (hero.ban_rate * 100).toFixed(1) }}%</span>
              <span class="stat-label">禁用率</span>
            </div>
          </div>
        </div>
        
        <div class="section">
          <h2 class="section-title">技能介绍</h2>
          <div class="skills-list">
            <div v-for="(skill, index) in hero.skills" :key="index" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ skill.name }}</span>
                <span class="skill-type">{{ skill.type }}</span>
              </div>
              <p class="skill-description">{{ skill.description }}</p>
              <div class="skill-meta">
                <span>冷却: {{ skill.cooldown }}</span>
                <span>消耗: {{ skill.cost }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="section">
          <h2 class="section-title">克制关系</h2>
          <div v-if="hero.counter_heroes && hero.counter_heroes.length" class="counter-section">
            <p class="counter-title">克制:</p>
            <div class="counter-list">
              <span v-for="name in hero.counter_heroes" :key="name" class="counter-tag">{{ name }}</span>
            </div>
          </div>
          <div v-if="hero.countered_by_heroes && hero.countered_by_heroes.length" class="counter-section">
            <p class="counter-title">被克制:</p>
            <div class="counter-list">
              <span v-for="name in hero.countered_by_heroes" :key="name" class="counter-tag danger">{{ name }}</span>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <van-button type="primary" block @click="askAboutEquipment">询问出装</van-button>
          <van-button block @click="askAboutInscription">询问铭文</van-button>
        </div>
      </div>
      
      <van-empty v-if="!loading && !hero" description="英雄信息不存在" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getHeroDetail } from '@/api/hero'
import { useChatStore } from '@/stores/chat'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()

const hero = ref(null)
const loading = ref(false)

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
  loadHeroDetail()
})

async function loadHeroDetail() {
  loading.value = true
  try {
    hero.value = await getHeroDetail(route.params.id)
  } catch (error) {
    showToast({ type: 'fail', message: '加载英雄详情失败' })
  } finally {
    loading.value = false
  }
}

async function askAboutEquipment() {
  if (!hero.value) return
  
  router.push('/home')
  await chatStore.sendChatMessage(`${hero.value.name}怎么出装？`, hero.value.id)
}

async function askAboutInscription() {
  if (!hero.value) return
  
  router.push('/home')
  await chatStore.sendChatMessage(`${hero.value.name}用什么铭文？`, hero.value.id)
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
.hero-detail-page {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.content {
  padding: 16px;
}

.hero-header {
  text-align: center;
  padding: 20px 0;
}

.hero-image {
  width: 120px;
  height: 120px;
  margin: 0 auto 16px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: #f5f5f5;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: none;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 8px;
}

.hero-title {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.hero-tags {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.tag {
  padding: 6px 16px;
  border-radius: 16px;
  font-size: 13px;
  color: white;
}

.tag.position {
  background-color: #4caf50;
}

.tag.difficulty {
  background-color: #ff9800;
}

.stats-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-row {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-color);
  display: block;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
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

.skills-list {
  background-color: var(--card-bg);
  border-radius: 12px;
  overflow: hidden;
}

.skill-item {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
}

.skill-item:last-child {
  border-bottom: none;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.skill-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.skill-type {
  padding: 4px 8px;
  background-color: rgba(30, 136, 229, 0.1);
  color: var(--primary-color);
  border-radius: 4px;
  font-size: 12px;
}

.skill-description {
  font-size: 14px;
  color: var(--text-color);
  line-height: 1.6;
  margin-bottom: 8px;
}

.skill-meta {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  gap: 16px;
}

.counter-section {
  margin-bottom: 16px;
}

.counter-title {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.counter-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.counter-tag {
  padding: 6px 12px;
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
  border-radius: 16px;
  font-size: 13px;
}

.counter-tag.danger {
  background-color: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.action-buttons .van-button {
  flex: 1;
}

.dark-mode .stats-card,
.dark-mode .skills-list {
  background-color: var(--card-bg);
}
</style>
