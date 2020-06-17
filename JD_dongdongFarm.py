import jdCookie
import json
import requests
import time

"""
1、从jdCookie.py处填写 cookie
2、shareCode 为自己的助力码，但是需要别人为自己助力
3、欢迎留下shareCode互助
"""
shareCode = ["c081c648576e4e61a9697c3981705826",
             "f1d0d5ebda7c48c6b3d262d5574315c7",
             "13d13188218a4e3aae0c4db803c81985"]


def TurntableFarm(cookies):
    print("\n【集卡抽奖】")
    print("todo")
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/443.51;apprpd/DongdongFarmMain;ref/https%3A%2F%2Fh5.m.jd.com%2FbabelDiy%2FZeus%2FCvMVbdFGXPiWFFPCc934RiJfMPu%2Findex.html%3Flng%3D0.000000%26lat%3D0.000000%26sid%3D2f6a5275f96a3a5dda89b8ea95f98c4w%26un_area%3D5_274_49707_49973;psq/5;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1837;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Host': 'api.m.jd.com',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/CvMVbdFGXPiWFFPCc934RiJfMPu/index.html?lng=0.000000&lat=0.000000&sid=2f6a5275f96a3a5dda89b8ea95f98c4w&un_area=5_274_49707_49973',
        'Origin': 'https://h5.m.jd.com',
    }

    params = (
        ('functionId', 'initForTurntableFarm'),
        ('body', '{"version":4,"channel":1}'),
        ('appid', 'wh5'),
    )

    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    fruitTotalTimes = result["fruitTotalTimes"]
    print(f"""当前水果卡: {fruitTotalTimes}""")

    turntableBrowserAdsStatus = result["turntableBrowserAdsStatus"]
    print(F"""浏览广告: {turntableBrowserAdsStatus}""")
    turntableBrowserAdsGotStatus = result["turntableBrowserAdsGotStatus"]
    print(F"""浏览广告2: {turntableBrowserAdsStatus}""")
    timingGotStatus = result["timingGotStatus"]
    print(F"""timingGotStatus: {timingGotStatus}""")


def masterHelp(cookies, shareCode):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', 'initForFarm'),
    )
    data = {
        'body': json.dumps({"imageUrl": "", "nickName": "", "shareCode": shareCode, "babelChannel": "3", "version": 2, "channel": 1}),
        "appid": "wh5"
    }
    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, params=params)
    # print(response.text)


def initFarm(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', 'initForFarm'),
    )
    data = {
        'body': json.dumps({"version": 2}),
        "appid": "wh5"
    }
    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    nickName = result["farmUserPro"]["nickName"]
    myshareCode = result["farmUserPro"]["shareCode"]
    print(f"""[ {nickName} ]\n{result["farmUserPro"]["name"]}""")
    print(f"""我的助力码: {myshareCode}""")
    print(
        f"""treeEnergy: {result["farmUserPro"]["treeEnergy"]}/{result["farmUserPro"]["treeTotalEnergy"]}""")


def waterRain(cookies):
    print(">>>>水滴雨")
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/442.92;apprpd/DongdongFarmMain;ref/JDFarmHomeViewController;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1816;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.m.jd.com',
        'Origin': 'https://h5.m.jd.com',
        'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/2SHa5TqJiM5sBC4svoLLxG1CAp3a/index.html?lng=0.000000&lat=0.000000&sid=2f6a5275f96a3a5dda89b8ea95f98c4w&un_area=5_274_49707_49973',
    }

    data = {
        'functionId': 'waterRainForFarm',
        'body': '{"type":1,"hongBaoTimes":100,"version":3}',
        'appid': 'wh5'
    }

    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data)
    print(response.text)


