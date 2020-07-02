import requests
import time
import json
import jdCookie


"""
收、卖
七日签到
三餐签到
分享

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
    print("\n【收获金果】")
    # 收获金果
    data = {
        'reqData': json.dumps({"source": 2, "sharePin": None, "userId": userInfo['userInfo'], "userToken": userInfo['userToken']})
    }

    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/harvest?_={int(time.time()*1000)}',
                             headers=headers, data=data, cookies=cookies)
    treeInfo = json.loads(response.text)["resultData"]["data"]["treeInfo"]
    # print(treeInfo)
    print(treeInfo["treeName"])
    print("金果数量: ", treeInfo["fruit"])
    print("升级剩余: ", treeInfo["progressLeft"])


def sell(cookies):
    print("\n sell")
    time.sleep(1)
    data = 'reqData={"source":2,"riskDeviceParam":"{\\"fp\\":\\"\\",\\"eid\\":\\"\\",\\"sdkToken\\":\\"\\",\\"sid\\":\\"\\"}"}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/sell?_={int(time.time()*1000)}',
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
    print("分享任务  test")
    time.sleep(1)
    data = 'reqData={"source":0,"workType":2,"opType":1}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    print(response.text)
    time.sleep(2)
    data = 'reqData={"source":0,"workType":2,"opType":2}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/doWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    print(response.text)


def dayWork(cookies, userInfo):
    time.sleep(1)
    data = {
        'reqData': json.dumps({"source": 2, "linkMissionIds": ["666", "667"], "LinkMissionIdValues": [7, 7]})
    }
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/dayWork?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    data = json.loads(response.text)["resultData"]["data"]
    dailyTask = [i for i in data if i["prizeType"] == 2]
    time.sleep(1)
    for i in dailyTask:

        if i["workType"] == 1:  # 三餐签到
            print("【三餐签到】")
            if i["workStatus"] == 0:
                sign(cookies, userInfo)
            if i["workStatus"] == 2:
                print("ok")
        if i["workType"] == 2:  # 每日分享
            print("【分享】")
            if i["workStatus"] == 0:
                share(cookies, userInfo)
            if i["workStatus"] == 2:
                print("ok")


def signOne(cookies):
    print("\n【连续签到】")
    data = 'reqData={"source":2}'
    response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/signIndex?_{int(time.time()*1000)}', headers=headers,
                             cookies=cookies, data=data)
    data = json.loads(response.text)["resultData"]["data"]
    if data["canSign"] == 2:
        body = {'reqData': json.dumps(
            {"source": 2, "signDay": data["signDay"]})}
        response = requests.post(f'https://ms.jr.jd.com/gw/generic/uc/h5/m/signOne?_{int(time.time()*1000)}', headers=headers,
                                 cookies=cookies, data=body)
        result = json.loads(response.text)
        print(result)
    if data["canSign"] == 1:
        print("ok")


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    signOne(cookies)
    userInfo = user_info(cookies)
    dayWork(cookies, userInfo)
    harvest(cookies, userInfo)  # 收获
    sell(cookies)               # 卖出
    print("\n")
    print("###"*20)
