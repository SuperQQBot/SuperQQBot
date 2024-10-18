# SuperQQBot
# 新一代QQ机器人SDK框架
# 遵循最新的OneBot11规范
## 1.简介
SuperQQBot是一个基于Python开发的新一代QQ机器人SDK框架，遵循最新OneBot12规范，完美兼容官方的QQBot-py SDK使用方式
## 2.特点
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
## 3.但是
- 我们还在内测（写接口太折磨人了，特别是当接口改了，但是文档没改的时候）
- 所以我们希望大家来参与开发与测试，一起让SuperQQBot变得更好
## 联系我们报告问题或加入开发
1. 主开发者QQ：[点击链接加我为QQ好友](https://qm.qq.com/q/xcLUNrdwwo)
2. QQ群（每次限20人，因为有官方内测机器人【为了内测机器人没有提审，群聊限制20人，敬请谅解】，超人数请加互助群或频道）：[点击链接加入群聊【SuperQQBot SDK官方群聊】](https://qm.qq.com/q/xRKUN02st)
3. QQ频道：[点击链接加入腾讯频道【Bot机器人互助频道】](https://pd.qq.com/s/5lx2mz4dh)
4. 机器人开发互助群：[点击链接加入群聊](https://qm.qq.com/q/POilUp1kUq)
5. 邮箱：[给我发邮箱](mailto:trustedinster@outlook.com)
## 由于技术原因无法直接平替的用法
## [平替模组]()
### 轻微：使用会被警告（可通过平替模组解决）

| 即将弃用的官方SDK用法      | SuperQQBot用法          | 类型 |
|-------------------|-----------------------|----|
| `self.robot.name` | `self.robot.username` | 用法 |
### 严重：无法使用或使用报错（不可通过平替模组解决）

| 已弃用的官方SDK用法 | SuperQQBot用法 | 错误提示 |
|-------------|--------------|------|
|             |              |      |


