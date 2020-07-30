import requests
import json
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

cookiesLists=[cookies1,]  #多账号准备


def valid(cookies):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'jdapp;iPhone;8.5.5;13.5;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('functionId', 'plantBeanIndex'),
        ('body', json.dumps(
            {"monitor_source": "plant_m_plant_index", "version": "8.4.0.0"})),
        ('appid', 'ld'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    if response.json()["code"] == "3":
        print(f"""## {cookies["pt_pin"]}: cookie过期""")
        return False
    return True

def get_cookies():
    return [i for i in cookiesLists if valid(i)]


# get_cookies()
print("***"*20)
print("***"*20)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("\n报错请至 https://github.com/Zero-S1/JD_tools\n")
