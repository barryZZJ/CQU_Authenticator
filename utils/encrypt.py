import base64
import random
import re
from math import floor

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def encryptAES(data: str, aesKey: str) -> str:
    if not aesKey:
        return data
    encrypted = getAesString(randomString(64) + data, aesKey, randomString(16))
    return encrypted


aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
aes_chars_len = len(aes_chars)


def randomString(len):
    retStr = ''
    for i in range(len):
        retStr += aes_chars[floor(random.random() * aes_chars_len)]
    return retStr


# AES-128-CBC加密模式，key需要为16位，key和iv可以一样
# 返回的是base64格式的密文
def getAesString(data: str, key0: str, iv0: str) -> str:
    data = data.encode('utf8')
    key0 = re.sub(r'/(^\s+)|(\s+$)/g', '', key0)
    key0 = key0.encode('utf8')
    iv0 = iv0.encode('utf8')
    cipher = AES.new(key0, AES.MODE_CBC, iv=iv0)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size, 'pkcs7'))
    ct = base64.b64encode(ct_bytes).decode('utf8')
    return ct


if __name__ == '__main__':
    data = 'fXpRKMBeBtKewWr32EFbPKjRRiNDQxktfzzY4p4nam45t5kSxsc4k3GEzmK76SNczzjzzj0123'
    key0 = '2uvVcozjcXKfSrZw'
    iv0 = 'PWs5NitQxCBpneEF'
    print(getAesString(data, key0, iv0))
    print(
        'XHTgYa6fDdsqXtXQ6tESgEhOokm+P1rJCKelQZBF3UpDfK7RYE2An5b/fjmiuqEsqpdbTCFzeTVJdTWaJbpNXUEU2E7W9GiZD3ifKU5MS74=')
