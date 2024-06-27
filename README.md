<p align="center">
  <a href="https://github.com/LinYuanovo/pikpak_auto_invite">
    <img src="https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/faviconV2.png" alt="Logo" width="80" height="80">
  </a>
  <h1 align="center">PikPak自动邀请</h1>
  <p align="center">
    ·
    <a href="https://github.com/LinYuanovo/pikpak_auto_invite/issues">报告Bug</a>
    ·
    <a href="https://github.com/LinYuanovo/pikpak_auto_invite/issues">提出新特性</a>
  </p>
</p>

基于bilibili平台UP主[纸鸢花的花语](https://space.bilibili.com/67788420/)所公开的源码以及其群管理Atong的pikpak临时碰撞版脚本进行修改的PikPak自动邀请程序，附带图像识别过验证码

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->

## 目录

- [作者](#作者)
- [说明](#说明)
- [上手指南](#上手指南)
  - [本地运行](#本地运行)
  - [GitHub Actions运行（每日云端定时自动运行）](#GitHubActions运行)
- [文件目录说明](#文件目录说明)

### 作者

临渊

邮箱：<1577242215@qq.com>

### 说明

- 本项目仅仅只是在UP主[纸鸢花的花语](https://space.bilibili.com/67788420/)所公开的源码以及其群管理Atong的脚本基础上进行简单修改，加入了图像识别处理验证码，并未进行任何架构上的更改。上传本项目也仅为了用于学习研究以及备份，无任何不良引导，如有侵权请联系我进行删除。如果项目对你有帮助欢迎点点star。
- 项目可以依赖于GitHub Actions自动运行，无需任何环境
- 官方限制现在邀请的会员掉了人数也不会掉，所以邀请之前请查看自己人数是否超**50**人
- **因为是刷取的会员，所以很大概率会掉，所以建议日常注册小号获取会员来保存资源，需要的时候再把资源分享给大号，让大号刷会员使用资源**
- 如账号出现问题本人概不负责，建议小号使用

### 上手指南

#### 本地运行

##### 使用前的配置

在使用本项目前请确保你具有以下环境

1. Python[推荐Python3.9~~别问为什么，我就是3.9，别的我不知道能不能运行~~]（如未安装请查看[Python安装教程](https://blog.csdn.net/maiya_yayaya/article/details/131828467?ops_request_misc=&request_id=&biz_id=102&utm_term=python如何安装&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-131828467.142^v100^pc_search_result_base7&spm=1018.2226.3001.4187)）
2. pip（如未安装请查看[pip安装及如何加速安装第三方组件](https://blog.csdn.net/figo0423/article/details/136146344?ops_request_misc=%7B%22request%5Fid%22%3A%22171784122216800226579490%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=171784122216800226579490&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-7-136146344-null-null.142^v100^pc_search_result_base7&utm_term=pip如何安装&spm=1018.2226.3001.4187)）

##### **安装步骤**

1. 克隆项目到本地，如无法克隆也可以直接从右上角下载zip压缩包到本地解压

```shell
git clone https://github.com/LinYuanovo/pikpak_auto_invite.git
```

2. 进入到项目目录

```shell
cd pikpak_auto_invite
```

3. 安装项目所需依赖（如安装有问题自行换源）

```shell
pip install -r requirements.txt
```

##### 效果演示

在项目目录下用终端输入或利用`Pycharm`等工具直接运行`run.py`

```shell
python run.py
```

![效果演示](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/7c010670-6d0c-41c0-8ad5-d6dab5e6bf02.png)

如果需要查看请求返回信息，请将主程序`run.py`的`DEBUG_MODE`参数设为True

如果多次出现IP问题可尝试将自己所用的魔法设置为代理，即主程序`run.py`的`PROXY`参数

#### GitHubActions运行

[B站-视频教程](https://www.bilibili.com/video/BV1JZ3FeWEsF/)

1. 点击项目右上角进行**fork**，也可以顺手点个**star**

    ![对项目进行fork](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/f43174c1-1576-4ab0-b86f-31355b400887.png)

2. 然后点击你fork的项目中的**Settings**，找到**Secrets and variables**，选中**Actions**里的**New repository secret**添加一个环境变量，名称必须为**INVITE_CODE**，内容就填你的邀请码，如果是多个邀请码，用换行或者@进行分割。

    ![添加变量](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/8ad57054-1c8b-4100-8e24-ab8d6ef51899.png)

    ![添加变量](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/1a702216-0a12-44c4-8067-54eb8e34e7c5.png)

3. （可选）如果需要推送结果到微信，建议使用pushplus推送服务，添加一个环境变量，名称必须为**PUSHPLUS_TOKEN**，内容就填你的pushplus的token（[token获取方法](https://pushplus.plus/push1.html)）。

    ![填写pushplus变量](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/Snipaste_2024-06-27_14-50-57.png)

4. 点击你项目上方的**Actions**，第一次打开可能需要点击 `I understand...`，来启用actions

5. 提交修改来触发Actions，建议直接修改`run.py`，在空白的地方输入一次换行**commit**提交即可

    ![修改run.py](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/44e7cf20-658a-4400-99a3-35babc2d5834.png)

    ![提交修改](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/cca72584-36be-4b16-b0bb-141899eaa1b5.png)

6. 点开**Actions**查看运行日志

    ![查看日志](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/3e58af4c-bf57-496c-9129-d237fd0aae7d.png)

    ![查看日志](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/2cbadd33-bb64-4619-bc38-f86b3bd59ed8.png)

    至此操作完成，每天晚六点十分定时执行一次（可以自己到`/.github/workflows/run.yml`中修改定时），可以以同样方式进入**Actions**查看日志
    
    如果你启用了PUSHPLUS_TOKEN环境变量，效果如下所示
    
    ![推送结果](https://raw.githubusercontent.com/LinYuanovo/pic_bed/main/pikpak_auto_invite/61874733-02e9-4118-816c-4e35791de986.png)

### 文件目录说明

```
pikpak_auto_invite 
├── /.github/
│  │──  /workflows/
│  │  │── run.yml           Github Actions配置文件
├── README.md
├── /models/
│  │── pikpak3.0.onnx       图像识别模型
│  │── pikpak4.0.onnx       图像识别模型
│  │── charsets.json        配置
├── /temp/                  缓存验证图片
├── run.py                  程序主入口
├── image.py                处理图片
└── recognize.py            图像识别
```


<!-- links -->

[your-project-path]:LinYuanovo/pikpak_auto_invite
[contributors-shield]: https://img.shields.io/github/contributors/LinYuanovo/pikpak_auto_invite.svg?style=flat-square
[contributors-url]: https://github.com/LinYuanovo/pikpak_auto_invite/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/LinYuanovo/pikpak_auto_invite.svg?style=flat-square
[forks-url]: https://github.com/LinYuanovo/pikpak_auto_invite/network/members
[stars-shield]: https://img.shields.io/github/stars/LinYuanovo/pikpak_auto_invite.svg?style=flat-square
[stars-url]: https://github.com/LinYuanovo/pikpak_auto_invite/stargazers
[issues-shield]: https://img.shields.io/github/issues/LinYuanovo/pikpak_auto_invite.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/LinYuanovo/pikpak_auto_invite.svg
