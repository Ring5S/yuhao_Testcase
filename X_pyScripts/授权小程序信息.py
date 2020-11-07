from sshtunnel import SSHTunnelForwarder
import pymysql
from selenium import webdriver
import tkinter.messagebox
from Auto_Scripts.Interface_method import Interface_Method

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
import requests


def miniinfo():
    try:
        orgcode = input("查询商户：")
        url = f'http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?org_code={orgcode}&page%5Bindex%5D=1&page%5Bsize%5D=20&symbol=3'
        response = requests.get(url=url, headers=headers)
        authorizer_refresh_token = response.json()[0]['authorizer_refresh_token']
        authorization_appid = response.json()[0]['authorization_appid']
        print(
            f'appid 【{authorization_appid}】 orgcode【{orgcode}】 域名【https://{orgcode}.w.joowing.com】 refresh_token【{authorizer_refresh_token}】')
        # print(response.request.headers)
    except Exception as e:
        print(e)
        print("检查orgcode是否输错,或者商户未授权")
        miniinfo()

message = tkinter.messagebox

def refresh():
    a = 0
    check_refreshtime = 50
    org_code = input("输入要监控的商户code：")
    import time
    released_status = 1
    url = f'http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?org_code={org_code}&page%5Bindex%5D=1&page%5Bsize%5D=20&symbol=3'
    while released_status==1:
        res = requests.get(url, headers=headers)
        released_status = res.json()[0]['released_status']
        if released_status == 1:
            print(f"商户{org_code}审核结果未变动")
            a += 1
        else:
            message.showinfo(title="吼吼吼！",message=f"商户{org_code}已变更审核状态！！！")
            check_times = a*check_refreshtime
            check_timeh = check_times/3600
            check_timeh2f = '%.2f' % check_timeh
            print(f'审核时间为{check_timeh2f}小时')
        time.sleep(check_refreshtime)


# print(format(1.23456, '.3f'))
# check_times = 5000
# check_timeh = check_times / 3600
# check_timeh2f = '%.2f' % check_timeh
# print(f'审核时间为{check_timeh2f}小时')

# miniinfo()
refresh()