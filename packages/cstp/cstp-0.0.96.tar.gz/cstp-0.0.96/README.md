# CSTP

CSTP(Command String List Transfer Protocol) library wrote by Weber Juche.

2016.5.27


## CSTP包功能说明

### 设计目的
实现“串列表”明文协议的客户端和服务端封装。

#### “串列表”明文协议
以串为核心来传输数据。


#### 客户端封装
TCmdStringSck.py

#### 服务端封装
TCmdStringHub.py


## 相关命令如下

````
$ python setup.py sdist  # 编译包
$ python setup.py sdist upload  # 上传包
$ pip install --upgrade --no-cache-dir cstp
````