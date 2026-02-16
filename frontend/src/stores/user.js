import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 用户状态管理Store
 * 用于管理用户的个人信息、偏好设置等状态
 */
export const useUserStore = defineStore('user', () => {
  // 用户基本信息
  const userId = ref('')           // 用户ID
  const nickname = ref('')         // 用户昵称
  const avatar = ref('')            // 用户头像
  const rank = ref('')              // 用户段位
  const stars = ref(0)              // 用户星星数
  const favoriteHeroes = ref([])    // 收藏的英雄列表
  
  // 用户偏好设置
  const preferences = ref({
    voice_enabled: true,           // 语音功能开关
    voice_wake_word: '王者助手',    // 语音唤醒词
    float_window_enabled: true,     // 浮窗开关
    dark_mode: false,              // 深色模式
    sound_enabled: true,           // 音效开关
    vibration_enabled: true,       // 震动开关
    auto_clear_context: false,     // 自动清除上下文
    context_rounds: 5              // 上下文轮数
  })
  
  /**
   * 初始化用户信息
   * 从localStorage加载用户数据，如果没有则创建新的用户ID
   */
  function initUser() {
    const storedId = localStorage.getItem('user_id')
    if (storedId) {
      // 加载已存在的用户数据
      userId.value = storedId
      nickname.value = localStorage.getItem('nickname') || ''
      avatar.value = localStorage.getItem('avatar') || ''
      rank.value = localStorage.getItem('rank') || ''
      stars.value = parseInt(localStorage.getItem('stars') || '0')
      favoriteHeroes.value = JSON.parse(localStorage.getItem('favorite_heroes') || '[]')
      loadPreferences()
    } else {
      // 创建新用户ID并保存
      userId.value = 'user_1771059406553_demo'
      localStorage.setItem('user_id', userId.value)
      savePreferences()
    }
  }
  
  /**
   * 生成唯一的用户ID
   * @returns {string} 格式为 user_<timestamp>_<random>
   */
  function generateUserId() {
    return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
  }
  
  /**
   * 更新用户资料
   * @param {Object} data - 用户资料数据
   * @param {string} data.nickname - 用户昵称
   * @param {string} data.avatar - 用户头像
   * @param {string} data.rank - 用户段位
   * @param {number} data.stars - 用户星星数
   * @param {Array} data.favoriteHeroes - 收藏的英雄列表
   */
  function updateProfile(data) {
    if (data.nickname) nickname.value = data.nickname
    if (data.avatar) avatar.value = data.avatar
    if (data.rank) rank.value = data.rank
    if (data.stars !== undefined) stars.value = data.stars
    if (data.favoriteHeroes) favoriteHeroes.value = data.favoriteHeroes
    
    // 保存到localStorage
    localStorage.setItem('nickname', nickname.value)
    localStorage.setItem('avatar', avatar.value)
    localStorage.setItem('rank', rank.value)
    localStorage.setItem('stars', stars.value.toString())
    localStorage.setItem('favorite_heroes', JSON.stringify(favoriteHeroes.value))
  }
  
  /**
   * 从localStorage加载用户偏好设置
   */
  function loadPreferences() {
    const stored = localStorage.getItem('user_preferences')
    if (stored) {
      try {
        preferences.value = { ...preferences.value, ...JSON.parse(stored) }
      } catch (e) {
        console.error('加载偏好设置失败', e)
      }
    }
  }
  
  /**
   * 保存用户偏好设置到localStorage
   */
  function savePreferences() {
    localStorage.setItem('user_preferences', JSON.stringify(preferences.value))
  }
  
  /**
   * 更新用户偏好设置
   * @param {Object} newPrefs - 新的偏好设置
   */
  function updatePreferences(newPrefs) {
    preferences.value = { ...preferences.value, ...newPrefs }
    savePreferences()
  }
  
  /**
   * 清除所有用户数据
   * 清除localStorage中的所有用户相关数据并重置状态
   */
  function clearData() {
    // 清除localStorage
    localStorage.removeItem('user_id')
    localStorage.removeItem('nickname')
    localStorage.removeItem('avatar')
    localStorage.removeItem('rank')
    localStorage.removeItem('stars')
    localStorage.removeItem('favorite_heroes')
    localStorage.removeItem('user_preferences')
    localStorage.removeItem('chat_history')
    
    // 重置所有状态
    userId.value = ''
    nickname.value = ''
    avatar.value = ''
    rank.value = ''
    stars.value = 0
    favoriteHeroes.value = []
    preferences.value = {
      voice_enabled: true,
      voice_wake_word: '王者助手',
      float_window_enabled: true,
      dark_mode: false,
      sound_enabled: true,
      vibration_enabled: true,
      auto_clear_context: false,
      context_rounds: 5
    }
  }
  
  // 导出状态和方法
  return {
    userId,
    nickname,
    avatar,
    rank,
    stars,
    favoriteHeroes,
    preferences,
    initUser,
    updateProfile,
    loadPreferences,
    savePreferences,
    updatePreferences,
    clearData
  }
})
