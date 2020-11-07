# -*- coding: utf-8 -*-
import xlrd
import requests
import re, json
import tkinter.messagebox
import time
import xlwt
from datetime import date, datetime

fail_List = []
on_env = 'http://jmp.joowing.com'
test03_env = 'https://jmp-test03.joowing.com'
Cookie = 'SESSION=1b34ce71-dbfb-44fd-9fc4-d0467b63f4b1; JSESSIONID=node0i39pwyo0dz69szqjl3ym4hlu38.node0; login=xyh%40demo.com; retailer-jwt=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoieHloQGRlbW8uY29tIiwidXNlcl9hdHRyaWJ1dGVzIjp7fSwiZXhwIjoxNjAwNDI4NTk4fQ.tGprsS5GXbFugi1cty-sZv0FoA7fsOBQ4zCMiYy2zFQ; _newbee_session=BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJWI3MjgzMjYxMjQzZjZkNTFkZWVmYjU0YmYwNDgwZWI1BjsAVEkiDHVzZXJfaWQGOwBGaQLIokkiD2V4cGlyZXNfYXQGOwBGVTogQWN0aXZlU3VwcG9ydDo6VGltZVdpdGhab25lWwhJdToJVGltZQ1KIh7AVMupdwk6DW5hbm9fbnVtaQKsAzoNbmFub19kZW5pBjoNc3VibWljcm8iBpQ6CXpvbmVJIghVVEMGOwBGSSIMQmVpamluZwY7AFRJdTsHDVIiHsBUy6l3CTsIaQKsAzsJaQY7CiIGlDsLSSIIVVRDBjsARkkiDW5lYnVsYS0zBjsARlQ%3D--9fe3f7a1740a1519770b25b3b1597469c8bce213; joowing-session=49c7e1a6b354161c71dbdf9a12749a44'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Cookie': Cookie
}
p_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Content-Length': '45',
    'Cookie': Cookie
}

sendlist = []
memberinfo_list = []
org_code = "demo"
# 打开文件
try:
    workbook = xlrd.open_workbook(r'C:/Users/DELL/Desktop/man_coupon1.xlsx')
except Exception as e:
    messagebox = tkinter.messagebox
    messagebox.showwarning(title="warn", message=e)
    exit()
# 获取所有sheet

sheet_index = workbook.sheet_by_index(0)  # sheet索引从0开始
# print(sheet_index.name,sheet_index.nrows,sheet_index.ncols)
rows = sheet_index.row_values(2)  # 获取第1行内容
cols = sheet_index.col_values(0)  # 获取第1列内容


# print(rows, cols)

def Datetype():
    if rows[2]:
        print("有效天数不为空,按照天数发券")
        return "by_day"
    else:
        print("有效天数为空，按照日期发券")
        return "by_date"


# 先判定发券按照有效期发还是按照天数发
Datetype = Datetype()

'''
遍历读取表格中的信息，将信息填入请求体，发送请求命令
'''

for count in range(2, len(cols)):
    if int(sheet_index.row_values(0)[1]) == 1:
        phone = sheet_index.row_values(count)[1]
        member_type = "phone"
        member_no = ""
        member_data = {"org_code": "{org_code}".format(org_code=org_code),
                       "phone": "{phone}".format(phone=phone)}
        member_data = json.dumps(member_data)
    elif int(sheet_index.row_values(0)[1]) == 2:
        phone = ""
        member_no = sheet_index.row_values(count)[1]
        member_type = "member_nos"
        member_data = {"org_code": "{org_code}".format(org_code=org_code),
                       "member_no": "{member_no}".format(member_no=member_no)}
        member_data = json.dumps(member_data)
    serial_no = sheet_index.row_values(count)[0]

    send_num = sheet_index.row_values(count)[5]
    # print("券数量：", send_num)
    # 判定会员信息为会员号还是手机号
    sendlist.append(serial_no)
    if eval(sheet_index.row_values(0)[1]) == 1:
        phone = sheet_index.row_values(count)[1]
        member_no = ""
        sendlist.append(phone)
    elif eval(sheet_index.row_values(0)[1]) == 2:
        phone = ""
        member_no = sheet_index.row_values(count)[1]
        sendlist.append(member_no)

    member_info_url = 'http://jmp.joowing.com/api/ris/spi/demo/members/__query'
    serialinfo_url = 'http://jmp.joowing.com/api/pb/api/v1/promotion/coupon_definitions.json?coupon_definition%5Bcoupon_type%5D=mall&coupon_definition%5Borg_code%5D={orgcode}&keywords={serial_no}&page%5Bindex%5D=1&page%5Bsize%5D=20'.format(
        orgcode=org_code, serial_no=serial_no)
    send_url = 'http://jmp.joowing.com/api/pb/jmp_api/v1/coupon_definitions/batch_send_coupons.json'
    member_info = requests.post(url=member_info_url, headers=p_headers, data=member_data)
    try:
        jw_id = member_info.json()[0]['jw_id']
    except:
        if phone:
            print(f"\n未查询到手机号为{sheet_index.row_values(count)[1]}的会员")
            fail_List.append(sheet_index.row_values(count)[1])
            jw_id = ""
        else:
            print(f"\n未查询到会员号为{sheet_index.row_values(count)[1]}的会员")
            fail_List.append(sheet_index.row_values(count)[1])
            jw_id = ""
    # print(jw_id)
    serial_info = requests.get(serialinfo_url, headers=headers)
    # print(serial_info.json())
    id = serial_info.json()[0]['id']
    name = serial_info.json()[0]['name']
    # print(id,name)
    send_data = {
        "option": [
            {
                "definition_id": id,
                "serial_no": serial_no,
                "display_name": "[{serial_no}]{name}".format(serial_no=serial_no, name=name),
                "jw_id": [
                    jw_id
                ],
                "expiration_date_type": Datetype,
                "num": send_num,
                "expiration_day": 7,
                "begin_date": "2020-08-23",
                "end_date": "2020-08-31"
            }
        ],
        "org_code": org_code
    }
    if Datetype == 'by_day':
        sendday = int(sheet_index.row_values(count)[2])
        send_data['option'][0]['expiration_day'] = sendday
    elif Datetype == 'by_date':
        start_date = sheet_index.row_values(count)[3]
        end_date = sheet_index.row_values(count)[4]
        send_data['option'][0]['begin_date'] = start_date
        send_data['option'][0]['end_date'] = end_date
    send_data = json.dumps(send_data)
    # print(send_data, member_info.json()[0]['phone'], member_info.json()[0]['member_no'])
    send_res = requests.post(url=send_url, headers=p_headers, data=send_data)
    c_number = len(cols) - 2
    a = count - 1
    b = (a / c_number) * 100
    # print(send_res.json())
    if send_res.json() == {'success': True, 'result': 'ok'}:
        print('本次共{num}个发券任务，已执行{done}个，总进度：{b}%'.format(num=c_number, done=a, b='%.2f' % b), end='')
    # else:
    #     fail_List.append(member_info.json()[0]['phone'])
    time.sleep(0.3)
    if len(fail_List) != 0:
        print(f"\n发券失败的{member_type}：{set(fail_List)}")
