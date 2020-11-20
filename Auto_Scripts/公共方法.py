import requests
import re, json
import pymysql
from sshtunnel import SSHTunnelForwarder

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
        NB_Session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'})
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
            return Login.NB_Login()
            # return NB_Session

    def JMP_Login(self, ):
        # uesrname = input("输入登录JMP的账号:")
        # password = input("输入登录JMP的密码:")
        uesrname = "yuhao.xue"
        password = "980127xyhXYC"
        url = f'http://jmp.joowing.com/api/ris/sessions.json?session%5Blogin%5D={uesrname}&session%5Bpassword%5D={password}'
        JMP_Session = requests.Session()
        res = JMP_Session.post(url=url, headers=self.headers, data=self.data)
        # print(res.request.headers)
        # print(res)
        # print(res.request.url)
        if res.status_code == 200:
            print('JMP登录成功！')
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

    def Sql_Connect(self):
        server = SSHTunnelForwarder(
            ('222.73.36.230', 2002),  # 跳板机ip及端口
            ssh_password='980127xyhXYC',  # 跳板机密码
            ssh_username='yuhao.xue',  # 跳板机用户名
            remote_bind_address=('rm-uf6f05k2rg95s23bp.mysql.rds.aliyuncs.com', 3306))  # 连接的数据库地址及端口
        server.start()
        db_connect = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                     port=server.local_bind_port,  # 默认，无需修改
                                     user='chong_chen_st',  # 连接的数据库用户名
                                     passwd='rdvYPB3cX4XbUYhwmQzj',  # 连接的数据库密码
                                     db='ris_production')  # 连接的数据库名称
        # print(db_connect)
        cursor = db_connect.cursor()
        # print(1)
        # print(cursor)
        return cursor, db_connect


if __name__ == '__main__':
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Connection': 'keep-alive'
    }
    data = {}

    login = Login(headers=headers, data=data)

    # session = login.NB_Login()
    # print(session.headers)
    # url = 'http://nb3.joowing.com/nebula/v3/red_envelope/pay_config'
    # res = session.get(url=url)
    # print(res.request.headers)
    cursor_result = login.Sql_Connect()
    # print(cursor_result)
    cursor = cursor_result[0]
    connect = cursor_result[1]
    SQL = """SELECT
REPLACE(json_extract(plugins,'$[*].nickname'),'"','') 
FROM ris_production.mini_programs
where org_code in ('xtaed')"""
    # cursor.execute(SQL)
    # result = cursor.fetchall()
    # print(result)
    # for i in result:
    #     print(i)
    #     if re.search('小程序直播组件',str(i)):
    #         print("OK!")
    #     print(type(i))
    #     a=list(i)[0]
    #     print(a)
    # cursor.close()
    # connect.close()

    list1 = []
    list2 = []
    for i in range(100):
        list1.append(i)
    for i in range(50, 100):
        list2.append(i)

    list3 = list(set(list2 + list1))
    for i in range(len(list3) - 1):
        print(i, end=",")
    # a = str(list3)
    # print(re.)
