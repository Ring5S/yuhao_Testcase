
"""-----------------------该文件用于存放公共变量----------------------"""

# 部分场景需要用到接口查询，请求头和空请求json参数
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Connection': 'keep-alive'
}
data = {}

# 账号密码信息
# 后台账号密码
account_name = 'js1@haoshijie.com'
account_password = 'js1109'
# 导购手机号和导购对应的商户code
phone = '12020102902'
org_code = 'jwbaby'
