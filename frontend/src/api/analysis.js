import request from './index'

export function analyzeMatch(data) {
  return request({
    url: '/api/v1/analysis/analyze',
    method: 'post',
    data
  })
}

export function getAnalysisReport(analysisId) {
  return request({
    url: `/api/v1/analysis/report/${analysisId}`,
    method: 'get'
  })
}

export function getImprovementSuggestions(heroId) {
  return request({
    url: `/api/v1/analysis/suggestions/${heroId}`,
    method: 'get'
  })
}
