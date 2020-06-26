import requests
import time
import json
import jdCookie

"""
1、从jdCookie.py处填写 cookie
2、plantUuid 为自己的助力码，但是需要别人为自己助力
3、欢迎留下plantUuid互助
"""

plantUuid = ["7pt22jcko7ljrbpeask7r6avre3h7wlwy7o5jii",
             "r7zdf2yfo4phlpel3nu4q63reu",
             "e7lhibzb3zek2ssdsoyhpgn26va7nkkzj6ygely"]  # 填写别人的助力码


def functionTemplate(cookies, functionId, body):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'JD4iPhone/167249 (iPhone;iOS 13.5.1;Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1,en-CN;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': "application/x-www-form-urlencoded"
    }
    if "version" not in body:
        body["version"] = "9.0.0.1"
    body["monitor_source"] = "plant_app_plant_index"
    params = (
        ('functionId', functionId),
        ('body', json.dumps(body)),
        ('appid', 'ld'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    return json.loads(response.text)


def takeTask(cookies, taskList):
    # for i in taskList:
    #     print(i,"\n")
    time.sleep(2)
    taskResult = functionTemplate(cookies, "receiveNutrientsTask", {
        "monitor_refer": "receiveNutrientsTask", "awardType": "7"})  # 金融双签 额外
    # print(taskResult)
    time.sleep(2)
    taskResult = functionTemplate(cookies, "receiveNutrientsTask", {
        "monitor_refer": "plant_receiveNutrientsTask", "awardType": "4"})  # 逛逛会场
    # print(taskResult)
    for i in taskList:

        if i["dailyTimes"] == 1 and i["gainedNum"] == "0" and i["taskType"] != 8:
            print(i)
            taskResult = functionTemplate(cookies, "receiveNutrientsTask", {
                "monitor_refer": "receiveNutrientsTask", "awardType": str(i["taskType"])})
            print(taskResult)
            time.sleep(2)
        if i["taskType"] == 7 and i["isFinished"] == 0:  # 金融双签 有时候不出现在taskList
            taskResult = functionTemplate(cookies, "receiveNutrientsTask", {
                "monitor_refer": "receiveNutrientsTask", "awardType": str(i["taskType"])})
            print(taskResult)
            time.sleep(2)
        if i["taskType"] == 3 and i["isFinished"] == 0:
            print("浏览店铺")
            N = int(i["totalNum"])-int(i["gainedNum"])
            plant_shopList = functionTemplate(cookies, "shopTaskList", {
                                              "monitor_refer": "plant_receiveNutrients"})["data"]
            goodShopList = [
                i for i in plant_shopList["goodShopList"] if i["taskState"] == "2"]
            moreShopList = [
                i for i in plant_shopList["moreShopList"] if i["taskState"] == "2"]
            shopList = goodShopList + moreShopList
            for shop in shopList:
                shopTaskId = shop["shopTaskId"]
                shopId = shop["shopId"]
                result = functionTemplate(cookies, "shopNutrientsTask", {
                                          "monitor_refer": "plant_shopNutrientsTask", "shopId": str(shopId), "shopTaskId": str(shopTaskId)})
                print(result)
                if "data" in result:
                    if result["data"]["nutrState"] == "1":
                        N -= 1
                if N == 0:
                    break
                time.sleep(1)
        if i["taskType"] == 10 and i["isFinished"] == 0:
            print("关注频道")
            N = int(i["totalNum"])-int(i["gainedNum"])
            plant_ChannelList = functionTemplate(
                cookies, "plantChannelTaskList", {})["data"]
            goodChannelList = [
                i for i in plant_ChannelList["goodChannelList"] if i["taskState"] == "2"]
            normalChannelList = [
                i for i in plant_ChannelList["normalChannelList"] if i["taskState"] == "2"]
            channelList = goodChannelList+normalChannelList

            for channel in channelList:
                result = functionTemplate(cookies, "plantChannelNutrientsTask", {"channelTaskId": channel["channelTaskId"], "channelId": channel["channelId"]
                                                                                 })
                print(result)
                if "data" in result:
                    if result["data"]["nutrState"] == "1":
                        N -= 1
                if N == 0:
                    break
                time.sleep(1)
        if i["taskType"] == 5 and i["isFinished"] == 0:
            print("挑选商品")
            N = int(i["totalNum"])-int(i["gainedNum"])
            productInfoList = functionTemplate(cookies, "productTaskList", {
                                               "monitor_refer": "plant_productTaskList"})["data"]["productInfoList"]
            productList = sum(productInfoList, [])
            productList = list(
                filter(lambda i: i["taskState"] == "2", productList))

            for product in productList:
                result = functionTemplate(cookies, "productNutrientsTask", {
                                          "productTaskId": product["productTaskId"], "skuId": product["skuId"], "monitor_refer": "plant_productNutrientsTask"})
                print(result)
                if "data" in result:
                    if result["data"]["nutrState"] == "1":
                        N -= 1
                if N == 0:
                    break
                time.sleep(1)


def _help(cookies, plantUuid):
    for i in plantUuid:
        functionTemplate(cookies, "plantBeanIndex", {
                         "plantUuid": i, "followType": "1", "wxHeadImgUrl": "", "shareUuid": "", })


def steal(cookies, roundId):
    print("\n【偷取营养液】\n默认对方有3个才会偷取\n不足自动跳过 ")
    pageNum = 1
    while("data" in functionTemplate(cookies, "plantFriendList", {"pageNum": str(pageNum)})):
        time.sleep(2)
        result = functionTemplate(cookies, "plantFriendList", {
                                  "pageNum": str(pageNum)})
        # print(result)
        if "tips" in result["data"]:
            print("今日已达上限")
            # exit()
            return
        # exit()
        stealList = [i for i in result["data"]
                     ["friendInfoList"] if "nutrCount" in i]

        for i in stealList:

            if int(i["nutrCount"]) == 3:  # 为3时才会偷取
                print(i)
                print(functionTemplate(cookies, "collectUserNutr", {
                    "paradiseUuid": i["paradiseUuid"], "roundId": roundId}))
                time.sleep(2)


def getReward(cookies, status):
    print("\n[收获状况]")
    if status == "5":
        data = functionTemplate(
            cookies, "receivedBean", {"roundId": lastRoundId})["data"]
        print(f"""{data["growth"]}成长值兑换{data["awardBean"]}京豆""")
    if status == "6":
        print("您已领奖，去京豆明细页看看")


def water(cookies):
    print("\n[浇水ing]")
    result = functionTemplate(cookies, "cultureBean", {
        "roundId": currentRoundId, "monitor_refer": "plant_index"})
    if "errorMessage" in result:
        print(result["errorMessage"])
        return


def egg(cookies):
    print("\n[天天扭蛋]")
    restLotteryNum = functionTemplate(cookies, "plantEggLotteryIndex", {})[
        "data"]["restLotteryNum"]
    if restLotteryNum == 0:
        print(">>>暂无扭蛋")
    for i in range(restLotteryNum):
        print(">>>扭蛋 ", i+1)
        functionTemplate(cookies, "plantEggDoLottery", {})


def waterWheel(cookies):
    print("\n[水车生产(6-21)]")
    result = functionTemplate(cookies, "receiveNutrients", {
        "roundId": currentRoundId, "monitor_refer": "plant_receiveNutrients"})
    if "errorMessage" in result:
        print(result["errorMessage"])
        return


for cookies in jdCookie.get_cookies():
    plantBeanIndex = functionTemplate(cookies, "plantBeanIndex", {})

    print(
        f"""【{plantBeanIndex["data"]["plantUserInfo"]["plantNickName"]}】\n""")
    print(
        f"""我的助力码: {plantBeanIndex["data"]["jwordShareInfo"]["shareUrl"].split("=")[-1]}\n""")
    _help(cookies, plantUuid)
    roundList = plantBeanIndex["data"]["roundList"]
    lastRoundId = roundList[0]["roundId"]  # 上期id
    currentRoundId = roundList[1]["roundId"]  # 本期id
    taskList = plantBeanIndex["data"]["taskList"]  # 任务列表
    takeTask(cookies, taskList)  # 执行每日任务
    print("     任务   进度")
    for i in functionTemplate(cookies, "plantBeanIndex", {})["data"]["taskList"]:
        print(
            f"""[{i["taskName"]}]  {i["gainedNum"]}/{i["totalNum"]}   {i["isFinished"]} """)

    egg(cookies)
    waterWheel(cookies)
    steal(cookies, currentRoundId)
    water(cookies)
    getReward(cookies, roundList[0]["awardState"])
    print("\nEND\n")
    print("##"*30)
