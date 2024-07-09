import requests
from bs4 import BeautifulSoup

url_login = 'https://sso.dainam.edu.vn/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3D96d0cb60-6e85-4adf-b8f6-702647326cf3%26redirect_uri%3Dhttps%253A%252F%252Fnhapdiem.dainam.edu.vn%252Fsignin-oidc%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520api1%26state%3D8dfdad6b0a454926b4e10f957a378abc%26code_challenge%3DShlngxFfaVq27QF-TpsAV8J9LlqRW9pf0h2MLNYGq0A%26code_challenge_method%3DS256%26response_mode%3Dquery'
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
}
response_login = session.get(url_login,headers=headers)
soup_login = BeautifulSoup(response_login.content, "html.parser")
requestVerificationToken = soup_login.find('input', attrs={'name':'__RequestVerificationToken', 'type':'hidden'}).attrs["value"]
print(requestVerificationToken)
data = {
        '__RequestVerificationToken': requestVerificationToken,
        'ReturnUrl': "/connect/authorize/callback?client_id=96d0cb60-6e85-4adf-b8f6-702647326cf3&redirect_uri=https%3A%2F%2Fnhapdiem.dainam.edu.vn%2Fsignin-oidc&response_type=code&scope=openid%20profile%20api1&state=e2269edfed7c4b8abc604294cc70e89d&code_challenge=jnUDvvxqlTEh6fDbfrDW6KZdufbLBWjR3L4AXe2kamY&code_challenge_method=S256&response_mode=query",
        'UserName': 'DN01500961',
        'Password': 'DN01500961',
        'button': 'login'
    }

headers_1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'scheme': 'https',
    'host': 'nhapdiem.dainam.edu.vn',
	'filename': '/BaoCaoTaiChinh/Index',
    'Address':'103.48.194.162:443'
}

session.post(url_login, data=data, headers=headers, allow_redirects=True)
# b = BeautifulSoup(a.content, "html.parser")
# print(b)
session.cookies.update(session.cookies)

url_tai_chinh = 'https://nhapdiem.dainam.edu.vn/BaoCaoTaiChinh/Index'
response_GetCasaInfo = session.get(url_tai_chinh, headers=headers_1)
test = BeautifulSoup(response_GetCasaInfo.content, "html.parser")
print(test)