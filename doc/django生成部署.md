# django + uwsgi + nginx部署

# 0、概述

+ 部署后的效果

<center>
    <img src="img\部署后效果图.jpg" />
    <center>部署效果</center>
</center>

+ 部署流程

  <center>
      <img src="img\部署流程.jpg">
      <center>部署流程</center>
  </center>

  + 参考

    https://www.zhihu.com/question/22850801?sort=created

    https://www.jianshu.com/p/956debe2891d

## 一、uwsgi部署

### 1、安装

- 命令

```text
sudo apt-get install build-essential python-dev
pip install uwsgi
```

- 测试安装是否成功

在本地写如下测试代码test_uwsgipy

```python
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return ["success!"]
```

　该目录下输入以下命令：

```text
uwsgi --http :8000 --wsgi-file test.py
```

访问8000端口

```text
curl 127.0.0.1:8000 
```

成功返回success

## 2、配置

+ 在项目路径下创建uwsgi.ini 文件, 配置如下:

```text
[uwsgi]
# 使用nginx连接时 使用
socket=127.0.0.1:8888

# 直接作为web服务器使用
http=127.0.0.1:8889
# 配置工程目录
chdir=/home/zero/django/AuthoringSystem

# 配置项目的wsgi目录。相对于工程目录
wsgi-file=AuthoringSystem/wsgi.py

#配置进程，线程信息
processes=4

threads=10

enable-threads=True

master=True

pidfile=uwsgi.pid

daemonize=uwsgi.log

```

+ 命令：

```text
启动：uwsgi --ini uwsgi.ini
停止：uwsgi --stop uwsgi.pid
重启：uwsgi --reload uwsgi.pid
```

## 二、nginx部署

### 1、安装

+ 命令

```text
sudo apt-get install nginx
service nginx start
```

查看是否启动成功:

```text
curl 127.0.0.1
```

### 2、配置

+ 根据项目创建_nginx.conf文件，内容如下：

```text
# the upstream component nginx needs to connect to
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8888; # for a web port socket (we'll use this first)
}
 
# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name 192.168.3.50; # substitute your machine's IP address or FQDN
    charset     utf-8;
 
    # max upload size
    client_max_body_size 75M;   # adjust to taste
 
    # Django media
    location /media  {
        alias /home/zero/django/AuthoringSystem/media;  # your Django project's media files - amend as required
    }
 
    location /static {
        alias /home/zero/django/AuthoringSystem/static; # your Django project's static files - amend as required
    }
 
    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
}
```

+ 然后把这个配置文件链接到sites-enabled目录下:

sudo ln -s /home/zero/django/AuthoringSystem/authsys_nginx.conf /etc/nginx/sites-enabled/authsys_nginx.conf

+ 检查一下配置文件的语法是否有问题，提示ok就可以

```text
sudo service nginx configtest
```

+ 重启服务：

```text
service nginx restart
```

+ 测试

```text
curl 127.0.0.1:8000
```

+ 接口或者web测试

  在python manage.py runserver命令下测试通过的脚本或者命令，此时应该可以正常运行

## 补充知识

### 1、正向代理

我访问不了某网站比如[www.google.com](https://links.jianshu.com/go?to=http%3A%2F%2Fwww.google.com)，但是我能访问一个代理服务器，这个代理服务器呢，它能访问那个我不能访问的网站，于是我先连上代理服务器，告诉它我需要那个无法访问网站的内容，代理服务器去取回来,然后返回给我。正向代理的过程，隐藏了真实的请求客户端，服务端不知道真实的客户端是谁，客户端请求的服务都被代理服务器代替来请求。

<center>
    <img src="img\正向代理.jpg">
    <center>正向代理示意</center>
</center>

### 2、反向代理

当我们请求 [www.baidu.com](https://links.jianshu.com/go?to=http%3A%2F%2Fwww.baidu.com) 的时候，当我们访问[www.baidu.com](https://links.jianshu.com/go?to=http%3A%2F%2Fwww.baidu.com)的时候，背后可能有成千上万台服务器为我们服务，但具体是哪一台，不知道，也不需要知道，只需要知道反向代理服务器是谁就好了，[www.baidu.com](https://links.jianshu.com/go?to=http%3A%2F%2Fwww.baidu.com) 就是我们的反向代理服务器，反向代理服务器会帮我们把请求转发到真实的服务器那里去。反向代理隐藏了真实的服务端。

<center>
    <img src="img\反向代理.jpg">
    <center>反向代理示意</center>
</center>

