## AuthoringSystem接口文档_V1

### 一、登录接口

##### 1、接口地址： [post]  /upp/v1/login/

##### 2、请求参数说明

```json
{
    "u_name": "用户名",
    "u_password": "密码",
}
```

##### 3、返回参数说明

```json
{
    "status": 状态码,
    "msg": "返回信息",
    "results": {
        "token": "令牌",
        "token_expire_time": 令牌有效时间,
        "pubkey": "RSA公钥"
    }
}
```

### 二、获取license

##### 1、接口地址： [post]  /upp/v1/license/

##### 2、请求参数说明

```json
{
    "product_name": "产品名",
    "hardware_info": "硬件指纹",
    "token": "令牌",
}
```

##### 3、返回参数说明

```json
{
    "status": 状态码,
    "msg": "返回信息",
    "results": {
        "licenseInfo": "license正文",
        "digitalSign": "license正文的数字签名"
    }
}
```

### 三、令牌延期

##### 1、接口地址： [post]  /upp/v1/token-overtime/

##### 2、请求参数说明

```json
{
    "u_name": "用户名",
    "token": "令牌"
}
```

##### 3、返回参数说明

```json
{
    "status": 状态码,
    "msg": "token过期时间已刷新",
    "results": {
        "token_expire_time": 令牌有效时间
    }
}
```

### 四、获取所有订单信息

##### 1、接口地址： [get]  /upp/v1/token-overtime/

##### 2、请求参数说明

```json
{
    "u_name": "用户名",
    "token": "令牌"
}
```

##### 3、返回参数说明

```json
{
    "status": 状态码,
    "msg": "订单查询成功",
    "results": [
        {
            "product_name": "产品名",
            "total_num": 总数,
            "consume_num": 消耗数,
            "residue_num": 剩余数
        },
        {
            "product_name": "产品名",
            "total_num": 总数,
            "consume_num": 消耗数,
            "residue_num": 剩余数
        },
        ...
    ]
}
```

### 五、状态码说明

| 状态码 | 详细说明 |
| ------ | :------- |
| 200    | OK       |

