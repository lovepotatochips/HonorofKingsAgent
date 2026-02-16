import request from './index'

export function importMatch(data) {
  return request({
    url: '/api/v1/match/import',
    method: 'post',
    data
  })
}

export function getMatchHistory(userId, limit = 10) {
  return request({
    url: `/api/v1/match/history/${userId}`,
    method: 'get',
    params: { limit }
  })
}

export function getMatchSummary(matchId) {
  return request({
    url: `/api/v1/match/summary/${matchId}`,
    method: 'get'
  })
}

export function deleteMatch(matchId) {
  return request({
    url: `/api/v1/match/${matchId}`,
    method: 'delete'
  })
}

export function analyzeMatch(data) {
  return request({
    url: '/api/v1/analysis/analyze',
    method: 'post',
    data
  })
}
