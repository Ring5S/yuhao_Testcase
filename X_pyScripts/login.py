from Auto_Scripts.公共方法 import Login
import json
import requests
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Connection': 'keep-alive',
    'Cookie':'UM_distinctid=1748a47d9990-07dad5d805dfe8-333769-144000-1748a47d99a2cd; _ga=GA1.2.998566515.1600415159; Hm_lvt_0c2e41563784bcc9e3dabc630b67ef35=1604553260; _newbee_session=3b7188cd1bef135dc10baab1d6787177; joowing-session-id=3b7188cd1bef135dc10baab1d6787177; retailer-staff-jwt=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6ODYwMTksIm5hbWUiOiJqczFAY2h5c3RwLmNvbSIsIm5pY2tfbmFtZSI6IuS7juWMluS8mOS4iuerpeWTgS3mioDmnK8xIiwibm8iOiJKVzAwMSIsInBob25lIjoiMTgwMDAwMDE2OTYiLCJ0eXBlIjoiam9vd2luZy1zdGFmZiIsIm9yZ19pZCI6MTQxNDksIm9yZ19jb2RlIjoiY2h5c3RwIiwicmV0YWlsZXJfaWQiOjE0MTQ5LCJyZXRhaWxlcl9jb2RlIjoiY2h5c3RwIiwiZXhwIjoxNjA1NTc5NDEyfQ.fAhZdkdffPZp5HSVqBfOXwrNlxqrYVYhePaggXA8ak4; login=js1%40chystp.com'
}
data = {}

# login = Login(headers=headers, data=data)
# Nb_session = login.NB_Login()
# print(Nb_session)
# url = 'http://nb3.joowing.com/api/pb/chystp/showcase/themes.json?page%5Bindex%5D=1&page%5Bsize%5D=999'
# res = Nb_session.get(url, headers=headers)
# print(res.request.headers)
# print(res.json())

print("发起PUT请求")
data1 = {"item":{"id":56367,"org_id":14149,"org_code":"chystp","name":"邱群娣","user_id":87294,"user_name":"qiuqundi@chystp.com","phone":"13926214326","member_no":"ZW100056","type_codes":["00001"],"creator_id":86019,"shop_id":48738,"shop_code":"000003","is_dimission":False,"dimission_time":None,"is_deleted":False,"created_at":"2020-11-16T11:20:17+08:00","updated_at":"2020-11-16T11:20:17+08:00","user_no":"809","attention_member":True,"scene_id":None,"ticket":None,"jw_id":"91603d70-09e8-0139-929d-4ade75defa64","opts":None,"shop_name":"广州市从化街口浩敏钟商店","domain":"chystp.com"}}
data1 = json.dumps(data1)
url1 = 'http://nb3.joowing.com/nebula/v3/shopping_consultant/guides/56367.json'
res = requests.put(url=url1, headers=headers, data=data1)
print(res,res.json())