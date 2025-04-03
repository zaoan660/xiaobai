import time
from openai import OpenAI
from app.common import log, conf


class DashScopeClient:
    def __init__(self):
        self.api_key = conf.DASHSCOPE_API_KEY
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        log.info(f"DashScope客户端初始化成功")

    def chat_completion(self, message):
        start_time = time.time()
        
        completion = self.client.chat.completions.create(
            model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {
                    "role": "system",
                    "content": "你是一个行为像人的机器人助手, 你的回答应该像人类一样简短, 但是当察觉到我情绪明显时(比如, 很开心, 很低落 这样的极端情绪), 你应该回答的热情一点.",
                },
                {
                    "role": "system",
                    "content": "现在的时间是: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            stream=True,
            stream_options={"include_usage": True},
        )
        
        full_content = ""
        first_token = True
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                if first_token:
                    first_token_time = time.time()
                    log.info(f"首字等待时间: {first_token_time - start_time:.4f} 秒")
                    first_token = False
                full_content += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content



dashscope_client = DashScopeClient()