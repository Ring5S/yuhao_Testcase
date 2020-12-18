# coding=utf-8
import requests
import re, json
import tkinter.messagebox
import pymysql
from sshtunnel import SSHTunnelForwarder
from selenium import webdriver
import time
from multiprocessing import pool

message = tkinter.messagebox
print("""
-------------欢迎使用豪大大JMP黑科技脚本---------------
""")

"""----------------登录板块----------------"""
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
p_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    'Host': 'jmp.joowing.com',
    'Connection': 'keep-alive'
}
data = []


def login():
    username = 'yuhao.xue'
    password = '980127xyhXYC'
    # username = input("请输入您的JMP账号：")
    # password = input("请输入您的JMP密码：")
    url = 'http://jmp.joowing.com/api/ris/sessions.json?session%5Blogin%5D={username}&session%5Bpassword%5D={password}'.format(
        username=username, password=password)
    response = requests.post(headers=headers, url=url, data=data)
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
        cookie = response.headers['set-cookie']
        print(
            """--------------登录成功！请输入数字操作指令-----------------
               0：退出黑科技脚本
               1：黑账户（弹窗+打印URL）
               2：批量撤券（一次撤销指定会员指定数量的券，仅对接ERP撤券接口可用，慎用）
               3：同步门店配送方式（开户小组需求，导入门店后自动对齐配送方式，保持其他数据不变）
               4：小程序管理-商户导入
               5：JMP小程序体验版二维码获取
               6：小程序授权appid扫描检测
               7：商户数据库信息查询
        ------------------------------------------------------
            """
        )
        return cookie


cookie = login()
# response = login()
"""--------------获取动态cookie-----------------------"""
cookie = re.sub('Path=/', '', cookie)
cookie = re.sub(',', '', cookie)
cookie = re.sub(cookie.split(';')[1], '', cookie)
cookie = re.sub(cookie.split(';')[2], '', cookie)
# cookie = response.cookies
# cookie = requests.utils.dict_from_cookiejar(cookie)
# cookie = json.dumps(cookie)
# print(cookie, type(cookie))
headers['Cookie'] = cookie
p_headers['Cookie'] = cookie


# -----------操作命令----------------
def SQL_Excute(SQL):
    with SSHTunnelForwarder(
            ('222.73.36.230', 2002),  # 跳板机ip及端口
            ssh_password='980127xyhXYC',  # 跳板机密码
            ssh_username='yuhao.xue',  # 跳板机用户名
            remote_bind_address=('rm-uf6f05k2rg95s23bp.mysql.rds.aliyuncs.com', 3306)) as server:  # 连接的数据库地址及端口
        # sever.start()
        db_connect = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                     port=server.local_bind_port,  # 默认，无需修改
                                     user='chong_chen_st',  # 连接的数据库用户名
                                     passwd='rdvYPB3cX4XbUYhwmQzj',  # 连接的数据库密码
                                     db='ris_production')  # 连接的数据库名称
        # print(db_connect)
        cursor = db_connect.cursor()
        cursor.execute(SQL)
        data = cursor.fetchall()
        # print(data)
        cursor.close()
        # db_connect.close()
        return data


def check_id():
    SQL1 = """
    SELECT org_code,authorization_appid FROM ris_production.mini_programs
    where auth_status=1
    """
    org_list = []
    list_id = []
    data = SQL_Excute(SQL1)
    for count in range(len(data)):
        orgcode = data[count][0]
        id = data[count][1]
        org_list.append(orgcode)
        list_id.append(id)
    # print(org_list)
    # print(list_id)

    SQL2 = f"SELECT org_code,weapp_app_id FROM pomelo_backend_production.nebula_config_wx_public_configs where org_code in {tuple(org_list)}"
    # print(SQL2)

    check_id_list = []
    check_org_list = []

    data = SQL_Excute(SQL2)
    for count in range(len(data)):
        orgcode = data[count][0]
        id = data[count][1]
        check_org_list.append(orgcode)
        check_id_list.append(id)

    # print(check_org_list)
    # print(check_id_list)

    Unqualified_list = []
    Unqualified_code = []

    """
    用NB的配置ID和JMP的id进行遍历对比，将不匹配的筛选出来
    """

    for id, org_code in zip(check_id_list, check_org_list):
        if id in list_id:
            pass
        else:
            Unqualified_list.append(f"{org_code}:{id}")
            Unqualified_code.append(org_code)
    print(f"检测授权Id和NB配置的独立小程序不一致的商户清单：{Unqualified_list}")
    SQL3 = f"""
    SELECT * FROM ris_production.mini_programs
    where auth_status=1
    and org_code not in{tuple(Unqualified_code)}
    """
    # 此SQL为公网正确授权的小程序清单
    print(f"此SQL为公网正确授权的小程序清单:{SQL3}")


