<template>
  <div class="home-page">
    <div class="chat-container" ref="chatContainer">
      <div class="chat-messages">
        <div
          v-for="(message, index) in chatStore.messages"
          :key="index"
          :class="['message', message.role]"
        >
          <div class="message-bubble">
            <div class="message-content">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            <div v-if="message.role === 'assistant' && message.suggestions" class="suggestions">
              <div
                v-for="(suggestion, idx) in message.suggestions"
                :key="idx"
                class="suggestion-tag"
                @click="handleSuggestionClick(suggestion)"
              >
                {{ suggestion }}
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="chatStore.loading" class="message assistant">
          <div class="message-bubble loading">
            <van-loading type="spinner" size="20" />
            <span>思考中...</span>
          </div>
        </div>
      </div>
      
      <div class="quick-commands">
        <div
          v-for="command in quickCommands"
          :key="command.command"
          class="quick-command"
          @click="handleQuickCommand(command.command)"
        >
          {{ command.command }}
        </div>
      </div>
      
      <div class="input-area">
        <div class="input-wrapper">
          <input
            v-model="inputMessage"
            type="text"
            placeholder="问我关于王者荣耀的任何问题..."
            @keyup.enter="handleSend"
            class="message-input"
          />
          <button
            :disabled="!inputMessage.trim() || chatStore.loading"
            @click="handleSend"
            class="send-button"
          >
            发送
          </button>
        </div>
      </div>
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
import { ref, onMounted, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import { showToast } from 'vant'

const chatStore = useChatStore()
const chatContainer = ref(null)
const inputMessage = ref('')
const activeTab = ref('home')

const quickCommands = [
  { command: '我的常用英雄出装' },
  { command: '当前版本强势英雄' },
  { command: 'BP阵容建议' },
  { command: '对局复盘' }
]

onMounted(async () => {
  await chatStore.loadHistory()
  scrollToBottom()
})

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

async function handleSend() {
  if (!inputMessage.value.trim() || chatStore.loading) return
  
  const message = inputMessage.value.trim()
  inputMessage.value = ''
  
  try {
    await chatStore.sendChatMessage(message)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    showToast({ type: 'fail', message: '发送失败，请重试' })
  }
}

function handleQuickCommand(command) {
  inputMessage.value = command
  handleSend()
}

function handleSuggestionClick(suggestion) {
  inputMessage.value = suggestion
  handleSend()
}

function scrollToBottom() {
  if (chatContainer.value) {
    const messages = chatContainer.value.querySelector('.chat-messages')
    messages.scrollTop = messages.scrollHeight
  }
}
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-color);
  padding-bottom: 50px;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 8px;
  min-height: 0;
}

.message {
  display: flex;
  margin-bottom: 16px;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.message.user .message-bubble {
  background-color: var(--primary-color);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-bubble {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-bottom-left-radius: 4px;
}

.message-bubble.loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.message-content {
  word-wrap: break-word;
  line-height: 1.5;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 4px;
}

.suggestions {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.suggestion-tag {
  padding: 4px 12px;
  background-color: rgba(30, 136, 229, 0.1);
  color: var(--primary-color);
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
}

.quick-commands {
  display: flex;
  gap: 8px;
  padding: 8px 16px;
  overflow-x: auto;
  background-color: var(--card-bg);
}

.quick-command {
  padding: 8px 16px;
  background-color: rgba(30, 136, 229, 0.1);
  color: var(--primary-color);
  border-radius: 20px;
  font-size: 13px;
  white-space: nowrap;
  cursor: pointer;
}

.input-area {
  padding: 12px 16px;
  background-color: var(--card-bg);
  border-top: 1px solid var(--border-color);
}

.input-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.message-input:focus {
  border-color: var(--primary-color);
}

.send-button {
  padding: 12px 24px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dark-mode .message.user .message-bubble {
  background-color: #42a5f5;
}

.dark-mode .message.assistant .message-bubble {
  background-color: var(--card-bg);
  border-color: var(--border-color);
}
</style>
