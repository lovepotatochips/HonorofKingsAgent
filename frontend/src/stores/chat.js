import { defineStore } from 'pinia'
import { ref } from 'vue'
import { sendMessage, getChatHistory, clearChatHistory } from '@/api/chat'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const loading = ref(false)
  const currentIntent = ref('')
  
  async function sendChatMessage(userMessage, heroId = null, matchId = null) {
    loading.value = true
    
    try {
      messages.value.push({
        role: 'user',
        content: userMessage,
        timestamp: Date.now()
      })
      
      const context = messages.value
        .slice(-6, -1)
        .map(msg => ({
          user_message: msg.role === 'user' ? msg.content : '',
          ai_response: msg.role === 'assistant' ? msg.content : ''
        }))
      
      const response = await sendMessage({
        user_id: localStorage.getItem('user_id') || '',
        message: userMessage,
        context,
        hero_id: heroId,
        match_id: matchId
      })
      
      messages.value.push({
        role: 'assistant',
        content: response.response,
        intent: response.intent,
        confidence: response.confidence,
        suggestions: response.suggestions,
        related_heroes: response.related_heroes,
        timestamp: Date.now()
      })
      
      currentIntent.value = response.intent
      
      return response
    } catch (error) {
      messages.value.push({
        role: 'assistant',
        content: '抱歉，发送消息失败，请稍后再试。',
        timestamp: Date.now()
      })
      throw error
    } finally {
      loading.value = false
    }
  }
  
  async function loadHistory() {
    try {
      const userId = localStorage.getItem('user_id')
      if (!userId) return
      
      const history = await getChatHistory(userId, 20)
      messages.value = history.map(item => ({
        role: 'user',
        content: item.user_message,
        timestamp: new Date(item.created_at).getTime()
      })).concat(history.map(item => ({
        role: 'assistant',
        content: item.ai_response,
        intent: item.intent,
        timestamp: new Date(item.created_at).getTime()
      })))
    } catch (error) {
      console.error('加载对话历史失败', error)
    }
  }
  
  async function clearHistory() {
    try {
      const userId = localStorage.getItem('user_id')
      if (!userId) return
      
      await clearChatHistory(userId)
      messages.value = []
    } catch (error) {
      console.error('清除对话历史失败', error)
      throw error
    }
  }
  
  function clearLocalMessages() {
    messages.value = []
  }
  
  return {
    messages,
    loading,
    currentIntent,
    sendChatMessage,
    loadHistory,
    clearHistory,
    clearLocalMessages
  }
})
