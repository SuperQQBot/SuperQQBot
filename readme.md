<div align="center">
<img src="Logo.png">
<h1>SuperQQBot</h1>

[![Language](https://img.shields.io/badge/language-python-green.svg?style=plastic)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPL2.0-orange.svg?style=plastic)](https://github.com/tencent-connect/botpy/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![PyPI](https://img.shields.io/pypi/v/SuperQQBot)
![OneBot](https://img.shields.io/badge/OneBot-12-black)


_✨ 基于 [机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/) 实现的新一代机器人框架 ✨_

_✨ 为开发者提供一个易使用、开发效率高地开发框架 ✨_
</div>

# 新一代QQ机器人SDK框架

## 1. 简介

SuperQQBot是一个基于Python开发的新一代QQ机器人SDK框架，遵循最新OneBot12规范，完美兼容官方的QQBot-py SDK使用方式

## 2. 特点

### 高包容性

源代码放宽了一部分的规范，做了指令优化，对官方SDK的用户更加友好。目标是实现官方SDK代码无缝迁移，减轻开发者迁移负担

### 性能高

1. 使用了多线程，多进程，多协程等优化，以提升性能
2. 致力于代码优化，减少不必要的IO操作，提升性能
3. AI赋能，让代码性能再上一层楼

### 稳定可靠

官方的烂摊子开发者们受够了，你的烂摊子我们不接！让我们重新构造SDK的新生态。作者将为源代码提供稳定的支持

### 方便易用

- 官方的API文件对新手小白来说极为吃力
- 官方的SDK文档根本不靠谱
- 在我们的错误信息中添加了更加人性化的中文解决方案，不再为错误感到担忧
- 我们构建了新SDK架构，让新手小白也能1秒上手，后期打算搭建GUI界面，让机器人编程不再是大佬的专有名词

### 社区活跃

1. 官方的SDK社区已经处于休眠状态，距离上一次更新已经有超过一年了，好多接口已经过时
2. 去官方频道反馈没有人处理，官方似乎已经弃坑此项目
3. 我们的社区成员活跃，主开发者愿意倾心帮助大家，并经常维护

### 合法合规

我们用的全部是官方的接口，官方的机器人参数，不存在封号风险

## 3. 用法
### PIP工具安装（由于国内镜像源更新缓慢，推荐使用官方接口）
#### 直接安装（如果配置了镜像可能下到旧版本）
```bash
pip install SuperQQBot
```
#### 国外镜像（稳定，但是速度慢）
```bash
pip install -i https://pypi.org/simple SuperQQBot
```
### 手动通过whl安装（速度快，稳定，但是麻烦）
1. 从本站下载[最新的whl包](https://gitee.com/SuperQQBot/SuperQQBot/releases/tags/lastest)
2. *（可选，用于快速安装依赖）从本站下载[最新的requirements.txt文件](https://gitee.com/SuperQQBot/SuperQQBot/raw/master/requirements.txt)，然后在Bash中执行
```bash
pip install -r requirements.txt
```
3. 在whl包的下载目录执行安装库：
```bash
pip install SuperQQBot-0.0.1-py3-none-any.whl
```

## 4. 但是

- 我们还在内测（写接口太折磨人了，特别是当接口改了，但是文档没改的时候）
- 所以我们希望大家来参与开发与测试，一起让SuperQQBot变得更好

## 5. 单元测试

代码库提供API接口测试和 websocket 的单测用例，位于 `tests` 目录中。如果需要自己运行，可以在 `tests` 目录重命名 `.test.yaml`
文件后添加自己的测试参数启动测试：

### 单测执行方法

先确保已安装 `pytest` ：

```bash
pip install pytest
```

然后在项目根目录下执行单测：

```bash
pytest
```

## 联系我们报告问题或加入开发

1. 主开发者QQ：[点击链接加我为QQ好友](https://qm.qq.com/q/xcLUNrdwwo)
2. QQ群（每次限20人，因为有官方内测机器人【为了内测机器人没有提审，群聊限制20人，敬请谅解】，超人数请加互助群或频道）：[点击链接加入群聊【SuperQQBot SDK官方群聊】](https://qm.qq.com/q/xRKUN02st)
3. QQ频道：[点击链接加入腾讯频道【Bot机器人互助频道】](https://pd.qq.com/s/5lx2mz4dh)
4. 机器人开发互助群：[点击链接加入群聊](https://qm.qq.com/q/POilUp1kUq)
5. 邮箱：[给我发邮箱](mailto:trustedinster@outlook.com)
6. Gitee组织：[加入SuperQQBot组织](https://gitee.com/SuperQQBot)

## 由于技术原因无法直接平替的用法

### [平替模组](https://gitee.com/Root_cty/SuperQQBot-official-mod)

### 轻微：通过平替模组解决

| 即将弃用的官方SDK用法      | SuperQQBot用法          | 类型    |
|-------------------|-----------------------|-------|
| `self.robot.name` | `self.robot.username` | API用法 |
| `public_messages` | `GROUP_AND_C2C_EVENT` | 消息订阅  |

### 严重：无法使用或使用报错（不可通过平替模组解决）

| 已弃用的官方SDK用法 | SuperQQBot用法 | 错误提示 |
|-------------|--------------|------|
|             |              |      |


