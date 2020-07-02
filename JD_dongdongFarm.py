import jdCookie
import json
import requests
import time

"""
1、从jdCookie.py处填写 cookie
2、shareCode 为自己的助力码，但是需要别人为自己助力
3、欢迎留下shareCode互助
4、waterTimesLimit 自定义的每天浇水最大次数，防止浪费

"""
waterTimesLimit = 24
shareCodes = ["c081c648576e4e61a9697c3981705826",
              "f1d0d5ebda7c48c6b3d262d5574315c7",
              "13d13188218a4e3aae0c4db803c81985"]


def postTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', functionId),
    )
    body = body
    data = {
        'body': json.dumps(body),
        "appid": "wh5"
    }
    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, params=params)
    # print(json.loads(response.text))
    return json.loads(response.text)


def luck(cookies):
    print("\n【随机水滴】")
    result = postTemplate(cookies, "gotWaterGoalTaskForFarm", {"type": 3})
    if result["code"] == "0":
        print("addEnergy ", result["addEnergy"])
    if result["code"] == "7":
        print("暂无")


def initFarm(cookies):
    result = postTemplate(cookies, 'initForFarm', {"version": 2})
    # print(result)
    nickName = result["farmUserPro"]["nickName"]
    myshareCode = result["farmUserPro"]["shareCode"]
    print(f"""\n\n[ {nickName} ]\n{result["farmUserPro"]["name"]}""")
    print(f"""我的助力码: {myshareCode}""")
    print(
        f"""treeEnergy: {result["farmUserPro"]["treeEnergy"]}/{result["farmUserPro"]["treeTotalEnergy"]}""")


def water(cookies, totalWaterTaskTimes):
    print("\n【Water】")
    totalEnergy = postTemplate(cookies, "initForFarm", {"version": 2})[
        "farmUserPro"]["totalEnergy"]
    print(f"当前水滴: {totalEnergy}")
    if totalWaterTaskTimes >= waterTimesLimit:
        print("跳过浇水")
        print("已达今日最大浇水次数 ", waterTimesLimit)
        print("请自行修改 waterTimesLimit")
        return
    n = waterTimesLimit-totalWaterTaskTimes
    for i in range(int(totalEnergy/10)):
        if n == 0:
            print("浇水次数限制,结束浇水")
            return
        print(f"自动浇水...[{i}]")
        time.sleep(0.2)
        postTemplate(cookies, "waterGoodForFarm", {})
        n -= 1


def takeTask(cookies):
    print("\n【任务列表】")

    taskList = postTemplate(cookies, "taskInitForFarm", {})

    _signInit = taskList["signInit"]  # 连续签到
    print(f"""todaySigned: {_signInit["todaySigned"]}""")
    if not _signInit["todaySigned"]:
        print("连续签到")
        postTemplate(cookies, "signForFarm", {"type": 2})

    _gotBrowseTaskAdInit = taskList["gotBrowseTaskAdInit"]  # 浏览
    print(f"""BrowseTaskAd: {_gotBrowseTaskAdInit["f"]}""")
    if not _gotBrowseTaskAdInit["f"]:
        for i in _gotBrowseTaskAdInit["userBrowseTaskAds"]:
            print("浏览广告")
            postTemplate(cookies, "browseAdTaskForFarm", {
                         "type": 0, "advertId": i["advertId"]})
            time.sleep(0.4)
            postTemplate(cookies, "browseAdTaskForFarm", {
                         "type": 1, "advertId": i["advertId"]})

    _gotThreeMealInit = taskList["gotThreeMealInit"]  # 定时领水 6-9，11-14，17-21
    print(
        f"""ThreeMeal: {_gotThreeMealInit["f"]}""")
    if _gotThreeMealInit["f"] == False:
        print("三餐定时领取")
        postTemplate(cookies, "gotThreeMealForFarm", {})

    _firstWaterInit = taskList["firstWaterInit"]  # 每日首次浇水
    print(f"""firstWater: {_firstWaterInit["f"]}""")
    if not _firstWaterInit["f"]:
        print("首次浇水奖励")
        postTemplate(cookies, "firstWaterTaskForFarm", {})

    _totalWaterTaskInit = taskList["totalWaterTaskInit"]  # 每日累计浇水
    print(
        f"""totalWaterTask: {_totalWaterTaskInit["f"]}  ({_totalWaterTaskInit["totalWaterTaskTimes"]}/10)""")
    if not _totalWaterTaskInit["f"]:
        print("浇水10次奖励")
        postTemplate(cookies, "totalWaterTaskForFarm", {})

    _waterRainInit = taskList["waterRainInit"]  # 收集水滴雨
    print(f"""waterRain: {_waterRainInit["winTimes"]}/2""")
    if _waterRainInit["f"] == False:
        print(">>>>水滴雨")
        postTemplate(cookies, "waterRainForFarm", {
            "type": 1, "hongBaoTimes": 100, "version": 3})
    return _totalWaterTaskInit["totalWaterTaskTimes"]


def _help(cookies, shareCodes):
    for i in shareCodes:
        postTemplate(cookies, "initForFarm", {
            "imageUrl": "", "nickName": "", "shareCode": i, "babelChannel": "3", "version": 2, "channel": 1})


def masterHelp(cookies):
    print("\n【助力得水】")
    help_me_list = postTemplate(cookies, "masterHelpTaskInitForFarm", {})
    print(
        f"""完成进度 {len(help_me_list["masterHelpPeoples"])}/5   {help_me_list["f"]}""")
    if not help_me_list["f"]:
        help_me_list1 = postTemplate(
            cookies, "masterGotFinishedTaskForFarm", {})
        print(help_me_list1)


for cookies in jdCookie.get_cookies():
    initFarm(cookies)
    _help(cookies, shareCodes)
    totalWaterTaskTimes = takeTask(cookies)
    masterHelp(cookies)
    luck(cookies)
    water(cookies, totalWaterTaskTimes)
    print("\n")
    print("##"*30)
