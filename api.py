
# Even
# 2018.5.3

#import sysfiles
import os
import json
import base64
import binascii
#import constfiles
#from ... import sysfiles
from Crypto.Cipher import AES



# 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7');
nonce = '0CoJUm6Qyw8W8jud';
pubKey = '010001';

#text 是一个dict文件 包含用户名和密码
def Encrypt_Data(text):
    text = json.dumps(text);
    Key = createRandomKey(16);
    encText = aesEncrypt(aesEncrypt(text, nonce), Key);
    encKey = rsaEncrypt(Key, pubKey, modulus);
    data = {'params': encText, 'encSecKey': encKey};
    return data;
def aesEncrypt(text, Key):
    pad = 16 - len(text) % 16;
    text = text + chr(pad) * pad;
    encryptor = AES.new(Key, 2, '0102030405060708');
    ciphertext = encryptor.encrypt(text);
    ciphertext = base64.b64encode(ciphertext).decode('utf-8');
    return ciphertext;
def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1];
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16));
    return format(rs, 'x').zfill(256);
def createRandomKey(size):
    return binascii.hexlify(os.urandom(size))[:16];
