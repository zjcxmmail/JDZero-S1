import jdCookie
import json
import requests
import time


"""
1、从jdCookie.py处填写 cookie
2、shareCode 为自己的助力码，但是需要别人为自己助力
3、欢迎留下shareCode互助
4、feedTimesLimit 自定义的每天喂养最大次数，防止浪费

"""
feedTimesLimit = 24
shareCodes = [
    "MTAxODc2NTEzMTAwMDAwMDAwOTYwNDkzMQ==", "MTAxODcxOTI2NTAwMDAwMDAwMTY0NTc4OQ==", "MTAxODc2NTEzMDAwMDAwMDAyNjYzMDQ3MQ=="
]  # 自己不能助力自己,填写他人的助力码


def functionTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (('functionId', functionId),)
    data = {'body': json.dumps(body), 'appid': "wh5"}
    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    return json.loads(response.text)


def feedPets(cookies):
    print("\n【feedPets】")
    result = functionTemplate(cookies, "initPetTown", {})["result"]
    foodAmount = result["foodAmount"]
    hadFeedTimes = int(functionTemplate(cookies, "taskInit", {})[
        "result"]["feedReachInit"]["hadFeedAmount"]/10)

    # print(foodAmount, hadFeedAmount)
    if foodAmount < 10:
        print(" [X]跳过feed, food不足:", foodAmount)
        return

    if hadFeedTimes >= feedTimesLimit:
        print(" [X]跳过feed, 到达feed最大值")
        return

    n = feedTimesLimit-hadFeedTimes  # (n>0)
    print(n)

    for i in range(int(foodAmount/10)):  # 剩余狗粮喂养次数
        if n == 0:
            print("喂养次数限制")
            return
        print(f"自动喂养...[{i}]")

        print(functionTemplate(cookies, "feedPets", {}))
        time.sleep(3)
        n -= 1


def energyCollect(cookies):
    print('\n【收集爱心】')
    petPlaceInfoList = functionTemplate(cookies, "initPetTown", {})[
        "result"]["petPlaceInfoList"]

    _place = [i["place"] for i in petPlaceInfoList if i["energy"] > 0]
    if len(_place) == 0:
        print(" [X]暂无")
        return
    for i in _place:
        print(">>>> ", i)
        print(functionTemplate(cookies, "energyCollect", {"place": i}))
        time.sleep(2)


def help(cookies, shareCodes):
    for i in shareCodes:
        # print(i)
        # exit()
        functionTemplate(cookies, "slaveHelp", {"shareCode": str(i)})


def masterHelp(cookies):
    print("\n【好友助力】")
    masterHelpInit = functionTemplate(cookies, "masterHelpInit", {})["result"]
    # print(masterHelpInit)
    if not masterHelpInit["helpLimitFlag"]:
        print("未完成好友助力任务")
    if masterHelpInit["helpLimitFlag"] and masterHelpInit["addedBonusFlag"]:
        print("奖励已经领取")
    if masterHelpInit["helpLimitFlag"] and not masterHelpInit["addedBonusFlag"]:
        print("领取助力奖励")
        print(functionTemplate(cookies, "getHelpAddedBonus", {}))


def sport(cookies):
    print("\n【sport】")

    for i in range(10):
        sport = functionTemplate(cookies, "petSport", {})
    # print(sport)
        if sport["resultCode"] == "3001":
            print(">>>运动次数上限")
            return

        print(f"""sport [{i+1}]""")
        result = functionTemplate(cookies, "getSportReward", {})
        print(result)
        if result["resultCode"] == "1005":
            return
        if result["resultCode"] == "0" and result["result"]["petSportStatus"] == 3:
            # print("需要手动收取")
            time.sleep(2)


def takeTask(cookies):
    print("\n【检查任务】")
    taskList = functionTemplate(cookies, "taskInit", {})["result"]

    _signInit = taskList["signInit"]  # 每日签到
    print(f"""[每日签到]: {_signInit["finished"]}""")
    if not _signInit["finished"]:
        print(functionTemplate(cookies, "getSignReward", {}))

    _threeMealInit = taskList["threeMealInit"]  # 三餐
    print(
        f"""[三餐福袋]: {_threeMealInit["finished"]}""")
    if _threeMealInit["timeRange"] != -1 and _threeMealInit["finished"] == False:  # 时间 、未完成
        print(f"""执行threeMeal{_threeMealInit["timeRange"]}""")
        print(functionTemplate(cookies, "getThreeMealReward", {}))

    _browseSingleShopInit = taskList["browseSingleShopInit"]  # 浏览单个店铺
    print(f"""[指定店铺]: {_browseSingleShopInit["finished"]}""")
    if not _browseSingleShopInit["finished"]:
        print(functionTemplate(cookies, "getSingleShopReward", {}))

    # _browseShopsInit = taskList["browseShopsInit"]  # 浏览店铺 多次
    # print(f"""[多个店铺]: {_browseShopsInit["finished"]}""")
    # if not _browseShopsInit["finished"]:
    #     print(functionTemplate(cookies, "getBrowseShopsReward", {}))

    _firstFeedInit = taskList["firstFeedInit"]  # 每日首次投喂 自动领取
    print(f"""[首次投喂]: {_firstFeedInit["finished"]}""")

    _feedReachInit = taskList["feedReachInit"]  # 每日10次
    print(
        f"""[投喂10次]: {_feedReachInit["finished"]}      feedTimes:({int(_feedReachInit["hadFeedAmount"]/10)}/10)""")


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    status = functionTemplate(cookies, "initPetTown", {})["result"]
    print("\n【检查状态】")
    print(f"""宠物等级: {status["petSportStatus"]}""")
    print(f"""还需能量: {status["needCollectEnergy"]}""")
    print(f"""当前进度: {status["medalPercent"]}%""")
    print(f"""当前饵料: {status["foodAmount"]}""")
    print("我的助力码: ", status["shareCode"])
    help(cookies, shareCodes)
    takeTask(cookies)
    sport(cookies)
    masterHelp(cookies)
    feedPets(cookies)
    energyCollect(cookies)
    # feedPets(cookies)
    # energyCollect(cookies)
    print("\n为防止遗漏，再运行一次")

    print("##"*30)
