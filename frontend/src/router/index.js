// 导入 Vue Router 的核心函数
import { createRouter, createWebHistory } from 'vue-router'
// 导入用户状态管理 store
import { useUserStore } from '@/stores/user'

// 定义路由配置数组
const routes = [
  {
    path: '/',           // 根路径
    redirect: '/home'    // 重定向到首页
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),  // 懒加载首页组件
    meta: { title: '首页', keepAlive: true }       // 设置页面标题和启用缓存
  },
  {
    path: '/hero',
    name: 'Hero',
    component: () => import('@/views/Hero.vue'),   // 懒加载英雄列表组件
    meta: { title: '英雄', keepAlive: true }       // 设置页面标题和启用缓存
  },
  {
    path: '/hero/:id',
    name: 'HeroDetail',
    component: () => import('@/views/HeroDetail.vue'),  // 懒加载英雄详情组件
    meta: { title: '英雄详情' }                         // 设置页面标题
  },
  {
    path: '/match',
    name: 'Match',
    component: () => import('@/views/Match.vue'),  // 懒加载对局组件
    meta: { title: '对局', keepAlive: true }       // 设置页面标题和启用缓存
  },
  {
    path: '/analysis/:id',
    name: 'AnalysisDetail',
    component: () => import('@/views/AnalysisDetail.vue'),  // 懒加载复盘分析组件
    meta: { title: '复盘分析' }                             // 设置页面标题
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),  // 懒加载个人中心组件
    meta: { title: '我的', keepAlive: true }         // 设置页面标题和启用缓存
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),  // 懒加载设置组件
    meta: { title: '设置' }                            // 设置页面标题
  }
]

// 创建路由实例，配置使用 HTML5 History 模式
const router = createRouter({
  history: createWebHistory(),  // 使用 HTML5 History 模式
  routes                        // 注入路由配置
})

// 全局前置守卫，在每次路由跳转前执行
router.beforeEach((to, from, next) => {
  // 获取用户 store 实例
  const userStore = useUserStore()
  // 如果用户未初始化，则初始化用户信息
  if (!userStore.userId) {
    userStore.initUser()
  }
  
  // 动态设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 王者荣耀智能助手` : '王者荣耀智能助手'
  // 放行路由跳转
  next()
})

// 导出路由实例
export default router
