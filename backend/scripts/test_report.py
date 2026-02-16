import urllib.request
import json

url = "http://localhost:8000/api/v1/analysis/report/50ec69a8-8e6f-4fe0-970c-9a41b7a97966"

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
        print(f"状态码: {response.status}")
        print(f"响应: {content}")
except Exception as e:
    print(f"请求失败: {e}")
