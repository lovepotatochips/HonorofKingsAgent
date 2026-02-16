// 导入 Vue 核心库
import { createApp } from 'vue'
// 导入 Pinia 状态管理库
import { createPinia } from 'pinia'
// 导入 Element Plus UI 组件库（用于 PC 端）
import ElementPlus from 'element-plus'
// 导入 Vant UI 组件库（用于移动端）
import Vant from 'vant'
// 导入 Vant 样式文件
import 'vant/lib/index.css'
// 导入 Element Plus 样式文件
import 'element-plus/dist/index.css'
// 导入全局样式文件
import './style.css'
// 导入根组件
import App from './App.vue'
// 导入路由配置
import router from './router'
// 导入 Vant 触摸模拟器（用于桌面端调试）
import '@vant/touch-emulator'

// 定义演示用户 ID
const demoUserId = 'user_1771059406553_demo'
// 从本地存储获取当前用户 ID
const currentUserId = localStorage.getItem('user_id')

// 如果当前用户 ID 存在且不是演示用户，则重置为演示用户
if (currentUserId && currentUserId !== demoUserId) {
  localStorage.setItem('user_id', demoUserId)
}

// 创建 Vue 应用实例
const app = createApp(App)
// 创建 Pinia 状态管理实例
const pinia = createPinia()

// 注册插件到应用
app.use(pinia)  // 注册状态管理
app.use(router) // 注册路由
app.use(ElementPlus) // 注册 Element Plus UI 库
app.use(Vant) // 注册 Vant UI 库

// 挂载应用到 DOM
app.mount('#app')
