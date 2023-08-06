# qcloud_ccs

qcloud_ccs: 腾讯云容器服务运维命令行工具及sdk
封装腾讯云sdk, 实现:

1. 程序与配置文件分离; 执行时指定当前执行对象服务信息
2. 暴露接口: 启停容器
3. 暴露接口：更新容器配置

## Git仓库地址

https://code.ppgame.com/yw/qcloud_ccs.git

## 依赖
* python 3.4+
* 软件包

> pyyaml==3.12
>
> qcloudapi-sdk-python==2.0.7
>
> requests==2.18.4

## 打包上传到PyPI

[How-to: 提交python软件到PyPI](https://newops.cn/15077893526985.html)

> python setup.py sdist upload

或者

> make && make clean

## qcloud_ccs 使用

### 安装

> pip install qcloud_ccs -U --no-cache-dir

### 配置

* 登录腾讯云容器服务的认证信息

```bash
$ cp account.yml-sample /etc/qcloud_ccs/account.yml
# 也可以将account.yml放在其它目录，使用 --auth/-a 指定
```

* 应用程序的容器服务配置信息

```bash
$ cp product.yml-sample plat-accountcenter-qa.yml
# 将account.yml 配置在这里也可以，优先级最高
```

### 运行

#### 查询用法

```bash
# python3
$ qcloud_ccs -h
```

#### example: 查询当前服务信息

```bash
$ qcloud_ccs -f plat-accountcenter-qa.yml describe_service
```

#### example: 更新配置和镜像，并停止服务(-replicas 0)


```bash
$ qcloud_ccs -config ./product.yml -file templates/application-product.properties-yaml -file-version 100e0624323 -container accounter-qa -tag 1.0.0-e06243.23 -envlist "DBname=test;DBuser=test" -replicas 0 update_service 
```

**重要**

*  一次更新一个配置文件组(configMap)下的所有配置文件(KEY:VALUE)

*  但一次只能更新一组容器(POD)中的一个容器镜像(container image:tag)

**注意**

* 更新配置文件需要传参: -file-version 和 -file; 如果不传或传值为None，则不更新

* 更新镜像需要传参: -tag; 如果不传或传值为None, 则不更新

* 更新服务实例数量要传参: -replicas； 如果不传或值为None,则不更新容器数量， 如果值为0，则停服，如果值为其它，则更新实例数量为指定值
