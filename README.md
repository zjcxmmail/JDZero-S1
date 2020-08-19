# JD_tools使用说明

> 基于python的薅羊毛小工具
> 欢迎留下对应的shareCode互助

### 主要脚本：

- 种豆得豆 JD_plantBean.py
- 天天加速 JD_speed.py
- 东东农场 JD_dongdongFarm.py
- 东东萌宠 JD_dongdongPet.py
- 宠汪汪   JD_chongWangWang.py
- 摇钱树   moneyTree.py
- 京喜工厂 JD_dreamFactory.py (弃坑)
- 京小超  JD_superMarket.py



### 运行方式

##### 1、方案一 

本地执行、云服务器、云函数等等 

下载到本地，填写`jdCookie.py`中的`cookies`信息

##### 2、方案二(推荐)

GitHub action自动运行，账号信息读取自`Repo-Setting-Secrets`
参考 action.md



### 通知服务

默认不开启，需要通知服务的修改`notification.py`

支持两种通知方式

```
needYou2Know = 0    # [0,1,2]  0:不通知     1:server酱      2:SMTP邮件服务
```

修改参数`needYou2Know`

1. 使用Server酱的需要参数`SCKEY` 
2. 使用SMTP邮件服务的填写`email_dict`
