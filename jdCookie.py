import requests
import re
import time

"""
1、抓包，登录 https://bean.m.jd.com 点击签到并且出现签到日历后
2、返回抓包，搜索关键词 functionId=signBean 复制Cookie中的pt_key与pt_pin填入以下两个空白处
3、注意，cookies会过期,大约为一个月
4、python3.6+ 环境，需要requests包

集中cookie管理
多账号准备
过期检查
"""

cookies1={
'pt_key': '',    #cookie参数填写
'pt_pin': '',
}

cookies2={}   # 如果有其它账号，还需要将cookies2填写进 下面的cookieLists

cookieLists=[cookies1,]  #多账号准备



def isNot_valid(cookies):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'jdapp;iPhone;8.5.5;13.4;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167121;supportBestPay/0;jdSupportDarkMode/0;pv/103.2;apprpd/MyJD_Main;ref/https%3A%2F%2Fbean.m.jd.com%2FplantBean%2Findex.action%3Fsource%3Dwojing%26un_area%3D5_274_49707_49973%26lng%3D116.8438383685941%26lat%3D39.95744163210918;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|219;jdv/0|direct|-|none|-|1583449735697|1583796810;adk/;app_device/IOS;pap/JA2015_311210|8.5.5|IOS 13.4;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('functionId', 'plantBeanIndex'),
        ('body', f"""{{"monitor_refer":"","wxHeadImgUrl":"","shareUuid":"7pt22jcko7ljrbpeask7r6avre3h7wlwy7o5jii","followType":"1","monitor_source":"plant_m_plant_index","version":"8.4.0.0"}}"""),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.5'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('uuid', '9b812b59e055cd226fd60ebb5fd0981c4d0d235d'),
        ('jsonp', 'jsonp_1585181731771_80279'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    f= re.fullmatch(r"jsonp\w+\({\"code\":\"3\"}\);", response.text,flags=0) #返回None表示有效；反之
    if f!=None:
        print(f"""## {cookies["pt_pin"]}: cookie过期""")
    return f

def get_cookies():
    i= [i for i in cookieLists if not isNot_valid(i)]
    return i
    
print("***"*20)
print("***"*20)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
