import requests
import json
import time


class Interface_Method:
    def __init__(self, url, data):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'Connection': 'keep-alive'
        }
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

    def query_by_phone_or_member_no(self, org_code):
        self.org_code = org_code
        member_info = input("member_info:")
        member_info_url = f'http://jmp.joowing.com/api/ris/spi/{self.org_code}/members/query_by_phone_or_member_no?page%5Bindex%5D=1&page%5Bsize%5D=20&phone_or_member_no={member_info}'
        res = requests.get(url=member_info_url, headers=self.headers)
        if res.status_code != 200:
            print("会员信息查询接口异常")
            return Interface_method.query_by_phone_or_member_no()
        else:
            if res.json() == []:
                print("未查询到会员信息！")
                return Interface_method.query_by_phone_or_member_no()
            else:
                return res.json()[0]

    def timeflush(self):
        sum = 10  # 设置倒计时时间
        timeflush = 0.25  # 设置屏幕刷新的间隔时间
        for i in range(0, int(sum / timeflush)):
            list = ["\\", "|", "/", "—"]
            index = i % 4
            print("\r程序正在运行 {}".format(list[index]), end="")
            time.sleep(timeflush)


if __name__ == '__main__':
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Connection': 'keep-alive'
    }
    url = "http://nb3.joowing.com/nebula/v3/session?session%5Blogin%5D=js1@aitiantian.com&session%5Bpassword%5D=js0909"
    data = {}
    Interface_method = Interface_Method(url=url, data=data)
    res = Interface_method.query_by_phone_or_member_no()
    print(res)
