<template>
  <div class="settings-page">
    <van-nav-bar
      title="设置"
      left-arrow
      @click-left="$router.back()"
      fixed
      placeholder
    />
    
    <div class="settings-content">
      <van-cell-group title="偏好设置">
        <van-cell center title="语音功能">
          <template #right-icon>
            <van-switch v-model="preferences.voice_enabled" @change="savePreferences" />
          </template>
        </van-cell>
        
        <van-field
          v-model="preferences.voice_wake_word"
          label="语音唤醒词"
          placeholder="请输入语音唤醒词"
          @blur="savePreferences"
        />
        
        <van-cell center title="悬浮窗">
          <template #right-icon>
            <van-switch v-model="preferences.float_window_enabled" @change="savePreferences" />
          </template>
        </van-cell>
        
        <van-cell center title="暗黑模式">
          <template #right-icon>
            <van-switch v-model="preferences.dark_mode" @change="savePreferences" />
          </template>
        </van-cell>
        
        <van-cell center title="声音提示">
          <template #right-icon>
            <van-switch v-model="preferences.sound_enabled" @change="savePreferences" />
          </template>
        </van-cell>
        
        <van-cell center title="震动反馈">
          <template #right-icon>
            <van-switch v-model="preferences.vibration_enabled" @change="savePreferences" />
          </template>
        </van-cell>
        
        <van-cell center title="自动清空上下文">
          <template #right-icon>
            <van-switch v-model="preferences.auto_clear_context" @change="savePreferences" />
          </template>
        </van-cell>
        
        <van-field
          v-model.number="preferences.context_rounds"
          label="上下文轮数"
          type="number"
          placeholder="请输入上下文轮数"
          @blur="savePreferences"
        />
      </van-cell-group>
      
      <van-cell-group title="个人信息">
        <van-field
          v-model="profile.nickname"
          label="昵称"
          placeholder="请输入昵称"
          @blur="saveProfile"
        />
        
        <van-field
          v-model="profile.rank"
          label="段位"
          placeholder="请输入段位"
          @blur="saveProfile"
        />
        
        <van-field
          v-model.number="profile.stars"
          label="星数"
          type="number"
          placeholder="请输入星数"
          @blur="saveProfile"
        />
      </van-cell-group>
      
      <div class="info-section">
        <p>版本：1.0.0</p>
        <p>王者荣耀智能助手 - 合规、轻量、AI驱动</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { showToast } from 'vant'

const router = useRouter()
const userStore = useUserStore()

const preferences = ref({
  voice_enabled: true,
  voice_wake_word: '王者助手',
  float_window_enabled: true,
  dark_mode: false,
  sound_enabled: true,
  vibration_enabled: true,
  auto_clear_context: false,
  context_rounds: 5
})

const profile = ref({
  nickname: '',
  rank: '',
  stars: 0
})

onMounted(() => {
  loadSettings()
})

function loadSettings() {
  preferences.value = { ...userStore.preferences }
  profile.value = {
    nickname: userStore.nickname || '',
    rank: userStore.rank || '',
    stars: userStore.stars || 0
  }
}

function savePreferences() {
  userStore.updatePreferences(preferences.value)
  showToast({ type: 'success', message: '设置已保存' })
}

function saveProfile() {
  userStore.updateProfile({
    ...profile.value,
    avatar: userStore.avatar,
    favoriteHeroes: userStore.favoriteHeroes
  })
  showToast({ type: 'success', message: '个人信息已保存' })
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background-color: var(--bg-color);
}

.settings-content {
  padding: 16px;
}

.info-section {
  text-align: center;
  padding: 32px 16px;
  color: var(--text-secondary);
  font-size: 12px;
}

.info-section p {
  margin: 4px 0;
}
</style>