def recall_coupon():
    from Auto_Scripts.Interface_method import Interface_Method
    org_code = input("org_code:")
    Interface_Method = Interface_Method(url=1,data={})
    member_no_info = Interface_Method.query_by_phone_or_member_no(org_code)
    member_no = member_no_info['member_no']
    count_list = []
    c_number = int(input("输入要撤的券数量："))
    serial_no = input("指定撤券的券号，不填默认按照数量进行撤券：")
    if serial_no:
        print(f"本次撤券为指定券号撤券，券号为{serial_no}")
        search_url = f'http://jmp.joowing.com/api/pb/api/v1/history/coupon_histories.json?coupon_history%5Bcoupon_type%5D=mall&coupon_history%5Bmember_no%5D={member_no}&coupon_history%5Borg_code%5D={org_code}&coupon_history%5Bserial_no%5D={serial_no}&coupon_history%5Bstate%5D=init,expired&page%5Bindex%5D=1&page%5Bsize%5D={c_number}'
        res = requests.get(search_url, headers)
        for couponinfo in res.json():
            state = couponinfo['state']
            if state == '未使用':
                id = couponinfo['id']
                recall_url = 'http://jmp.joowing.com/api/pb/jmp_api/v1/coupon_histories/{id}/recall.json'.format(id=id)
                recall_data = {"id": id}
                recall_data = json.dumps(recall_data)
                response = requests.post(url=recall_url, headers=headers, data=recall_data)
                print(response.json())
            else:
                print(f'券状态为{state}，过滤')
    else:
        check_instructions = input(f"本次撤券为无差别撤券，按页面顺序撤{c_number}张券，是否确认执行? y/n\n")
        if check_instructions == 'y':
            pass
        else:
            recall_coupon()
        for count in range(c_number):
            couponlist = 'http://jmp.joowing.com/api/pb/api/v1/history/coupon_histories.json?coupon_history%5Bcoupon_type%5D=mall&coupon_history%5Bmember_no%5D={member_no}&coupon_history%5Borg_code%5D={orgcode}&coupon_history%5Bstate%5D=init,expired&page%5Bindex%5D=1&page%5Bsize%5D={c_number}'.format(
                member_no=member_no, orgcode=org_code, c_number=c_number)
            res = requests.get(url=couponlist, headers=headers)
            id = res.json()[count]['id']
            recall_url = 'http://jmp.joowing.com/api/pb/jmp_api/v1/coupon_histories/{id}/recall.json'.format(id=id)
            recall_data = {"id": id}
            recall_data = json.dumps(recall_data)
            response = requests.post(url=recall_url, headers=headers, data=recall_data)
            count_list.append(response)
            a = count + 1
            b = (a / c_number) * 100
            print('\r本次共{num}个任务，已执行{done}个，当前进度：{b}%'.format(num=c_number, done=a, b='%.2f' % b), end='')


def hackinfo():
    print("商户必填，手机号会员号有哪个填哪个就行，另一个可以直接回车掉")
    org_code = input('商户code：')
    phone = input('手机号：')
    member_no = input('会员号：')
    if phone:
        SQL = "SELECT seq FROM ris_production.members where org_code='{code}' and phone='{phone}'".format(code=org_code,
                                                                                                          phone=phone)
    else:
        SQL = "SELECT seq FROM ris_production.members where org_code='{code}' and member_no='{member_no}'".format(
            code=org_code, member_no=member_no)
    # 直接链接到业务库，切记关闭
    with SSHTunnelForwarder(
            ('222.73.36.230', 2002),  # 跳板机ip及端口
            ssh_password='980127xyhXYC',  # 跳板机密码
            ssh_username='yuhao.xue',  # 跳板机用户名
            remote_bind_address=('rm-uf6f05k2rg95s23bp.mysql.rds.aliyuncs.com', 3306),
    local_bind_address=('0.0.0.0',22)) as server:  # 连接的数据库地址及端口

        db_connect = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                     port=server.local_bind_port,  # 默认，无需修改
                                     user='chong_chen_st',  # 连接的数据库用户名
                                     passwd='rdvYPB3cX4XbUYhwmQzj',  # 连接的数据库密码
                                     db='ris_production')  # 连接的数据库名称
        # print(db_connect)
        cursor = db_connect.cursor()
        cursor.execute(SQL)
        data = cursor.fetchone()
        # print(data)
        if data == None:
            message.showwarning(title="？？", message="确认一下会员嗷")
            hackinfo()
        usr = (data[0])
        print(usr)
        cursor.close()
        db_connect.close()

    url = 'https://{org_code}.w.joowing.com/org/{org_code}/home_page?with_tabs=1&usr={usr}'.format(org_code=org_code,
                                                                                                   usr=usr)
    print(url)
    driver = webdriver.Chrome("D:\PyCharm Community Edition 2020.2.1\chromedriver.exe")
    driver.get(url)
    print(url)
    time.sleep(30)


