import ast
import re

import execjs
import requests
from hashlib import md5, sha1, sha256
class GetCookie:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

    def go(self, data):
        '''
        对go函数的逆向
        '''
        chars = data["chars"]
        for i in chars:
            for j in chars:
                cookie = data["bts"][0] + i + j + data["bts"][1]
                if data['ha']:
                    encrypt = eval(data['ha']+'()')
                    encrypt.update(cookie.encode(encoding='utf-8'))
                    if encrypt.hexdigest() == data['ct']:
                        return cookie

    def get_cookies(self, url):
        '''
        输入url获取正确cookies
        '''
        response = self.session.get(url=url)
        cookie = response.headers['Set-Cookie'].split(';')[0].split('=')
        cookies = {cookie[0]: cookie[1]}
        cookie = re.findall(r'(cookie=.*?)location', response.text)[0]
        js_code = "function get_cookies(){" + cookie + "return cookie}"
        cookie = execjs.compile(js_code).call('get_cookies').split(';')[0].split('=')
        cookies.update({cookie[0]: cookie[1]})
        response = self.session.get(url=url, cookies=cookies)
        data = ast.literal_eval(re.findall(r'go\((.*?)\)', response.text)[1])
        cookie = self.go(data)
        cookies.update({'__jsl_clearance': cookie, '__jsl_clearance_s': cookie})
        return cookies

if __name__ == '__main__':
    # 使用测试
    a = GetCookie()
    url = 'http://sthjj.beijing.gov.cn/bjhrb/index/xxgk69/zfxxgk43/fdzdgknr2/ywdt28/gsl/index.html'
    response = requests.get(url=url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        },cookies=a.get_cookies(url))
    print(response.text)