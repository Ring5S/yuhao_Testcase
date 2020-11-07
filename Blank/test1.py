# 0、1、1、2、3、5、8、13、21、34
import json


def fib_recur():
    fib_recur = [0, 1]
    a = 1
    num = int(input("输入组数数字:"))
    for i in range(num - 2):
        fib_recur_next = fib_recur[a - 1] + fib_recur[a]
        fib_recur.append(fib_recur_next)
        # fib_recur[3] = 2
        print(fib_recur)
        a += 1
    print(f'fib_recur数列第{len(fib_recur)}组数字为{fib_recur[len(fib_recur) - 1]}')


headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    "Connection": "keep-alive",
    'content-type': 'application/json',
    'Cookie': 'jwbaby_user_id=28de5760-5161-0138-1527-165424acb931;_pomelo_session=75f8583d9d8f1328a4652d9224a43f73;',
    'Origin': 'http://127.0.0.1:32559',
    'Referer': 'https://servicewechat.com/wxa626fd2bb831c8a1/devtools/page-frame.html',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 wechatdevtools/1.03.2010240 MicroMessenger/7.0.4 Language/zh_CN webview/',
    'X-CSRF-Token': 'sA0+Qj6ciWlCMNH8wZsg/7Abu2zdswKk3zaYQPfVQSU=',
    'Content-Length': '240',
    'sec-ch-ua': 'nwjs 75',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Host': 'jwbaby.w.joowing.com'
}

url = 'https://jwbaby.w.joowing.com/org/jwbaby/orders/build_order.json'
data = {"order": {"cart_items": [
    {"sku": "4902011747577", "num": 1, "shop": "16535", "buz_type": "promotion", "buz_code": "mutex_1604307827070257",
     "buz_pid": "mutex_item_16043079306564603"}], "scene": "mall", "easy_buy": True, "address_id": None},
        "version": "2.5.4"}
data = json.dumps(data)
import requests

res = requests.post(url=url, headers=headers,data=data)
print(res, res.json())
print(res.request.headers)
