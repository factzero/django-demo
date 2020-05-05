# AuthoringSystem接口文档

### 一、登录接口

##### 1、接口地址： [post] /upp/users/?action=login

##### 2、请求参数说明

```json
{
    "u_name": "用户名",
    "u_password": "密码"
}
```

##### 3、返回参数说明

```json
{
    "msg": "返回信息",
    "status": 状态码,
    "pubkey": "RSA公钥",
    "token": "令牌"
}
```

### 二、获取license

#### 1、接口地址： [post] /upp/license/?token=

##### 2、请求参数说明

```json
{
    "token": "令牌",
    "productName": "产品BOM",
    "hardwareInfo": "硬件指纹"
}
```

##### 3、返回参数说明

```json
{
    "msg": "返回信息",
    "status": 状态码,
    "licenseInfo": "license正文",
    "digitalSign": "license正文的数字签名"
}
```

### 三、状态码说明

| 状态码 | 详细说明 |
| ------ | :------- |
| 200    | OK       |

