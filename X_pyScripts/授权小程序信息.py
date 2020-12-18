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
    # 设置监控间隔时间
    check_refreshtime = 30
    org_code = input("输入要监控的商户code：")
    import time
    released_status = 1
    url = f'http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?org_code={org_code}&page%5Bindex%5D=1&page%5Bsize%5D=20&symbol=3'
    while released_status == 1:
        res = requests.get(url, headers=headers)
        released_status = res.json()[0]['released_status']
        if released_status == 1:
            # print(f"商户{org_code}审核结果未变动")
            a += 1
        else:
            message.showinfo(title="吼吼吼！", message=f"商户{org_code}已变更审核状态！！！")
            check_times = a * check_refreshtime
            check_timeh = check_times / 3600
            check_timeh2f = '%.2f' % check_timeh
            print(f'审核时间为{check_timeh2f}小时')
        time.sleep(check_refreshtime)


def search_app():
    import json, requests
    url = "http://jmp.joowing.com/rbj/api/wxopen/release"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    release_version = input("要推送的小程序版本：")
    s_url = "http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?auth_status=1&page%5Bindex%5D=1&page%5Bsize%5D=1000&symbol=3"
    # s_url = "http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?org_code=demo&page%5Bindex%5D=1&page%5Bsize%5D=20&symbol=3"
    res = requests.get(s_url)
    for info in res.json():
        a = 0
        list = []
        org_code = info["org_code"]
        appid = info["authorization_appid"]
        plugins = info["plugins"]
        # print(plugins)
        data = {"release": {"authorization_appid": appid, "release_version": release_version}}
        data = json.dumps(data)
        if len(plugins) > 0:
            for plugins in plugins:
                if "nickname" in plugins.keys() and plugins["nickname"] == "小程序直播组件":
                    print(f"{org_code}该商户检测到存在直播插件")
                    list.append(plugins["nickname"])
                else:
                    # print(f"{org_code}该商户本轮检测不存在直播插件")
                    pass
                    # data["release"]["release_version"] = f"{release_version}b"
                    # res2 = requests.post(url, data=data, headers=headers)
                    # print(res2)
                    # if res2.status_code == 200:
                    #     a += 1
            if "小程序直播组件" in list:
                res1 = requests.post(url, data=data, headers=headers)
                print(res1)
                if res1.status_code == 200:
                    a += 1
            else:
                print(f"{org_code}该商户不存在直播插件")
                data["release"]["release_version"] = f"{release_version}b"
                res2 = requests.post(url, data=data, headers=headers)
                print(res2)
                if res2.status_code == 200:
                    a += 1
        else:
            print(f"{org_code}该商户不存在直播插件")
            if_live = False
            data["release"]["release_version"] = f"{release_version}b"
            res3 = requests.post(url, data=data, headers=headers)
            print(res3)
            if res3.status_code == 200:
                a += 1
    print("本次推送共{}个商户小程序，{}个成功推送".format(len(res.json()), a))


search_app()
# miniinfo()
refresh()
