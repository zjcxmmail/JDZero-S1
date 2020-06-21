import jdCookie
import json
import requests
import time

"""
东东萌宠
1、从jdCookie.py处填写 cookie
2、shareCode 为自己的助力码，但是需要别人为自己助力
3、欢迎留下shareCode互助
"""

shareCodes = [
    "MTAxODc2NTEzMTAwMDAwMDAwOTYwNDkzMQ==", 
    "MTAxODcxOTI2NTAwMDAwMDAwMTY0NTc4OQ==",
    "MTAxODc2NTEzMDAwMDAwMDAyNjYzMDQ3MQ==",
]  # 自己不能助力自己,填写他人的助力码


def initPetTown(cookies):
    print("\n【检查状态】\n")
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'initPetTown'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)

    data = result["result"]
    # print(data)
    # petPlaceInfoList = data["petPlaceInfoList"]
    petSportStatus = data["petSportStatus"]
    _shareCode = data["shareCode"]

    print(f"""宠物等级: {petSportStatus}""")
    print(f"""还需能量: {data["needCollectEnergy"]}""")
    print(f"""当前进度: {data["medalPercent"]}%""")
    print(f"""当前饵料: {data["foodAmount"]}""")
    print("我的助力码: ", _shareCode)


def update_info(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'initPetTown'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    data = result["result"]
    petPlaceInfoList = data["petPlaceInfoList"]

    j = 0
    for i in petPlaceInfoList:
        if i["energy"] > 0:
            energyCollect(cookies, i["place"])
        j += 1

    return data["foodAmount"]


def sport(cookies):

    print("\n【sport】")
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/443.87;apprpd/DongdongFarmMain;ref/JDFarmHomeViewController;psq/0;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1851;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'petSport'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    if result["resultCode"] == "3001":
        print(">>>运动次数上限")
        return
    for i in range(10):
        headers = {
            'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/443.87;apprpd/DongdongFarmMain;ref/JDFarmHomeViewController;psq/0;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1851;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1',
            'Host': 'api.m.jd.com',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = (
            ('functionId', 'getSportReward'),
        )

        data = {

            'body': '{}',
            'appid': "wh5"
        }

        response = requests.post('https://api.m.jd.com/client.action',
                                 headers=headers, params=params, cookies=cookies, data=data)
    # print("getSportReward  ", response.text)


def feedPets(cookies, foodAmount):
    print("\n【feedPets】")
    if foodAmount < 10:
        print(" [X]跳过feed, food不足:", foodAmount)
        return
    for _ in range(int(foodAmount/10)):
        headers = {
            'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
            'Host': 'api.m.jd.com',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = (
            ('functionId', 'feedPets'),
        )

        data = {
            'body': '{}',
            'appid': "wh5"
        }

        response = requests.post('https://api.m.jd.com/client.action',
                                 headers=headers, params=params, cookies=cookies, data=data)
        time.sleep(1)


def energyCollect(cookies, place):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'energyCollect'),
    )

    data = {
        'body': f"""{{"place":{place}}}""",
        'appid': "wh5"
    }
    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)


def initTask(cookies):
    print("\n【任务状态】")
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'taskInit'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    data = result["result"]
    _signInit = data["signInit"]  # 每日签到
    print(f"""[dailySign]: {_signInit["finished"]}""")
    if not _signInit["finished"]:
        getSignReward(cookies)

    _threeMealInit = data["threeMealInit"]  # 三餐
    print(
        f"""[threeMeal]: {_threeMealInit["finished"]}""")
    if _threeMealInit["timeRange"] != -1 and _threeMealInit["finished"] == False:  # 时间 、未完成
        print(f"""执行threeMeal{_threeMealInit["timeRange"]}""")
        threeMealReward(cookies)
    _browseSingleShopInit = data["browseSingleShopInit"]  # 浏览单个店铺
    print(f"""[browse_1_Shop]: {_browseSingleShopInit["finished"]}""")
    if not _browseSingleShopInit["finished"]:
        getSingleShopReward(cookies)
    _browseShopsInit = data["browseShopsInit"]  # 浏览店铺 多次
    print(f"""[browse_more_Shops]: {_browseShopsInit["finished"]}""")
    if not _browseShopsInit["finished"]:

        getBrowseShopsReward(cookies)

    _firstFeedInit = data["firstFeedInit"]  # 每日首次投喂
    print(f"""[feed_1]: {_firstFeedInit["finished"]}""")

    _feedReachInit = data["feedReachInit"]  # 每日10次
    print(
        f"""[feed_10]: {_feedReachInit["finished"]}      feedTimes:({int(_feedReachInit["hadFeedAmount"]/10)}/10)""")
    return {"hadFeedAmount": int(_feedReachInit["hadFeedAmount"]/10), }


def getSignReward(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'getSignReward'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)


def getBrowseShopsReward(cookies):
    print(">>>浏览店铺")
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'getBrowseShopsReward'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    # print(response.text)


def getSingleShopReward(cookies):
    print(">>>>单个广告")
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'getSingleShopReward'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)


def _help(cookies, shareCode):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', 'slaveHelp'),
    )
    data = {
        'body': json.dumps({"shareCode": shareCode}),
        'appid': "wh5"
    }
    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)


def threeMealReward(cookies):

    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'getThreeMealReward'),
    )

    data = {
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    # print(response.text)


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    initPetTown(cookies)
    for i in shareCodes:
        _help(cookies, i)
    initTask(cookies)
    sport(cookies)
    foodAmount = update_info(cookies)
    feedPets(cookies, foodAmount)
    update_info(cookies)
    print("\n")
    print("##"*20)
    # exit()

