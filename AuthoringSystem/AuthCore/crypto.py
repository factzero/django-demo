# -*- coding: utf-8 -*-
import rsa
import base64


def rsa_gen_key():
    (pubkey, privkey) = rsa.newkeys(512)
    return pubkey, privkey


def rsa_gen_key_pkcs1():
    (pubkey, privkey) = rsa.newkeys(512)
    pubkey = pubkey.save_pkcs1().decode()
    privkey = privkey.save_pkcs1().decode()
    return pubkey, privkey


def rsa_encrypt(message, pubkey):
    crypto_text = rsa.encrypt(message.encode(), pubkey)
    return crypto_text


def rsa_digital_sign(message, privkey):
    digital_sign_text = rsa.sign(message.encode(), privkey, 'SHA-1')
    digital_sign_text_base64 = base64.b64encode(digital_sign_text).decode('utf-8')
    return digital_sign_text_base64


def rsa_digital_sign_pkcs1(message, privkey):
    privkey = rsa.PrivateKey.load_pkcs1(privkey)
    digital_sign_text = rsa.sign(message.encode(), privkey, 'SHA-1')
    digital_sign_text_base64 = base64.b64encode(digital_sign_text).decode('utf-8')
    return digital_sign_text_base64


if __name__ == '__main__':
    pubkey, privkey = rsa_gen_key()
    mess = 'hello word'
    digital_sign_text = rsa_digital_sign(mess, privkey)
    print('digital_sign type:', type(digital_sign_text))
    print('digital_sign ori:', digital_sign_text)
    print('digital_sign base64:', base64.b64encode(digital_sign_text))
    print('digital_sign base64 utf8:', base64.b64encode(digital_sign_text).decode("utf-8"))
