# coding=utf-8
import requests
import re, json
import tkinter.messagebox
import pymysql
from sshtunnel import SSHTunnelForwarder
from selenium import webdriver
import time
from multiprocessing import pool

headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36""",
    "Content-Type": "application/json;charset=UTF-8"
}
message = tkinter.messagebox
print("""
-------------欢迎使用豪大大JMP黑科技脚本---------------
""")

"""----------------登录板块----------------"""
data = []


def login():
    username = 'yuhao.xue'
    password = '980127xyhXYC'
    # username = input("请输入您的JMP账号：")
    # password = input("请输入您的JMP密码：")
    url = 'http://jmp.joowing.com/api/ris/sessions.json?session%5Blogin%5D={username}&session%5Bpassword%5D={password}'.format(
        username=username, password=password)
    api_Session = requests.session()
    response = api_Session.post(url=url, data=data)
    if response.status_code != 200:
        if response.json()['code'] == 'INVALID_LOGIN':
            message.showwarning(title="¿¿¿", message="自己的账号都能输错¿¿¿")
            login()
        elif response.json()['code'] == 'INVALID_PASSWORD':
            message.showwarning(title="¿¿¿", message="密码错了嗷")
            login()
        else:
            print("登录系统错误，重新试下")
            login()
    else:
        return api_Session


jmp_session = login()
for member_no in ['100563']:
    count_list = []
    org_code = 'demo'
    member_no = member_no
    c_number = 1
    serial_no = 'cp_1603181250621549'
    if serial_no:
        print("指定券号撤券")
        search_url = f'http://jmp.joowing.com/api/pb/api/v1/history/coupon_histories.json?coupon_history%5Bcoupon_type%5D=mall&coupon_history%5Bmember_no%5D={member_no}&coupon_history%5Borg_code%5D={org_code}&coupon_history%5Bserial_no%5D={serial_no}&coupon_history%5Bstate%5D=init,expired&page%5Bindex%5D=1&page%5Bsize%5D={c_number}'
        res = jmp_session.get(search_url, headers=headers)
        # print(res.request.headers)
        for couponinfo in res.json():
            id = couponinfo['id']
            recall_url = 'http://jmp.joowing.com/api/pb/jmp_api/v1/coupon_histories/{id}/recall.json'.format(id=id)
            recall_data = {"id": id}
            recall_data = json.dumps(recall_data)
            response = jmp_session.post(url=recall_url, headers=headers, data=recall_data)
            print(response.request.headers)
            print(response.json())
    else:
        for count in range(c_number):
            couponlist = 'http://jmp.joowing.com/api/pb/api/v1/history/coupon_histories.json?coupon_history%5Bcoupon_type%5D=mall&coupon_history%5Bmember_no%5D={member_no}&coupon_history%5Borg_code%5D={orgcode}&coupon_history%5Bstate%5D=init,expired&page%5Bindex%5D=1&page%5Bsize%5D={c_number}'.format(
                member_no=member_no, orgcode=org_code, c_number=c_number)
            res = jmp_session.get(url=couponlist)
            id = res.json()[count]['id']
            recall_url = 'http://jmp.joowing.com/api/pb/jmp_api/v1/coupon_histories/{id}/recall.json'.format(id=id)
            recall_data = {"id": id}
            recall_data = json.dumps(recall_data)
            response = jmp_session.post(url=recall_url, data=recall_data)
            count_list.append(response)
            a = count + 1
            b = (a / c_number) * 100
            print('\r本次共{num}个任务，已执行{done}个，当前进度：{b}%'.format(num=c_number, done=a, b='%.2f' % b), end='')
