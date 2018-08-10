#仅用于响应获取原始api数据，未定义params参数。
#

import requests
import json
from bs4 import BeautifulSoup
import os
from Crypto.Cipher import AES
import base64
import urllib

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Origin': 'https://music.163.com',
}

headers['Cookie'] = '_ntes_nuid=a8f6aeeac6a8732e05ade2ea8e531d06;'

# 设置代理ip
proxies = {'http':'219.141.153.41:80'}


def get_encSecKey():
    #获取encSecKey
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey

def get_params(first_param):
    #获取encText，也就是params
    iv = "0102030405060708"
    first_key = "0CoJUm6Qyw8W8jud"
    second_key = 'F' * 16
    '''
    if page == 0:
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
    else:
        offset = str((page - 1) * 20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
    '''

    encText = AES_encrypt(first_param, first_key, iv)
    encText = AES_encrypt(encText.decode('utf-8'), second_key, iv)
    return encText

def AES_encrypt(text, key, iv):
    #AES加密
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    encrypt_text = encryptor.encrypt(text.encode('utf-8'))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def main(info):
    url, first_param = info
    params = get_params(first_param)
    encSecKey = get_encSecKey()
    data = {'params': params, 'encSecKey': encSecKey}
    data = urllib.parse.urlencode(data).encode('utf8')
    res = requests.post(url,params = data, headers = headers, proxies = proxies)
    return res.text
