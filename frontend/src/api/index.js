// 引入 axios HTTP 请求库
import axios from 'axios'
// 引入 Vant UI 组件库中的 Toast 提示组件
import { showToast } from 'vant'

// 从环境变量中获取 API 基础 URL
const baseURL = import.meta.env.VITE_API_BASE_URL

// 创建 axios 实例，配置默认参数
const request = axios.create({
  baseURL, // API 基础路径
  timeout: 10000, // 请求超时时间设置为 10 秒
  headers: {
    'Content-Type': 'application/json' // 默认请求头设置为 JSON 格式
  }
})

// 请求拦截器：在请求发送前对请求配置进行处理
request.interceptors.request.use(
  config => {
    // 可以在这里添加 token 等认证信息
    return config
  },
  error => {
    // 请求配置出错时的处理
    return Promise.reject(error)
  }
)

// 响应拦截器：对响应数据进行统一处理
request.interceptors.response.use(
  response => {
    // 成功响应时，直接返回响应数据
    return response.data
  },
  error => {
    // 错误响应时的统一处理
    if (error.response) {
      // 服务器返回了错误响应
      const status = error.response.status
      
      // 根据不同的 HTTP 状态码显示不同的错误提示
      if (status === 401) {
        // 未授权，用户未登录或 token 过期
        showToast({ type: 'fail', message: '未授权，请重新登录' })
      } else if (status === 404) {
        // 请求的资源不存在
        showToast({ type: 'fail', message: '请求的资源不存在' })
      } else if (status === 500) {
        // 服务器内部错误
        showToast({ type: 'fail', message: '服务器错误，请稍后再试' })
      } else {
        // 其他错误，尝试从响应数据中获取错误详情
        const message = error.response.data?.detail || '请求失败'
        showToast({ type: 'fail', message })
      }
    } else if (error.code === 'ECONNABORTED') {
      // 请求超时错误
      showToast({ type: 'fail', message: '请求超时，请检查网络连接' })
    } else {
      // 网络连接错误
      showToast({ type: 'fail', message: '网络错误，请稍后再试' })
    }
    
    // 将错误继续传递，让调用者可以进一步处理
    return Promise.reject(error)
  }
)

// 导出配置好的 axios 实例，供其他模块使用
export default request
