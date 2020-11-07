# -*- coding: utf-8 -*-
import xlrd
import requests
import re, json
import tkinter.messagebox
import time
import xlwt
from datetime import date, datetime

on_env = 'http://jmp.joowing.com'
test03_env = 'https://jmp-test03.joowing.com'
Cookie = 'UM_distinctid=1748a47d9990-07dad5d805dfe8-333769-144000-1748a47d99a2cd; Hm_lvt_0c2e41563784bcc9e3dabc630b67ef35=1600415152; _ga=GA1.2.998566515.1600415159; retailer=%7B%22id%22%3A58%2C%22code%22%3A%22ygyj%22%2C%22name%22%3A%22%E9%98%B3%E5%85%89%E7%9B%8A%E4%BD%B3%22%2C%22businesses%22%3A%5B%22payin%22%2C%22consign%22%5D%7D; joowing-staff-jwt=eyJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoieXVoYW8ueHVlIiwiZW1haWwiOiJ5dWhhby54dWVAam9vd2luZy5jb20iLCJ0eXBlIjoiam9vd2luZy1zdGFmZiIsImV4cCI6MTYwMzQ1OTU2NX0.NBO_AMLD_lJCLT1alMyWx966HdxoXovVBu7UBRLW400; joowing-session-id=477dae3092c3fe5611348aea471358a6; login=yuhao.xue'

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
workbook = xlrd.open_workbook(r'C:/Users/DELL/Desktop/Auto_Test/man_coupon1.xlsx')
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


# 先判定发券安装有效期发还是按照天数发
Datetype = Datetype()

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
    sendlist.append(serial_no)
    if int(sheet_index.row_values(0)[1]) == 1:
        phone = sheet_index.row_values(count)[1]
        member_no = ""
        sendlist.append(phone)
    elif int(sheet_index.row_values(0)[1]) == 2:
        phone = ""
        member_no = sheet_index.row_values(count)[1]
        sendlist.append(member_no)

    member_info_url = 'http://jmp.joowing.com/api/ris/spi/demo/members/__query'
    serialinfo_url = 'http://jmp.joowing.com/api/pb/api/v1/promotion/coupon_definitions.json?coupon_definition%5Bcoupon_type%5D=mall&coupon_definition%5Borg_code%5D={orgcode}&keywords={serial_no}&page%5Bindex%5D=1&page%5Bsize%5D=20'.format(
        orgcode=org_code, serial_no=serial_no)
    send_url = 'http://jmp.joowing.com/api/pb/jmp_api/v1/coupon_definitions/batch_send_coupons.json'
    member_info = requests.post(url=member_info_url, headers=p_headers, data=member_data)
    # print(member_info.json())
    jw_id = member_info.json()[0]['jw_id']
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
        "org_code": org_code,
        "description": "商户要求补发"}
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
    print(send_res)
    c_number = len(cols) - 2
    a = count - 1
    b = (a / c_number) * 100
    # print(send_res.json())
    if send_res.json() == {'success': True, 'result': 'ok'}:
        print('\r本次共{num}个发券任务，已执行{done}个，总进度：{b}%'.format(num=c_number, done=a, b='%.2f' % b), end='')
    time.sleep(0.3)