def shop_synchronization():
    count_list = []
    org_code = input("请输入需要同步门店配送方式的商户：")
    url = 'http://jmp.joowing.com/api/ris/org/{orgcode}/shops.json?page%5Bindex%5D=1&page%5Bsize%5D=1000'.format(
        orgcode=org_code)
    res = requests.get(url, headers=headers)
    shopinfo = res.json()
    shopnum = len(shopinfo)
    print(shopnum)
    for count in range(shopnum):
        id = shopinfo[count]['id']
        shop_type = shopinfo[count]['shop_type']
        data = shopinfo[count]
        data['omni_channel'] = True
        data['common'] = True
        data['need_data_analysis'] = True
        data['partner'] = False
        if shop_type == 'virtuality':
            data['delivery_methods'] = [6]
        elif shop_type == 'offline':
            data['delivery_methods'] = [2, 1]
        Request_URL = 'http://jmp.joowing.com/api/ris/org/{orgcode}/shops/{id}'.format(orgcode=org_code, id=id)
        data1 = {
            "shop": data
        }
        data = json.dumps(data1)
        response = requests.put(Request_URL, data=data, headers=p_headers)
        count_list.append(response)
        a = count + 1
        b = (a / len(shopinfo)) * 100
        if response.status_code == 200:
            print('\r本次共{num}个任务，已执行{done}个，当前进度：{b}%'.format(num=len(shopinfo), done=a, b='%.2f' % b), end='')
        else:
            print(f"商户{org_code}同步门店接口异常，同步门店ID为{id}")


def add_miniprogram():
    url = 'http://jmp.joowing.com/rbj/api/wxopen/mini_programs/create.json'
    """
    注意：这里的org列表和name列表对应的是商户表，一定要一一对应!如果不确定的来问我
    例：
    SELECT code,name FROM  ris_production.global_retailers
    where code in('demo')

    """
    orgcode_list = ['demo']
    retailer_name_list = ['demo']
    for orgcode, retailer_name in zip(orgcode_list, retailer_name_list):
        data = {"mini_program": {"org_code": "{orgcode}".format(orgcode=orgcode),
                                 "retailer_name": "{retailer_name}".format(retailer_name=retailer_name)}}
        data = json.dumps(data)
        Pres = requests.post(url=url, headers=p_headers, data=data)
        print(Pres.json())
        time.sleep(0.2)


def DownloadEX_png():
    import urllib.request
    orgcode = input("体验版二维码查询商户：")
    url = f'http://jmp.joowing.com/rbj/api/wxopen/mini_programs.json?org_code={orgcode}&page%5Bindex%5D=1&page%5Bsize%5D=20&symbol=3'

    response = requests.get(url=url, headers=headers)
    try:
        experience_qrcode_url = response.json()[0]['experience_qrcode_url']
        urllib.request.urlretrieve(experience_qrcode_url, filename=f'{orgcode}体验版二维码.png')
        print("二维码下载完成,需刷新文件夹")
    except Exception as e:
        print(e)
        print("检查orgcode是否输错,或者商户未授权")


def Search_database_agents():
    orgcode = input("需要查询数据库信息的商户：")
    url = f'http://jmp.joowing.com/api/crm/database_agents/{orgcode}/configs.json?page%5Bindex%5D=1&page%5Bsize%5D=20'
    response = requests.get(url=url, headers=headers)
    datebaseinfo = response.json()[0]
    print(f"""
数据库类型：{datebaseinfo['database_type']}
用户名：{datebaseinfo['username']}
连接密码：{datebaseinfo['password']}
host：{datebaseinfo['host']}
端口号：{datebaseinfo['port']}
datebase：{datebaseinfo['database']}
""")


def operation():
    try:
        operating_number = int(input("\n输入数字指令："))
    except:
        message.showerror(title="错误", message="必须输入数字！")
        operation()
    if operating_number == 1:
        hackinfo()
        time.sleep(0.2)
        operation()
    elif operating_number == 2:
        recall_coupon()
        time.sleep(0.2)
        operation()
    elif operating_number == 3:
        shop_synchronization()
        time.sleep(0.2)
        operation()
    elif operating_number == 4:
        add_miniprogram()
        time.sleep(0.2)
        operation()
    elif operating_number == 5:
        DownloadEX_png()
        time.sleep(0.2)
        operation()
    elif operating_number == 6:
        check_id()
        time.sleep(0.2)
        operation()
    elif operating_number == 7:
        Search_database_agents()
        operation()
    elif operating_number == 0:
        print("""
        ------------感谢您的使用，记得五星好评嗷亲----------------
        """)
        exit()
    else:
        print("未找到匹配的命令项！")
        time.sleep(1)
        operation()


operation()
