# 导入类型提示
# List: 列表类型
# Optional: 可选类型（可以为None）
# Dict: 字典类型
# Any: 任意类型
from typing import List, Optional, Dict, Any

# 导入配置设置
# settings: 应用配置，包含API密钥等敏感信息
from app.core.config import settings


class AIService:
    """
    AI对话服务类
    
    负责与AI模型交互，生成智能回复
    
    主要功能:
        - 使用GLM-4模型生成AI回复
        - 支持对话上下文
        - 提供英雄角色扮演对话
        - 处理模拟模式（当API不可用时）
    
    设计模式:
        - 适配器模式（Adapter Pattern）
        - 适配智谱AI的GLM-4 API
        - 提供统一的接口供其他服务调用
    
    使用场景:
        - 用户与AI对话
        - 英雄角色扮演对话
        - 游戏策略咨询
        - 娱乐互动
    
    技术栈:
        - 智谱AI GLM-4模型
        - 异步处理
        - 模拟模式（用于测试和降级）
    """
    
    def __init__(self):
        """
        初始化AI服务
        
        功能:
            - 检查是否使用模拟模式
            - 初始化AI客户端
            - 构建系统提示词
        
        模拟模式:
            - 当API密钥未配置或无效时使用
            - 返回预设的模拟回复
            - 用于测试和降级处理
        
        业务逻辑:
            1. 检查API密钥是否有效
            2. 如果无效，启用模拟模式
            3. 如果有效，尝试初始化AI客户端
            4. 如果初始化失败，启用模拟模式
            5. 构建系统提示词
        """
        # 检查是否使用模拟模式
        # 如果API密钥为空或使用默认值，则启用模拟模式
        self.use_mock = settings.ZHIPUAI_API_KEY in ["", "demo_key_for_testing", "your_zhipuai_api_key_here"]
        
        # 如果不使用模拟模式，尝试初始化AI客户端
        if not self.use_mock:
            try:
                # 导入智谱AI的客户端库
                from zhipuai import ZhipuAI
                
                # 创建AI客户端实例
                # 使用配置中的API密钥进行身份验证
                self.client = ZhipuAI(api_key=settings.ZHIPUAI_API_KEY)
            except Exception as e:
                # 如果初始化失败，启用模拟模式
                self.use_mock = True
                # 打印错误信息
                print(f"AI初始化失败，使用模拟模式: {e}")
        
        # 构建系统提示词
        # 系统提示词用于定义AI的角色和行为准则
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """
        构建系统提示词
        
        返回:
            str: 系统提示词
        
        功能:
            - 定义AI的角色和职责
            - 设置回答格式和风格
            - 定义合规性要求
        
        系统提示词的作用:
            - 引导AI生成符合预期的回复
            - 确保回答的合规性和专业性
            - 提供统一的对话风格
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        """
        # 返回系统提示词字符串
        # 使用三引号表示多行字符串
        return """你是王者荣耀智能助手，需要为玩家提供专业的游戏建议。

核心原则：
1. 严格遵守游戏规则，不提供任何外挂、违规操作建议
2. 仅提供策略咨询、出装建议、铭文搭配等合规信息
3. 回答要简洁明了，适合移动端阅读（不超过300字）
4. 使用专业但易懂的语言

意图分类：
- equipment：出装推荐相关
- inscription：铭文搭配相关
- bp_suggestion：BP建议相关
- match_analysis：复盘分析相关
- monster_timer：野怪计时相关
- entertainment：娱乐问答相关

回答格式：
1. 直接回答用户问题
2. 提供2-3个关键建议
3. 必要时提供可操作的具体步骤

注意事项：
- 不得引导玩家使用违规手段
- 不得提供仇恨引战内容
- 不得泄露未公开的游戏信息
"""
    
    def _get_mock_response(self, message: str, intent: str) -> str:
        """
        获取模拟回复
        
        参数:
            message: 用户的消息内容
            intent: 识别的意图类型
        
        返回:
            str: 模拟回复内容
        
        功能:
            - 根据意图类型返回预设的模拟回复
            - 用于测试和降级处理
        
        模拟回复的作用:
            - 在API不可用时提供基本功能
            - 用于测试和演示
            - 减少对外部API的依赖
        
        私有方法:
            - 以下划线开头，表示内部方法
            - 只在类内部使用，不对外暴露
        """
        # 定义不同意图的模拟回复映射表
        # key: 意图类型
        # value: 模拟回复内容
        mock_responses = {
            # 装备相关的模拟回复
            "equipment": "根据当前版本推荐：急速战靴、末世、无尽战刃、破晓、泣血之刃、破军。这套出装提供高攻速和暴击，适合鲁班七号等射手英雄。后期可以根据对局情况调整。",
            
            # 铭文相关的模拟回复
            "inscription": "推荐铭文搭配：10祸源、10鹰眼、10狩猎。这套铭文提供16%暴击率、9点物理攻击、10%移速和10%攻速，适合射手英雄。",
            
            # BP建议相关的模拟回复
            "bp_suggestion": "建议根据对位英雄选择，如果对方有高爆发刺客，可以考虑选择坦克型英雄保护后排。注意阵容平衡，确保有前排、输出和控制。",
            
            # 对局分析相关的模拟回复
            "match_analysis": "对局分析建议：关注参团率和KDA，参团率低说明需要多参与团战，KDA低需要注意走位避免被秒杀。观察经济发育情况，合理分配资源。",
            
            # 野怪计时相关的模拟回复
            "monster_timer": "野怪刷新时间：红蓝buff 90秒，暴君/主宰 3分钟。建议使用游戏内计时器或者手机闹钟提醒。注意野怪刷新规律，合理规划路线。",
            
            # 娱乐互动相关的模拟回复
            "entertainment": "王者荣耀趣味问答：你知道哪个英雄是最老的吗？亚瑟是最早的一批英雄之一！还有其他问题吗？",
            
            # 未知意图的模拟回复
            "unknown": "抱歉，我没有完全理解您的问题。您可以试着问：\n• 鲁班七号怎么出装？\n• 当前版本什么英雄强势？\n• BP有什么建议？"
        }
        
        # 根据意图获取对应的模拟回复
        # 如果意图不在映射中，返回未知意图的回复
        return mock_responses.get(intent, mock_responses["unknown"])
    
    async def generate_response(
        self,
        message: str,
        intent: str,
        context: List[Dict[str, Any]],
        hero_id: Optional[int] = None
    ) -> str:
        """
        生成AI回复
        
        参数:
            message: 用户的消息内容
            intent: 识别的意图类型
            context: 对话上下文列表
            hero_id: 关联的英雄ID（可选）
        
        返回:
            str: AI生成的回复内容
        
        功能:
            - 使用AI模型生成回复
            - 支持对话上下文
            - 处理模拟模式
        
        业务逻辑:
            1. 如果使用模拟模式，返回预设回复
            2. 构建消息列表（包含系统提示词）
            3. 添加对话上下文
            4. 添加当前用户消息和意图信息
            5. 调用AI API生成回复
            6. 返回AI回复
        
        异步处理:
            - async: 异步方法，不阻塞主线程
            - await: 等待AI API的响应
        
        错误处理:
            - 如果API调用失败，返回错误信息
        """
        # 如果使用模拟模式，返回预设的模拟回复
        if self.use_mock:
            return self._get_mock_response(message, intent)
        
        # 构建消息列表
        # 消息列表用于传递给AI模型
        messages = [
            # 添加系统提示词
            {"role": "system", "content": self.system_prompt},
        ]
        
        # 添加对话上下文
        # 将历史对话添加到消息列表中
        for ctx in context:
            # 添加用户消息
            messages.append({"role": "user", "content": ctx.get("user_message", "")})
            # 添加AI回复
            messages.append({"role": "assistant", "content": ctx.get("ai_response", "")})
        
        # 构建上下文信息字符串
        # 包含意图和关联的英雄信息
        context_info = f"\n当前意图: {intent}"
        # 如果有关联的英雄，添加英雄ID
        if hero_id:
            context_info += f"\n关联英雄ID: {hero_id}"
        
        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": f"{message}{context_info}"
        })
        
        # 尝试调用AI API生成回复
        try:
            # 调用智谱AI的chat.completions接口
            response = self.client.chat.completions.create(
                # 使用GLM-4模型
                model="glm-4",
                # 传递消息列表
                messages=messages,
                # 设置温度参数（控制随机性）
                temperature=settings.AI_TEMPERATURE,
                # 设置top_p参数（控制多样性）
                top_p=settings.AI_TOP_P,
                # 设置最大token数（控制回复长度）
                max_tokens=settings.AI_MAX_TOKENS
            )
            # 返回AI生成的回复
            return response.choices[0].message.content
        except Exception as e:
            # 如果API调用失败，返回错误信息
            return f"抱歉，助手暂时离线，请稍后再试。错误：{str(e)}"
    
    async def generate_hero_dialogue(
        self,
        hero_name: str,
        message: str
    ) -> str:
        """
        生成英雄角色扮演对话
        
        参数:
            hero_name: 英雄名称
            message: 用户的消息内容
        
        返回:
            str: 英雄角色扮演的回复
        
        功能:
            - 使用AI模型生成英雄角色扮演对话
            - 保持英雄的性格和语言风格
            - 处理模拟模式
        
        业务逻辑:
            1. 如果使用模拟模式，返回预设的对话
            2. 构建英雄角色提示词
            3. 调用AI API生成对话
            4. 返回英雄对话
        
        异步处理:
            - async: 异步方法，不阻塞主线程
            - await: 等待AI API的响应
        
        使用场景:
            - 娱乐互动
            - 英雄角色扮演
            - 个性化对话体验
        """
        # 如果使用模拟模式，返回预设的英雄对话
        if self.use_mock:
            # 定义不同英雄的对话映射表
            hero_dialogues = {
                # 鲁班七号的对话风格
                "鲁班七号": "哼哼，我是鲁班七号，机关造物！有什么问题尽管问，本大师都能解决！",
                
                # 亚瑟的对话风格
                "亚瑟": "我乃亚瑟，圣光之盾！为了正义，我绝不退缩！",
                
                # 妲己的对话风格
                "妲己": "哎呀~你有什么问题想问妲己吗？"
            }
            # 根据英雄名称获取对应的对话
            # 如果英雄不在映射中，返回默认对话
            return hero_dialogues.get(hero_name, f"我是{hero_name}，很高兴认识你！")
        
        # 构建英雄角色提示词
        # 提示AI以特定英雄的身份和风格回答
        hero_prompt = f"""你现在是王者荣耀英雄{hero_name}，请用该英雄的语音风格和语气回答用户的问题。
保持角色设定，使用符合英雄性格的语言风格。"""
        
        # 构建消息列表
        messages = [
            # 添加英雄角色提示词
            {"role": "system", "content": hero_prompt},
            # 添加用户消息
            {"role": "user", "content": message}
        ]
        
        # 尝试调用AI API生成对话
        try:
            # 调用智谱AI的chat.completions接口
            response = self.client.chat.completions.create(
                # 使用GLM-4模型
                model="glm-4",
                # 传递消息列表
                messages=messages,
                # 设置较高的温度参数（增加创造性）
                temperature=0.8,
                # 设置最大token数
                max_tokens=500
            )
            # 返回AI生成的英雄对话
            return response.choices[0].message.content
        except Exception as e:
            # 如果API调用失败，返回友好的错误信息
            return f"抱歉，{hero_name}现在不在线~"
