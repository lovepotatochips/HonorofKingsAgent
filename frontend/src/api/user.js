import request from './index'

export function getUserProfile(userId) {
  return request({
    url: `/api/v1/user/profile/${userId}`,
    method: 'get'
  })
}

export function updateUserProfile(userId, data) {
  return request({
    url: `/api/v1/user/profile/${userId}`,
    method: 'put',
    data
  })
}

export function getUserPreferences(userId) {
  return request({
    url: `/api/v1/user/preferences/${userId}`,
    method: 'get'
  })
}

export function updateUserPreferences(userId, data) {
  return request({
    url: `/api/v1/user/preferences/${userId}`,
    method: 'put',
    data
  })
}

export function clearUserData(userId) {
  return request({
    url: `/api/v1/user/data/${userId}`,
    method: 'delete'
  })
}
