import json
import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Cookie': 'UM_distinctid=1748a47d9990-07dad5d805dfe8-333769-144000-1748a47d99a2cd; _ga=GA1.2.998566515.1600415159; _newbee_session=3b61319e9f77d74f7e28dec91c697b9b; joowing-session-id=3b61319e9f77d74f7e28dec91c697b9b; Hm_lvt_0c2e41563784bcc9e3dabc630b67ef35=1604553260; retailer-staff-jwt=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6ODcwMjUsIm5hbWUiOiJqczFAZnFmYnQuY29tIiwibmlja19uYW1lIjoi56aP5riF56aP55m-56ulLeaKgOacrzEiLCJubyI6ImpzMSIsInBob25lIjoiMTgwMDAwMDE2OTYiLCJ0eXBlIjoiam9vd2luZy1zdGFmZiIsIm9yZ19pZCI6MTQxOTgsIm9yZ19jb2RlIjoiZnFmYnQiLCJyZXRhaWxlcl9pZCI6MTQxOTgsInJldGFpbGVyX2NvZGUiOiJmcWZidCIsImV4cCI6MTYwNDk3ODE1NX0.hrAdnbIScEmTqHU6VhIwdPcLuWNpZZ-sCz_byO0kVmo; login=js1%40fqfbt.com'
}
data1 = {"notification_config": {"org_code": "fqfbt", "buz_type": "order", "name": "null",
                                 "receivers": [{"id": 14900, "type": "role", "label": "区域母婴店长"}], "contents": [
        {"scene": "cancel", "name": "null", "content": "%{shop}有新退单%{order_no}，总价%{total}元，请及时退单"},
        {"scene": "fast_mail", "name": "null", "content": "%{shop}有新物流订单%{order_no}，总价%{total}元，请及时录单发货"},
        {"scene": "self_delivery", "name": "null", "content": "%{shop}有新自提订单%{order_no}，总价%{total}元，请及时录单"}]}}
# data2 = '{"notification_config":{"org_code":"fqfbt","buz_type":"order","name":"null","receivers":[{"id":14900,"type":"role","label":"区域母婴店长"}],"contents":[{"scene":"cancel","name":"null","content":"%{shop}有新退单%{order_no}，总价%{total}元，请及时退单"},{"scene":"fast_mail","name":"null","content":"%{shop}有新物流订单%{order_no}，总价%{total}元，请及时录单发货"},{"scene":"self_delivery","name":"null","content":"%{shop}有新自提订单%{order_no}，总价%{total}元，请及时录单"}]}}'
data3 = json.dumps(data1)
post_mess_url = 'http://nb3.joowing.com/nebula/v3/nebula_config/notification_configs/create_or_update'
Session = requests.session()
print(Session)
# res = session.post(url=post_mess_url, data=data1, headers=headers)
# res2 = session.post(url=post_mess_url, data=data2.encode())
res3 = Session.post(url=post_mess_url, data=data3 ,headers=headers)
print(res3.request.headers)


res = Session.post(url=post_mess_url, data=data3)
print(res.request.headers)
