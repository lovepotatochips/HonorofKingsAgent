import urllib.request
import json

url = "http://localhost:8000/api/v1/analysis/analyze"
data = {
    "match_id": "match_0_user_177",
    "user_id": "user_1771059406553_demo"
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        print(f"状态码: {response.status}")
        print(f"响应: {content}")
except Exception as e:
    print(f"请求失败: {e}")
