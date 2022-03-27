import requests as r

from utils.configs import Config1, Config2, Config3


class CquAuth:
    def __init__(self, username:str, password:str, **kwargs):
        self.s = r.Session()
        self.chain = [
            # Config1(),
            Config2(),
            Config3(username, password)
        ]
        self.kwargs = kwargs

    def login(self):
        # TODO exception handling of each config
        for config in self.chain:
            config.default_method(self.s, **self.kwargs)
        return self.s

    @property
    def session(self):
        return self.s

    @property
    def cookies(self):
        return self.s.cookies

    def close(self):
        self.s.close()

if __name__ == '__main__':
    username = ''
    password = ''
    proxies = {
        'http': 'http://127.0.0.1:9999',
        'https': 'http://127.0.0.1:9999',
    }
    cquauth = CquAuth(username, password, proxies=proxies)
    cquauth.login()
    print(cquauth.cookies.keys())
    # cquauth.close()