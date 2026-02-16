# 导入类型提示
# Dict: 字典类型
# Any: 任意类型
# List: 列表类型
# Optional: 可选类型（可以为None）
from typing import Dict, Any, List, Optional

# 导入意图识别结果模型
# IntentResult: 意图识别结果，包含意图类型、置信度和实体信息
from app.schemas.chat import IntentResult

# 导入正则表达式模块
# re: Python的正则表达式库，用于模式匹配
import re


class IntentService:
    """
    意图识别服务类
    
    负责识别用户问题的意图类型
    
    主要功能:
        - 识别用户问题的意图分类
        - 提取问题中的实体（如英雄名称、段位等）
        - 计算意图识别的置信度
    
    设计模式:
        - 基于规则的模式匹配（Rule-based Pattern Matching）
        - 使用正则表达式匹配问题模式
        - 返回意图识别结果
    
    使用场景:
        - 聊天对话中的意图识别
        - 引导AI生成正确的回复
        - 提供对话建议
    
    支持的意图类型:
        - equipment: 装备相关
        - inscription: 铭文相关
        - bp_suggestion: BP建议相关
        - match_analysis: 对局分析相关
        - monster_timer: 野怪计时相关
        - entertainment: 娱乐互动相关
    """
    
    # ==================== 意图模式定义 ====================
    
    # 意图模式映射表
    # key: 意图类型
    # value: 该意图对应的正则表达式模式列表
    # 用途: 通过正则表达式匹配用户问题，识别意图类型
    INTENT_PATTERNS = {
        # 装备相关的意图
        "equipment": [
            # 匹配包含"出装"的问题
            r".*出装.*",
            # 匹配包含"装备"的问题
            r".*装备.*",
            # 匹配包含"买什么"的问题
            r".*买什么.*",
            # 匹配包含"推荐装备"的问题
            r".*推荐装备.*",
            # 匹配包含"装备推荐"的问题
            r".*装备推荐.*"
        ],
        
        # 铭文相关的意图
        "inscription": [
            # 匹配包含"铭文"的问题
            r".*铭文.*",
            # 匹配包含"符文"的问题（铭文的旧称）
            r".*符文.*",
            # 匹配包含"搭配"的问题
            r".*搭配.*",
            # 匹配包含"铭文推荐"的问题
            r".*铭文推荐.*"
        ],
        
        # BP建议相关的意图
        "bp_suggestion": [
            # 匹配包含"BP"的问题（Ban/Pick阶段）
            r".*BP.*",
            # 匹配包含"禁选"的问题
            r".*禁选.*",
            # 匹配包含"counter"的问题（克制关系）
            r".*counter.*",
            # 匹配包含"阵容"的问题
            r".*阵容.*",
            # 匹配包含"选英雄"的问题
            r".*选英雄.*"
        ],
        
        # 对局分析相关的意图
        "match_analysis": [
            # 匹配包含"复盘"的问题
            r".*复盘.*",
            # 匹配包含"分析"的问题
            r".*分析.*",
            # 匹配包含"对局"的问题
            r".*对局.*",
            # 匹配包含"刚才"的问题
            r".*刚才.*",
            # 匹配包含"怎么打"的问题
            r".*怎么打.*"
        ],
        
        # 野怪计时相关的意图
        "monster_timer": [
            # 匹配包含"计时"的问题
            r".*计时.*",
            # 匹配包含"buff"的问题
            r".*buff.*",
            # 匹配包含"野怪"的问题
            r".*野怪.*",
            # 匹配包含"暴君"的问题
            r".*暴君.*",
            # 匹配包含"龙"的问题
            r".*龙.*"
        ],
        
        # 娱乐互动相关的意图
        "entertainment": [
            # 匹配包含"语音"的问题
            r".*语音.*",
            # 匹配包含"梗"的问题
            r".*梗.*",
            # 匹配包含"好玩"的问题
            r".*好玩.*",
            # 匹配包含"搞笑"的问题
            r".*搞笑.*",
            # 匹配包含"趣味"的问题
            r".*趣味.*"
        ]
    }
    
    # ==================== 英雄名称列表 ====================
    
    # 英雄名称列表
    # 用途: 从用户问题中提取英雄名称
    # 注意: 这是简化版本，实际应用中应该从数据库动态加载
    HERO_NAMES = [
        # 射手
        "鲁班七号", "后羿", "马可波罗", "公孙离", "孙尚香", "虞姬", "百里守约", "伽罗",
        # 法师
        "安琪拉", "王昭君", "甄姬", "貂蝉",
        # 战士/坦克
        "亚瑟", "程咬金", "典韦", "夏侯惇", "张飞",
        # 辅助
        "蔡文姬", "瑶",
        # 刺客
        "李白", "韩信", "孙悟空",
        # 坦克
        "庄周"
    ]
    
    def recognize(self, message: str) -> IntentResult:
        """
        识别用户问题的意图
        
        参数:
            message: 用户的消息内容
        
        返回:
            IntentResult: 意图识别结果，包含意图类型、置信度和实体信息
        
        功能:
            - 识别用户问题的意图类型
            - 提取问题中的实体
            - 计算意图识别的置信度
        
        业务逻辑:
            1. 清理消息（去除首尾空格）
            2. 如果消息为空，返回未知意图
            3. 提取问题中的实体（英雄名称、段位等）
            4. 遍历所有意图模式，尝试匹配
            5. 计算匹配的置信度
            6. 选择置信度最高的意图
            7. 如果没有匹配到意图但包含英雄名称，默认为装备相关
            8. 返回意图识别结果
        
        算法:
            - 基于规则的模式匹配（Rule-based Pattern Matching）
            - 使用正则表达式进行模式匹配
            - 置信度基于匹配模式数量和关键词
        """
        # 清理消息：去除首尾空格
        message = message.strip()
        
        # 如果消息为空，返回未知意图
        if not message:
            return IntentResult(
                intent="unknown",
                confidence=0.0,
                entities={}
            )
        
        # 提取问题中的实体（如英雄名称、段位等）
        entities = self._extract_entities(message)
        
        # 初始化最佳意图和置信度
        best_intent = "unknown"
        best_confidence = 0.0
        
        # 遍历所有意图模式
        # 尝试找到与消息匹配的意图
        for intent, patterns in self.INTENT_PATTERNS.items():
            # 遍历该意图的所有模式
            for pattern in patterns:
                # 使用正则表达式匹配消息
                # re.IGNORECASE: 忽略大小写
                if re.search(pattern, message, re.IGNORECASE):
                    # 计算该意图的置信度
                    confidence = self._calculate_confidence(message, intent)
                    
                    # 如果当前置信度更高，更新最佳意图
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent
        
        # 如果没有匹配到任何意图，但问题中包含英雄名称
        # 则默认推断为装备相关的问题
        if best_intent == "unknown" and entities.get("hero_name"):
            best_intent = "equipment"
            best_confidence = 0.7
        
        # 返回意图识别结果
        return IntentResult(
            intent=best_intent,
            confidence=best_confidence,
            entities=entities
        )
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """
        从消息中提取实体
        
        参数:
            message: 用户的消息内容
        
        返回:
            Dict[str, Any]: 提取的实体字典，包含英雄名称、段位等
        
        功能:
            - 提取消息中的英雄名称
            - 提取消息中的段位信息
            - 返回提取的实体信息
        
        业务逻辑:
            1. 遍历英雄名称列表，检查是否在消息中
            2. 使用正则表达式匹配段位信息
            3. 将提取的实体存储在字典中返回
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        
        支持的实体类型:
            - hero_name: 英雄名称
            - rank: 段位
        """
        # 初始化实体字典
        entities = {}
        
        # ==================== 提取英雄名称 ====================
        
        hero_name = None
        # 遍历英雄名称列表
        for hero in self.HERO_NAMES:
            # 检查英雄名称是否在消息中
            if hero in message:
                # 找到匹配的英雄名称
                hero_name = hero
                break
        
        # 如果找到了英雄名称，添加到实体字典
        if hero_name:
            entities["hero_name"] = hero_name
        
        # ==================== 提取段位信息 ====================
        
        # 定义段位匹配的正则表达式模式
        # 匹配：青铜、白银、黄金、铂金、钻石、星耀、王者、荣耀王者
        rank_pattern = r"(青铜|白银|黄金|铂金|钻石|星耀|王者|荣耀王者)"
        
        # 使用正则表达式匹配段位
        rank_match = re.search(rank_pattern, message)
        
        # 如果匹配到段位，添加到实体字典
        if rank_match:
            # group(1) 获取第一个捕获组的内容
            entities["rank"] = rank_match.group(1)
        
        # 返回实体字典
        return entities
    
    def _calculate_confidence(self, message: str, intent: str) -> float:
        """
        计算意图识别的置信度
        
        参数:
            message: 用户的消息内容
            intent: 识别的意图类型
        
        返回:
            float: 置信度，范围0-1
        
        功能:
            - 计算意图识别的可信程度
            - 基于消息中的关键词进行加权
        
        业务逻辑:
            1. 设置基础置信度为0.85
            2. 如果消息包含"推荐"或"怎么"，增加置信度
            3. 如果消息包含"详细"或"具体"，增加置信度
            4. 返回不超过0.99的置信度
        
        置信度计算规则:
            - 基础置信度: 0.85（表示基本匹配）
            - 关键词"推荐"或"怎么": +0.1（表示明确需求）
            - 关键词"详细"或"具体": +0.05（表示需要详细信息）
            - 最大置信度: 0.99（避免过度自信）
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        """
        # 基础置信度
        # 表示基本匹配到意图模式
        base_confidence = 0.85
        
        # 如果消息包含"推荐"或"怎么"，增加置信度
        # 这表示用户有明确的需求或问题
        if "推荐" in message or "怎么" in message:
            base_confidence += 0.1
        
        # 如果消息包含"详细"或"具体"，增加置信度
        # 这表示用户需要更详细的信息
        if "详细" in message or "具体" in message:
            base_confidence += 0.05
        
        # 返回不超过0.99的置信度
        # 避免过度自信，留有一定容错空间
        return min(base_confidence, 0.99)
