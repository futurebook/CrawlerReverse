import ast
import re

import execjs
import requests
from hashlib import md5, sha1, sha256

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

def go(data):
    chars = data["chars"]
    for i in chars:
        for j in chars:
            cookie = data["bts"][0] + i + j + data["bts"][1]
            if data['ha'] == 'md5':
                encrypt = md5()
            elif data['ha'] == 'sha1':
                encrypt = sha1()
            elif data['ha'] == 'sha256':
                encrypt = sha256()
            encrypt.update(cookie.encode(encoding='utf-8'))
            if encrypt.hexdigest() == data['ct']:
                return cookie

response = requests.get('http://www.zongyang.gov.cn/openness/OpennessContent/showList/1442/45712/page_1.html', headers=headers)
cookie = response.headers['Set-Cookie'].split(';')[0].split('=')
cookies = {cookie[0]: cookie[1]}
cookie = re.findall(r'(cookie=.*?)location', response.text)[0]
js_code = "function get_cookies(){"+cookie+"return cookie}"
cookie = execjs.compile(js_code).call('get_cookies').split(';')[0].split('=')
cookies.update({cookie[0]: cookie[1]})
response = requests.get('http://www.zongyang.gov.cn/openness/OpennessContent/showList/1442/45712/page_1.html', cookies=cookies, headers=headers)
data = ast.literal_eval(re.findall(r'go\((.*?)\)', response.text)[1])
cookie = go(data)
cookies.update({'__jsl_clearance': cookie})
response = requests.get('http://www.zongyang.gov.cn/openness/OpennessContent/showList/1442/45712/page_1.html', cookies=cookies, headers=headers)
print(response.text)
