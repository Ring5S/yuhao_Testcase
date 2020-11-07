import requests
import tkinter.messagebox
import json
from Auto_Scripts.Interface_method import Interface_Method

message = tkinter.messagebox

Js1_password = 'js0909'
data = {}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}


class Login:
    def __init__(self, org_code):
        self.org_code = org_code

    def NB_login(self):
        global headers
        global data
        global Js1_password
        NB_account = 'js1@{org_code}.com'.format(org_code=self.org_code)
        login_url = f'http://nb3.joowing.com/nebula/v3/session?session%5Blogin%5D={NB_account}&session%5Bpassword%5D={Js1_password}'
        Interface_method = Interface_Method(url=login_url, data=data, headers=headers)
        login_Session = Interface_method.Post_request()
        return login_Session

    def JMP_login(self):
        login_url = 'http://jmp.joowing.com/api/ris/sessions.json?session%5Blogin%5D=yuhao.xue&session%5Bpassword%5D=980127xyhXYC'
        Interface_method = Interface_Method(url=login_url, data=data, headers=headers)
        login_Session = Interface_method.Post_request()
        return login_Session


def switch_to_wxprivate(wx_public_configs_json, NB_Session, orgcode):
    wx_public_configs_json['platform_weapp_mode'] = 'private'
    wx_public_update = {'wx_public_config': wx_public_configs_json}
    # print(wx_public_update)
    update_url = 'http://nb3.joowing.com/nebula/v3/nebula_config/wx_public_configs/create_or_update.json'
    wx_public_update = json.dumps(wx_public_update)
    public_update_response = NB_Session.post(url=update_url, data=wx_public_update, headers=headers)
    # print(public_update_response, public_update_response.json())
    if public_update_response.status_code == 201:
        print(f"商户{orgcode}切换私域模式成功")
    elif public_update_response.status_code != 201:
        print(f"商户{orgcode}切换私域模式异常")


# org_list = ['demo', 'wtdemo']
orgcode = input("输入需要切换私域模式的商户org_code:")
Login = Login(org_code=orgcode)
NB_Session = Login.NB_login()
# JMP_Session = Login.JMP_login()

wx_public_configs_url = 'http://nb3.joowing.com/nebula/v3/nebula_config/wx_public_configs.json'
res = NB_Session.get(url=wx_public_configs_url)
wx_public_configs_json = res.json()

# if wx_public_configs_json == None:
#     print(f'商户【{orgcode}】微信公众号配置项为空！自动过滤')
#     # continue
# else:
#     # platform_weapp字段判定：
#     if wx_public_configs_json['platform_weapp']:
#         switch_to_wxprivate(wx_public_configs_json)
#     else:
#         # print(f"商户【{orgcode}】为独立版小程序")
#         determine = message.askokcancel(title='Determine', message=f"商户【{orgcode}】为独立版小程序，是否需要切换私域模式？")
#         if determine:
#             switch_to_wxprivate(wx_public_configs_json, NB_Session, orgcode)
#         else:
#             print(f"商户【{orgcode}】为独立版小程序，不切换私域模式")

