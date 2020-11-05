# JD_tools使用说明

> 基于python的自动化脚本  
> 长期活动，自用为主  
> 低调使用，请勿到处宣传  



### 特别声明:

- 本仓库发布的脚本，仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断

- 本项目内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布

- 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害

- 请勿将本仓库的任何内容用于商业或非法目的，否则后果自负

  

### 主要脚本：

| 名称                                                | 功能           | 备注                     |
| --------------------------------------------------- | -------------- | ------------------------ |
| jdCookie.py                                         | 账号相关       | **必须**，所有功能的入口 |
| notification.py                                     | 通知服务       | **必须**                 |
| jd_farm.py                                          | 东东农场       | 互助                     |
| jd_pet.py                                           | 东东萌宠       | 互助                     |
| jd_joy.py                                           | 宠汪汪         |                          |
| jd_joy_steal.py                                     | 宠汪汪steal    |                          |
| jd_plantBean.py                                     | 种豆得豆       | 互助                     |
| jd_superMarket.py                                   | 东东超市       |                          |
| jd_unfollow.py                                      | 取消订阅       |                          |
| count_bean.py                                       | 当日京豆统计   |                          |
| jd_farm_help.py                                     | 农场添加好友   |                          |
| [xmly_speed](https://github.com/Zero-S1/xmly_speed) | 喜马拉雅极速版 | 其他仓库                 |



### 其他脚本

无需特别配置，每天仅需运行一次的脚本

已集成GitHub action [合集](.github\workflows\工具合集.yml)

| 名称             | 功能       | 备注 |
| ---------------- | ---------- | ---- |
| jd_vvipclub.py   | 摇京豆     |      |
| jd_speed.py      | 天天加速   |      |
| jd_shop.py       | 进店领豆   |      |
| jd_red_packet.py | 全民开红包 |      |


### 运行方式

##### 1、方案一 

本地执行、云服务器、云函数等等 

下载到本地，填写 `jdCookie.py` 中的 `cookies` 信息  

##### 2、方案二(推荐)

GitHub action自动运行，账号信息读取自 `Repo-Setting-Secrets`  
但是 action 定时运行会有延迟  
参考 [action.md](action.md)



### 通知服务

默认不开启，需要通知服务的修改 [notification.py](notification.py)   

"没有消息就是最好的消息" ------ 作者非常懒，懒得写详细通知  

极简通知，目前会发送通知的情况有: 账号cookie过期; 东东农场可收获; 东东萌宠可收获  

支持三种通知方式  

```
 # [0，1，2，3]  0:不通知     1:server酱      2:SMTP邮件服务        3:bark服务
```

修改参数 `needYou2Know`  

1. 使用Server酱的需要参数 `SCKEY` ，支持GitHub action
2. 使用SMTP邮件服务的填写 `email_dict`  
3. 使用bark的填写 `BARK`  ，支持GitHub action

### 自动同步上游仓库

有能力且需要的同学可以参考[讨论](https://github.com/Zero-S1/JD_tools/pull/42)
> 个人不推荐， 因为你不确定上游改动了什么
