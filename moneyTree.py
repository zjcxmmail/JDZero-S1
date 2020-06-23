import requests
import time
import json
import jdCookie


"""
测试版
只完成了收金果
其他功能待测试

cron */6 * * * *   # 表示每6分钟收取一次，自行计算运行间隔
"""

headers = {
    'Host': 'ms.jr.jd.com',
    'Accept': 'application/json',
    'Origin': 'https://uuj.jr.jd.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Referer': 'https://uuj.jr.jd.com/wxgrowing/moneytree7/index.html?channellv=sy',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'X-Requested-With': 'com.jd.jrapp',
}


def user_info(cookies):
    data = {
        'reqData': '{"shareType":1,"source":0,"riskDeviceParam":"{\\"fp\\":\\"\\",\\"eid\\":\\"\\",\\"sdkToken\\":\\"\\",\\"sid\\":\\"\\"}"}'
    }
    response = requests.post(
        f'https://ms.jr.jd.com/gw/generic/uc/h5/m/login?_={int(time.time()*1000)}', headers=headers, data=data, cookies=cookies)

    return (response.json()['resultData']['data'])


def harvest(cookies, userInfo):
    print("\n收获金果")
    # 收获金果
    data = {
        'reqData': json.dumps({"source": 2, "sharePin": None, "userId": userInfo['userInfo'], "userToken": userInfo['userToken']})
    }

    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/harvest?_={int(time.time()*1000)}',
                             headers=headers, data=data, cookies=cookies)
    print(response.text)


def sign(cookies, userInfo):
    # 签到  test
    print("\n每日签到")
    data = 'reqData={"source":2,"workType":1,"opType":2}'

    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)

    print(response.text)


def share(cookies, userInfo):
    # 分享任务  test
    data = 'reqData={"source":2,"workType":2,"opType":1}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    print(response.text)
    time.sleep(2)
    data = 'reqData={"source":2,"workType":2,"opType":2}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    print(response.text)


def dayWork(cookies):
    data = 'reqData={"source":2,"linkMissonIds":["666","667"],"LinkMissonIdValues":[7,7]}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/dayWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    data=json.loads(response.text)["resultData"]["data"]
    dailyTask=[i for i in data if i["prizeType"]==2]
    for i in dailyTask:
        print(i,"\n")




for cookies in jdCookie.get_cookies():
    userInfo = user_info(cookies)
    harvest(cookies, userInfo)    #收获
