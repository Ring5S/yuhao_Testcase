import requests
import re, json

"""----------------登录板块----------------"""


class Login:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

    # 登录NB，JMP并返回session
    def NB_Login(self, ):
        org_code = input("输入登录NB的orgcode:")
        password = input("输入登录NB的密码:")
        # org_code = 'demo'
        # password = 'js0909'
        url = f'http://nb3.joowing.com/nebula/v3/session?session%5Blogin%5D=js1@{org_code}.com&session%5Bpassword%5D={password}'
        NB_Session = requests.Session()
        res = NB_Session.post(url=url, headers=self.headers, data=self.data)
        # print(res.request.headers)
        # print(res.json())
        # print(res.request.url)
        if res.status_code == 201:
            print('登录成功！')
            return NB_Session
        else:
            print("NB登录失败！请重试")
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'Connection': 'keep-alive'
            }
            data = {}
            # print(NB_Session)
            return Login(headers=headers, data=data).NB_Login()
            # return NB_Session

    def JMP_Login(self, ):
        uesrname = input("输入登录JMP的账号:")
        password = input("输入登录JMP的密码:")
        url = f'http://jmp.joowing.com/api/ris/sessions.json?session%5Blogin%5D={uesrname}&session%5Bpassword%5D={password}'
        JMP_Session = requests.Session()
        res = JMP_Session.post(url=url, headers=self.headers, data=self.data)
        # print(res.request.headers)
        # print(res)
        # print(res.request.url)
        if res.status_code == 200:
            print('登录成功！')
            return JMP_Session
        else:
            print("JMP登录失败！请重试")
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'Connection': 'keep-alive'
            }
            data = {}
            # print(JMP_Session)
            return Login(headers=headers, data=data).JMP_Login()
            # return JMP_Session


if __name__ == '__main__':
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Connection': 'keep-alive'
    }
    data = {}

    login = Login(headers=headers, data=data)
    session = login.NB_Login()
    print(session)
