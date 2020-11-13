from Auto_Scripts.公共方法 import Login

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Connection': 'keep-alive'
}
data = {}

login = Login(headers=headers, data=data)
Nb_session = login.NB_Login()
print(Nb_session)
url = 'http://nb3.joowing.com/api/pb/demo/showcase/themes.json?page%5Bindex%5D=1&page%5Bsize%5D=999'
res = Nb_session.get(url, headers=headers)
print(res.request.headers)
print(res.json())
