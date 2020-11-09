import requests
import tkinter.messagebox
import json
from Auto_Scripts.Interface_method import Interface_Method
from multiprocessing import pool
import time

message = tkinter.messagebox
import random

Js1_password = 'js0909'
# data = {
#     "profile": {"tabs": [{"code": "home"}, {"code": "live"}, {"code": "group"}, {"code": "cart"}, {"code": "mine"}]}}
# data = json.dumps(data)

data1 = {}
# determine = message.askokcancel(title='Determine', message="独立版小程序商户，是否也需要切换私域模式？")

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

orglist = ['ya0001', 'ya0003', 'ya0006', 'ya0013', 'ya0023', 'yslaybaby', 'yslazy', 'yslbabyplan', 'ysljlasy',
           'yslmasg', 'ya0055', 'ya0056', 'ya0057', 'ya0058', 'ya0059', 'ya0060', 'ya0061', 'ya0062', 'ya0063',
           'ya0064', 'ya0068', 'ya0069', 'ya0070', 'ya0071', 'ya0073', 'ya0078', 'ya0079', 'ya0080', 'ya0081', 'ya0082',
           'ya0083', 'ya0085', 'ya0087', 'ya0088', 'ya0089', 'ya0090', 'ya0091', 'ya0092', 'ya0094', 'ya0095', 'ya0096',
           'ya0097', 'ya0098', 'ya0099', 'ya0100', 'ya0101', 'ya0102', 'ya0103', 'ya0104', 'ya0105', 'ya0106', 'ya0107',
           'ya0108', 'ya0109', 'ya0110', 'ya0111', 'ya0112', 'ya0113', 'ya0115', 'ya0116', 'ya0117', 'ya0118', 'ya0119',
           'ya0120', 'ya0121', 'ya0122', 'ya0123', 'ya0124', 'ya0125', 'ya0126', 'ya0127', 'ya0128', 'ya0129', 'ya0130',
           'ya0131', 'ya0132', 'ya0133', 'ya0134', 'ya0135', 'ya0136', 'ya0137', 'ya0138', 'ya0139', 'ya0140', 'ya0141',
           'ya0142', 'ya0143', 'ya0144', 'ya0145', 'ya0146', 'ya0147', 'ya0148', 'ya0149', 'ya0151', 'ya0152', 'ya0153',
           'ya0154', 'ya0155', 'ya0157', 'ya0158', 'ya0159', 'ya0160', 'ya0237', 'ya0238', 'ya0239', 'ya0240', 'ya0241',
           'ya0242', 'ya0243', 'ya0591', 'ya0592', 'ya0593', 'ya0594', 'ya0595', 'ya0596', 'ya0597', 'ya0598', 'ya0599',
           'ya0601', 'ya0415', 'ya0416', 'ya0417', 'ya0418', 'ya0419', 'ya0912', 'ya0913', 'ya0914', 'ya0915', 'ya0916',
           'ya0920', 'ya0921', 'ya0922', 'ya0923', 'ya0924', 'ya0925', 'ya0926', 'ya0927', 'ya0928', 'ya0929', 'ya0930',
           'ya0931', 'ya0520', 'ya0521', 'ya0522', 'ya0524', 'ya0607', 'ya0608', 'ya0609', 'ya0610', 'ya0611', 'ya0705',
           'ya0706', 'ya0707', 'ya0727', 'ya0728', 'ya0729', 'ya0730', 'ya0731', 'ya0732', 'ya0733', 'ya0734', 'ya0735',
           'ya0736', 'ya0737', 'ya0738', 'ya0739', 'ya0740', 'ya0741', 'ya0742', 'ya0743', 'ya0744', 'ya0745', 'ya0746',
           'ya0787', 'ya0788', 'ya0789', 'ya0790', 'ya0791', 'ya0792', 'ya0793', 'ya0794', 'ya0795', 'ya0796', 'ya0797',
           'ya0798', 'ya0906', 'ya0907', 'ya0908', 'ya0909', 'ya0910', 'ya0587', 'ya0588', 'ya0589', 'ya0590', 'ya0603',
           'ya0604', 'ya0605', 'ya0606', 'ya0612', 'ya0613', 'ya0614', 'ya0615', 'ya0616', 'ya0617', 'ya0618', 'ya0619',
           'ya0621', 'ya0622', 'ya0699', 'ya0700', 'ya0701', 'ya0565', 'ya0566', 'ya0567', 'ya0568', 'ya0569', 'ya0570',
           'ya0571', 'ya0572', 'ya0573', 'ya0574', 'ya0575', 'ya0578', 'ya0821', 'ya0822', 'ya0823', 'ya0824', 'ya0825',
           'ya0826', 'ya0827', 'ya0828', 'ya0829', 'ya0830', 'ya0831', 'ya0490', 'ya0491', 'ya0492', 'ya0493', 'ya0494',
           'ya0495', 'ya0496', 'ya0497', 'ya0837', 'ya0838', 'ya0839', 'ya0840', 'ya0841', 'ya0842', 'ya0843', 'ya0844',
           'ya0845', 'ya0846', 'ya0959', 'ya0960', 'ya0961', 'ya0962', 'ya0963', 'ya0964', 'ya0965', 'ya0966', 'ya0967',
           'ya1646', 'ya1647', 'ya1652', 'ya1653', 'ya1656', 'ya1659', 'ya1661', 'ya1662', 'ya1663', 'ya1667', 'ya1668',
           'ya1669', 'ya1681', 'ya1688', 'ya1698', 'ya1703', 'ya1708', 'ya1714', 'ya1746', 'ya1751', 'ya1758', 'ya1759',
           'ya1761', 'ya1762', 'ya1768', 'ya1770', 'ya1771', 'ya1772', 'ya1773', 'ya1774', 'ya1778', 'ya1780', 'ya1781',
           'ya1783', 'ya1784', 'ya1788', 'ya1790', 'ya1791', 'ya1792', 'ya1794', 'ya1798', 'ya1800', 'ya1801', 'ya1803',
           'ya1804', 'ya1805', 'ya1806', 'ya1807', 'ya1808', 'ya1809', 'ya1813', 'ya1814', 'ya1815', 'ya1822', 'ya1823',
           'ya1827', 'ya1830', 'ya1832', 'ya1833', 'ya13331', 'ya13333']
