from lxml import etree
import requests
cookie = 'UM_distinctid=1748a47d9990-07dad5d805dfe8-333769-144000-1748a47d99a2cd; SESSION=6f650e0d-7e70-460f-8cd8-5db0c084a7a1; JSESSIONID=BD4547D596AE49F9E57D3DB281BD1D01; login=js1%40ezbbw.com; retailer-jwt=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoianMxQGV6YmJ3LmNvbSIsInVzZXJfYXR0cmlidXRlcyI6e30sImV4cCI6MTYwMDMzOTg5Mn0.lEcvyp1gGwj1YpLKK6pemO0aVdybpRDe7wJNoWjozN4; _newbee_session=BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJWIwMjk3OTkyYzNhNTg4NTY0ZTA5NzMzZmIwZTViY2JjBjsAVEkiDHVzZXJfaWQGOwBGaQL%2Bn0kiD2V4cGlyZXNfYXQGOwBGVTogQWN0aXZlU3VwcG9ydDo6VGltZVdpdGhab25lWwhJdToJVGltZQ0pIh7AsMEGzgk6DW5hbm9fbnVtaQK2AzoNbmFub19kZW5pBjoNc3VibWljcm8iBpU6CXpvbmVJIghVVEMGOwBGSSIMQmVpamluZwY7AFRJdTsHDTEiHsCwwQbOCTsIaQK2AzsJaQY7CiIGlTsLSSIIVVRDBjsARkkiDW5lYnVsYS0zBjsARlQ%3D--62e41d35927a8015289a89b3fcd2f68ef045f23e; joowing-session=19105400a840c8d07d03f2b077c4a1e2'
headers = {
    'Cookie' : cookie,
    'user-agent':''
}
url = 'http://nb3.joowing.com/nebula/config/wx_public_config'
page_text = requests.get(url,headers=headers).text
# parser = etree.HTMLParser(encoding='utf-8')
# tree = etree.parse('test.html',parser=parser)
# tree = etree.HTML(page_text)
# list = tree.xpath('//div[@class="logo layout-align-start-center layout-row"]')
# print(page_text,list)
# print(page_text)


import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie': cookie,
}
url = 'http://nb3.joowing.com/nebula/config/wx_public_config'
session = requests.Session()
response = session.get(url, headers=headers)

print(response.status_code)
print(response.text)