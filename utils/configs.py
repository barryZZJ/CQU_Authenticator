import re

import requests as r
from bs4 import BeautifulSoup

from utils.encrypt import encryptAES
from utils.timestamp import timestamp_ms


class Config:
    def __init__(self, addr: str=None, headers: dict=None, params: dict = None, data = None):
        self.common_header = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.update(addr, headers, params, data)

    def update(self, addr: str=None, headers: dict=None, params: dict = None, data = None):
        self.addr = addr
        self.headers = self.common_header.copy()
        if headers:
            self.headers.update(headers)
        self.params = params
        self.data = data

    def _post(self, session: r.Session, **kwargs):
        return session.post(self.addr, params=self.params, headers=self.headers, data=self.data, **kwargs)

    def _get(self, session, **kwargs):
        return session.get(self.addr, params=self.params, headers=self.headers, data=self.data, **kwargs)

    def default_method(self, session, **kwargs): pass


class Config1(Config):
    def __init__(self):
        addr = 'http://i.cqu.edu.cn/jsonp/school.json'
        headers = {
            'Accept': '*/*',
            'Referer': 'http://i.cqu.edu.cn/new/index.html',
        }
        super(Config1, self).__init__(addr, headers)

    def default_method(self, session, **kwargs):
        return self._get(session, **kwargs)


class Config2(Config):
    def __init__(self):
        addr = 'http://i.cqu.edu.cn/jsonp/getCurrentLocale.json'
        headers = {
            'Accept': '*/*',
            'Referer': 'http://i.cqu.edu.cn/new/index.html',
        }
        params = {'_': timestamp_ms()}
        super(Config2, self).__init__(addr, headers, params)

    def default_method(self, session, **kwargs):
        return self._get(session, **kwargs)


class Config3(Config):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        addr = 'http://authserver.cqu.edu.cn/authserver/login?service=http%3A%2F%2Fi.cqu.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fi.cqu.edu.cn%2Fnew%2Findex.html'
        headers_get = {
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://i.cqu.edu.cn/',
        }
        self.headers_post = {
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'http://authserver.cqu.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://authserver.cqu.edu.cn/authserver/login?service=http%3A%2F%2Fi.cqu.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fi.cqu.edu.cn%2Fnew%2Findex.html',
        }
        super(Config3, self).__init__(addr, headers_get)

    def make_data(self, resp, username, password):
        data = dict(username=username)
        soup = BeautifulSoup(resp.content, 'lxml')
        form = soup.find(id='casLoginForm')
        names = ['lt', 'dllt', 'execution', '_eventId', 'rmShown']
        for name in names:
            v = form.find(name='input', attrs={'name': name}).get('value')
            data[name] = v
        p = re.compile(r'pwdDefaultEncryptSalt = "(\S+)"')
        aesKey = None
        for script in soup.find_all('script'):
            if script.string:
                res = p.search(script.string)
                if res is not None:
                    aesKey = res.group(1)
                    break
        assert aesKey is not None
        data['password'] = encryptAES(password, aesKey)
        return data

    def default_method(self, session, **kwargs):
        resp = self._get(session, **kwargs)
        self.data = self.make_data(resp, self.username, self.password)
        self.headers = self.common_header.copy()
        self.headers.update(self.headers_post)
        # 304 jumps work properly
        return self._post(session, **kwargs)