print(len(orglist))


def NB_login(org_code):
    global headers
    global data
    global Js1_password
    NB_account = 'js1@{org_code}.com'.format(org_code=org_code)
    login_url = f'http://nb3.joowing.com/nebula/v3/session?session%5Blogin%5D={NB_account}&session%5Bpassword%5D={Js1_password}'
    session = requests.session()
    res = session.post(url=login_url, data=data1)
    print(res, org_code)
    # login_Session = session.Post_request()
    return session


def check(org_list):
    data = {
        "profile": {
            "tabs": [{"code": "home"}, {"code": "live"}, {"code": "group"}, {"code": "cart"}, {"code": "mine"}]}}
    data = json.dumps(data)
    # rtime = random.randint(1, 20)
    # time.sleep(rtime)
    orgcode = org_list
    NB_Session = NB_login(orgcode)
    url = f'http://nb3.joowing.com/api/pb/{orgcode}/showcase/profiles.json'
    res = NB_Session.get(url=url, headers=headers)
    print(res, res.json())
    try:
        if res.json()['tabs'] == [{'code': 'home'}, {'code': 'live'}, {'code': 'group'}, {'code': 'cart'},
                                  {'code': 'mine'}]:
            # print(f"商户{orgcode}导航栏正常")
            pass
        else:
            print(f"商户{orgcode}导航栏异常")
    except Exception as e:
        print(e,f'--------------------------------------{orgcode}')


def action(org_list):
    data = {
        "profile": {
            "tabs": [{"code": "home"}, {"code": "live"}, {"code": "group"}, {"code": "cart"}, {"code": "mine"}]}}
    data = json.dumps(data)
    # rtime = random.randint(1, 20)
    # time.sleep(rtime)
    orgcode = org_list
    NB_Session = NB_login(orgcode)
    url = f'http://nb3.joowing.com/api/pb/{orgcode}/showcase/profiles.json'
    res = NB_Session.put(url=url, headers=headers, data=data)
    print(res.request.headers)
    print(res, res.json())


if __name__ == '__main__':
    pool = pool.ThreadPool()  # 创建一个线程池
    pool.map(check, orglist)  # 往线程池中填线程
    pool.close()  # 关闭线程池，不再接受线程
    pool.join()  # 等待线程池中线程全部执行完

# print(len(orglist))
