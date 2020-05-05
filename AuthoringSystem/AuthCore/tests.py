from django.test import TestCase

# Create your tests here.
import requests
import json
import time
import threading


def get_license(user, password, product):
    ip = "http://192.168.3.50:8000"
    login_url = ip + "/upp/users/?action=login"
    data = {"u_name": user, "u_password": password}
    response = requests.post(login_url, data=data, json=True)
    token = response.json().get('token')
    print('user:{}, password:{}, token:{}, product:{} start'.format(user, password, token, product))

    license_url = ip + "/upp/license/?token={}".format(token)
    data = {"productName": product, "hardwareInfo": "zvafadfadfadsfac"}
    for i in range(5000):
        start_time = time.time()
        response = requests.post(license_url, data=data, json=True)
        end_time = time.time()
        # print('Took %f second' % (end_time - start_time))
        # print(response.json())
    print('user:{}, password:{}, token:{}, product:{} end'.format(user, password, token, product))


def get_license_v1(user, password, product):
    # ip = "http://127.0.0.1:8000"
    ip = "http://192.168.3.50:8000"
    login_url = ip + "/upp/v1/login/"
    data = {"u_name": user, "u_password": password}
    response = requests.post(login_url, data=data, json=True)
    response_data = response.json()
    token = response_data['results']['token']
    print('v1 user:{}, password:{}, token:{}, product:{} start'.format(user, password, token, product))

    license_url = ip + "/upp/v1/license/"
    data = {"product_name": product, "hardware_info": "zvafadfadfadsfac", "token": token}
    for i in range(50):
        start_time = time.time()
        response = requests.post(license_url, data=data, json=True)
        end_time = time.time()
        response_data = response.json()
        if 200 != response_data["status"]:
            print("license申请失败")
        # print('Took %f second' % (end_time - start_time))
        # print(response.json())
    print('v1 user:{}, password:{}, token:{}, product:{} end'.format(user, password, token, product))


if __name__ == '__main__':
    # get_license_v1("Lucy", "11011", "fs01")
    for i in range(2):
        t = threading.Thread(target=get_license_v1, args=("Lucy", "11011", "fs01"))
        t.start()
        t = threading.Thread(target=get_license_v1, args=("Lucy", "11011", "fs02"))
        t.start()
        t = threading.Thread(target=get_license_v1, args=("Rock", "11011", "fs02"))
        t.start()
        t = threading.Thread(target=get_license_v1, args=("Jhon", "12356", "ba01"))
        t.start()
