import requests
import json
import time

class Interface_Method:
    def __init__(self, url, data, headers):
        self.url = url
        self.headers = headers
        self.data = data

    def Get_request(self):
        res = requests.get(url=self.url, headers=self.headers)
        print(res.json())
        print(f"调用GET请求，请求URL为{self.url}，请求响应为{res.status_code}")
        return res

    def Post_request(self):
        # res = requests.post(url=self.url, headers=self.headers, data=self.data)
        session = requests.Session()
        res = session.post(url=self.url, headers=self.headers, data=self.data)
        # print(f'请求返回响应：{res.json()}, 请求头为：{res.request.headers}')
        return session

    def timeflush(self):
        sum = 10  # 设置倒计时时间
        timeflush = 0.25  # 设置屏幕刷新的间隔时间
        for i in range(0, int(sum / timeflush)):
            list = ["\\", "|", "/", "—"]
            index = i % 4
            print("\r程序正在运行 {}".format(list[index]), end="")
            time.sleep(timeflush)


if __name__ == '__main__':
    url = "http://nb3.joowing.com/nebula/v3/session?session%5Blogin%5D=js1@aitiantian.com&session%5Bpassword%5D=js0909"
    data = {}
    Interface_method = Interface_Method(url=url, data=data)
    login_res = Interface_method.Post_request()

    urls = 'http://nb3.joowing.com/api/pb/aitiantian/showcase/profiles.json'
    res = login_res.get(urls)
    print(res.json())
