/**
 * Hero API 模块
 * 提供英雄相关的接口请求方法
 */
import request from './index'

/**
 * 获取英雄列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 英雄列表数据
 */
export function getHeroList(params = {}) {
  return request({
    url: '/api/v1/hero/list',
    method: 'get',
    params
  })
}

/**
 * 获取英雄详细信息
 * @param {number|String} heroId - 英雄ID
 * @returns {Promise} 英雄详细数据
 */
export function getHeroDetail(heroId) {
  return request({
    url: `/api/v1/hero/${heroId}`,
    method: 'get'
  })
}

/**
 * 获取英雄装备推荐
 * @param {number|String} heroId - 英雄ID
 * @param {String} rank - 段位，默认为'全部'
 * @returns {Promise} 英雄装备推荐数据
 */
export function getHeroEquipment(heroId, rank = '全部') {
  return request({
    url: `/api/v1/hero/${heroId}/equipment`,
    method: 'get',
    params: { rank }
  })
}

/**
 * 获取英雄铭文推荐
 * @param {number|String} heroId - 英雄ID
 * @param {String} rank - 段位，默认为'全部'
 * @returns {Promise} 英雄铭文推荐数据
 */
export function getHeroInscription(heroId, rank = '全部') {
  return request({
    url: `/api/v1/hero/${heroId}/inscription`,
    method: 'get',
    params: { rank }
  })
}

/**
 * 获取BP（Ban/Pick）建议
 * @param {Array} ourHeroes - 我方已选英雄列表
 * @param {Array} enemyHeroes - 敌方已选英雄列表
 * @returns {Promise} BP建议数据
 */
export function getBPSuggestion(ourHeroes, enemyHeroes) {
  return request({
    url: '/api/v1/hero/bp/suggestion',
    method: 'post',
    data: {
      our_heroes: ourHeroes,
      enemy_heroes: enemyHeroes
    }
  })
}

/**
 * 获取英雄位置分类
 * @returns {Promise} 位置分类列表（如：对抗路、中路、发育路等）
 */
export function getPositions() {
  return request({
    url: '/api/v1/hero/categories/positions',
    method: 'get'
  })
}

/**
 * 获取英雄难度分类
 * @returns {Promise} 难度分类列表（如：简单、中等、困难等）
 */
export function getDifficulties() {
  return request({
    url: '/api/v1/hero/categories/difficulties',
    method: 'get'
  })
}