def water(cookies):
    print("\n【Water】")
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'initForFarm'),
    )

    data = {
        'body': json.dumps({"version": 2}),
        "appid": "wh5"

    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)

    totalEnergy = result["farmUserPro"]["totalEnergy"]

    print(f"当前水滴: {totalEnergy}")
    for i in range(int(totalEnergy/10)):
        print(f"自动浇水...[{i}]")
        time.sleep(1)

        params = (
            ('functionId', 'waterGoodForFarm'),
        )

        data = {
            'area': '5_274_49707_49973',
            'body': '{}',
            'appid': "wh5"
        }

        response = requests.post('https://api.m.jd.com/client.action',
                                 headers=headers, params=params, cookies=cookies, data=data)
        print(response.text)


def totalWaterTask(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'totalWaterTaskForFarm'),
    )

    data = {
        'area': '5_274_49707_49973',
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)


def initForTask(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'taskInitForFarm'),
    )

    data = {
        'area': '5_274_49707_49973',
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    print("\n【任务列表】")
    _signInit = result["signInit"]  # 连续签到
    print(f"""todaySigned: {_signInit["todaySigned"]}""")
    if not _signInit["todaySigned"]:
        sign(cookies)

    # _inviteToFarmInit=result["inviteToFarmInit"] #邀请
    _gotBrowseTaskAdInit = result["gotBrowseTaskAdInit"]  # 浏览
    print(f"""BrowseTaskAd: {_gotBrowseTaskAdInit["f"]}""")
    if not _gotBrowseTaskAdInit["f"]:

        for i in _gotBrowseTaskAdInit["userBrowseTaskAds"]:
            print("\n", i["advertId"])
            gotBrowseTaskAdReward(cookies, i["advertId"])

    _gotThreeMealInit = result["gotThreeMealInit"]  # 定时领水 6-9，11-14，17-21
    # print(_gotThreeMealInit)
    print(
        f"""ThreeMeal({_gotThreeMealInit["threeMealAmount"]}): {_gotThreeMealInit["f"]}""")
    if _gotThreeMealInit["f"] == False:
        gotThreeMeal(cookies)

    _firstWaterInit = result["firstWaterInit"]  # 每日首次浇水
    print(f"""firstWater: {_firstWaterInit["f"]}""")
    if not _firstWaterInit["f"]:
        firstWaterTaskForFarm(cookies)

    _totalWaterTaskInit = result["totalWaterTaskInit"]  # 每日累计浇水
    print(
        f"""totalWaterTask: {_totalWaterTaskInit["f"]}  ({_totalWaterTaskInit["totalWaterTaskTimes"]})""")
    if not _totalWaterTaskInit["f"]:
        totalWaterTask(cookies)

    _waterRainInit = result["waterRainInit"]  # 收集水滴雨
    # print(_waterRainInit)
    print(f"""waterRain: {_waterRainInit["winTimes"]}/2""")
    if _waterRainInit["f"] == False:
        waterRain(cookies)


def gotBrowseTaskAdReward(cookies, advertId):
    params = (
        ('functionId', 'browseAdTaskForFarm'),
    )
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'area': '5_274_49707_49973',
        'body': json.dumps({"type": 0, "advertId": advertId}),
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    time.sleep(9)
    data = {
        'area': '5_274_49707_49973',
        'body': json.dumps({"type": 1, "advertId": advertId}),
        'appid': "wh5"
    }
    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)

    # pass


def sign(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'signForFarm'),
    )

    data = {
        'area': '5_274_49707_49973',
        'body': '{"type":2}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    print(response.text)


def firstWaterTaskForFarm(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'firstWaterTaskForFarm'),
    )

    data = {
        'area': '5_274_49707_49973',
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    print(response.text)


def gotThreeMeal(cookies):
    print("三餐定时领取")
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'gotThreeMealForFarm'),
    )

    data = {
        'area': '5_274_49707_49973',
        'body': '{}',
        'appid': "wh5"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    print(response.text)


for cookies in jdCookie.get_cookies():
    initFarm(cookies)
    for i in shareCode:
        masterHelp(cookies, i)
    initForTask(cookies)
    # TurntableFarm(cookies)
    water(cookies)
    print("\n")
    print("##"*30)
