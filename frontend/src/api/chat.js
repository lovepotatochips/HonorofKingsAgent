import request from './index'

/**
 * 发送聊天消息
 * @param {Object} data - 消息数据对象
 * @returns {Promise} 返回请求的Promise对象
 */
export function sendMessage(data) {
  return request({
    url: '/api/v1/chat/send',
    method: 'post',
    data
  })
}

/**
 * 获取聊天历史记录
 * @param {string} userId - 用户ID
 * @param {number} limit - 返回记录数量限制，默认为20
 * @returns {Promise} 返回请求的Promise对象
 */
export function getChatHistory(userId, limit = 20) {
  return request({
    url: `/api/v1/chat/history/${userId}`,
    method: 'get',
    params: { limit }
  })
}

/**
 * 清除聊天历史记录
 * @param {string} userId - 用户ID
 * @returns {Promise} 返回请求的Promise对象
 */
export function clearChatHistory(userId) {
  return request({
    url: `/api/v1/chat/history/${userId}`,
    method: 'delete'
  })
}

/**
 * 获取聊天意图列表
 * @returns {Promise} 返回请求的Promise对象
 */
export function getIntents() {
  return request({
    url: '/api/v1/chat/intents',
    method: 'get'
  })
}
