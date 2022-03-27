# 安装环境
```
pip install requests
pip install beautifulsoup4
pip install pycryptodome
```

# 使用
## 基本用法
```python
from login import CquAuth

username = 'your_username'
password = 'your_password'
cquauth = CquAuth(username, password)
s = cquauth.login()  # 返回requests.Session对象
```

## 添加其他参数
可向session的get/post方法传递参数：
```python
proxies = {
    'http': 'http://127.0.0.1:9999',
    'https': 'http://127.0.0.1:9999',
}

auth = CquAuth(username, password, proxies=proxies)
```

# 执行过程说明
|host|url|方法|获得的cookie|
|---|---|---|---|
|i.cqu.edu.cn|/jsonp/getCurrentLocale.json?_=<TIMESTAMP>|GET|JSESSIONID|
|authserver.cqu.edu.cn|/authserver/login?service=http://i.cqu.edu.cn/login?service=http://i.cqu.edu.cn/new/index.html|GET|JSESSIONID|
|authserver.cqu.edu.cn|/authserver/login?service=http://i.cqu.edu.cn/login?service=http://i.cqu.edu.cn/new/index.html|POST|iPlanetDirectoryPro、CASTGC、CASPRIVACY|
|i.cqu.edu.cn|/login?service=http://i.cqu.edu.cn/new/index.html&ticket=<TICKET>|GET|MOD_AUTH_CAS|
|i.cqu.edu.cn|/login?service=http://i.cqu.edu.cn/new/index.html|GET|asessionid|


