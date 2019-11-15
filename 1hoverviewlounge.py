import requests

url = "https://api.meraki.com/api/v0/devices/Q2FV-K7QZ-K7B5/camera/analytics/overview"

headers = {
    'X-Cisco-Meraki-API-Key': "86c458f08e922045e6260cfcb06b8b76aabf2d3b",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "5d92210d-ff79-4e83-9a0a-0d42392ab562,80a59e67-f0db-49f2-ba45-593f562e54d1",
    'Accept-Encoding': "gzip, deflate",
    'Referer': "https://api.meraki.com/api/v0/devices/Q2FV-K7QZ-K7B5/camera/analytics/overview",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)
