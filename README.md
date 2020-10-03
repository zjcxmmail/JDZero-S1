# JD_tools使用说明(暂停维护)

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
- 京小超   JD_superMarket.py
- 京奇世界 jingqiWorld.py
- 摇京豆   JD_vvipclub.py


- 取消关注 jd_unfollow.py
- 互助合集 jdShareCodes.py
- 喜马拉雅极速    [xmly_speed](https://github.com/Zero-S1/xmly_speed) 


### 运行方式

##### 1、方案一 

本地执行、云服务器、云函数等等 

下载到本地，填写`jdCookie.py`中的`cookies`信息  

##### 2、方案二(推荐)

GitHub action自动运行，账号信息读取自`Repo-Setting-Secrets`
参考 action.md



### 通知服务

默认不开启，需要通知服务的修改`notification.py`  
"没有消息就是最好的消息" ------ 作者非常懒,懒得写详细通知  
极简通知,目前会发送通知的情况有: 账号cookie过期; 东东农场可收获; 东东萌宠可收获  
支持三种通知方式  

```
 # [0,1,2,3]  0:不通知     1:server酱      2:SMTP邮件服务        3:bark服务
```

修改参数`needYou2Know`  

1. 使用Server酱的需要参数`SCKEY`   
2. 使用SMTP邮件服务的填写`email_dict`  
3. 使用bark的填写`BARK`

### 自动同步上游仓库

有能力且需要的同学可以参考[讨论](https://github.com/Zero-S1/JD_tools/pull/42)
