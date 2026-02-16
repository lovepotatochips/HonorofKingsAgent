# API文档

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API版本**: v1
- **认证方式**: 暂不需要

## 对话接口

### 发送消息

```http
POST /api/v1/chat/send
Content-Type: application/json

{
  "user_id": "user_123456",
  "message": "鲁班七号怎么出装？",
  "context": [],
  "hero_id": 1,
  "match_id": null
}
```

**响应示例**:
```json
{
  "response": "鲁班七号作为射手，核心出装推荐...",
  "intent": "equipment",
  "confidence": 0.92,
  "suggestions": ["查看铭文搭配", "查看对位英雄"],
  "related_heroes": [2, 3]
}
```

### 获取对话历史

```http
GET /api/v1/chat/history/{user_id}?limit=20
```

### 清除对话历史

```http
DELETE /api/v1/chat/history/{user_id}
```

### 获取意图列表

```http
GET /api/v1/chat/intents
```

## 英雄接口

### 获取英雄列表

```http
GET /api/v1/hero/list?position=archer&difficulty=easy&search=鲁班
```

### 获取英雄详情

```http
GET /api/v1/hero/{hero_id}
```

### 获取英雄出装

```http
GET /api/v1/hero/{hero_id}/equipment?rank=全部
```

### 获取英雄铭文

```http
GET /api/v1/hero/{hero_id}/inscription?rank=全部
```

### BP建议

```http
POST /api/v1/hero/bp/suggestion
Content-Type: application/json

{
  "our_heroes": ["鲁班七号", "亚瑟", "妲己"],
  "enemy_heroes": ["孙悟空", "张飞", "程咬金"]
}
```

## 用户接口

### 获取用户信息

```http
GET /api/v1/user/profile/{user_id}
```

### 更新用户信息

```http
PUT /api/v1/user/profile/{user_id}
Content-Type: application/json

{
  "id": "user_123456",
  "nickname": "玩家1",
  "rank": "钻石",
  "stars": 3
}
```

### 获取用户偏好

```http
GET /api/v1/user/preferences/{user_id}
```

### 更新用户偏好

```http
PUT /api/v1/user/preferences/{user_id}
Content-Type: application/json

{
  "voice_enabled": true,
  "dark_mode": false
}
```

## 对局接口

### 导入对局数据

```http
POST /api/v1/match/import
Content-Type: application/json

{
  "user_id": "user_123456",
  "hero_name": "鲁班七号",
  "position": "射手",
  "result": "胜利",
  "kills": 12,
  "deaths": 3,
  "assists": 8
}
```

### 获取对局历史

```http
GET /api/v1/match/history/{user_id}?limit=10
```

### 获取对局摘要

```http
GET /api/v1/match/summary/{match_id}
```

### 删除对局

```http
DELETE /api/v1/match/{match_id}
```

## 分析接口

### 分析对局

```http
POST /api/v1/analysis/analyze
Content-Type: application/json

{
  "match_id": "match_123456",
  "user_id": "user_123456"
}
```

### 获取分析报告

```http
GET /api/v1/analysis/report/{analysis_id}
```

### 获取改进建议

```http
GET /api/v1/analysis/suggestions/{hero_id}
```

## 健康检查

```http
GET /health
```

**响应**:
```json
{
  "status": "healthy"
}
```

## 错误码

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
