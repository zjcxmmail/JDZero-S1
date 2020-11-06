import jdCookie
import json
import requests
import time

"""

宠汪汪
1、FEED_NUM :自定义 每次喂养数量; 等级只和喂养次数有关，与数量无关
2、cron 0 */3 * * *  jd_joy.py  #每隔三小时运行一次，加快升级
3、自动兑换京豆
4、佛系参加双人比赛、领取奖励
"""

FEED_NUM = 10   # [10,20,40,80]
combat_flag = 1  #自动参赛，取消置0
teamLevel = 2  # 双人赛据说不需要门票

headers = {
    'Content-Type': 'application/json',
    'reqSource': 'weapp',
    'Host': 'draw.jdfcloud.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e25) NetType/WIFI Language/zh_CN',
}
headers_app = {
    'Host': 'jdjoy.jd.com',
    'Content-Type': 'application/json',
    'reqSource': 'h5',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'jdapp;iPhone;9.0.6;13.6;Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
    'Referer': 'https://jdjoy.jd.com/pet/index?un_area=2_2823_51974_0&lng=0&lat=0',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
}


def getTemplate(cookies, functionId, params):
    params += (('reqSource', 'weapp'),)
    response = requests.get(f'https://draw.jdfcloud.com//pet/{functionId}',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def postTemplate(cookies, functionId, data):
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    response = requests.post(f'https://draw.jdfcloud.com//pet/{functionId}',
                             headers=headers, cookies=cookies, data=data)
    return response.json()


def postTemplate2(cookies, functionId, data):
    headers["Content-Type"] = "application/json"
    response = requests.post(f'https://draw.jdfcloud.com//pet/{functionId}',
                             headers=headers, cookies=cookies, data=json.dumps(data))
    return response.json()


def enterRoom(cookies):
    print("\n【喂养状态】")
    """
    进入房间；喂养后刷新
    """
    data = getTemplate(cookies, "enterRoom", ())["data"]
    # print(data)
    petFood = data["petFood"]
    feedCount = data["feedCount"]
    petLevel = data["petLevel"]
    print(
        f"""  
现有积分: {data["petCoin"]}
现有狗粮: {petFood}
喂养次数: {feedCount}
宠物等级: {petLevel}
        """
    )
    print("\n【bubble】")
    if not data["bubbleOpen"]:
        print("暂无")
    else:
        print("getBubbleReward  todo")  # TODO
        print(data["bubbleReward"])
        time.sleep(1)
        print(postTemplate(cookies, "getBubbleReward", data["bubbleReward"]))
        print(postTemplate2(cookies, "getBubbleReward", data["bubbleReward"]))


def feed(cookies, feedCount):
    data = getTemplate(cookies, "feed", (('feedCount', str(feedCount)),))
    print("\n【feed】\n ", data["errorCode"])


def takeTask(cookies):
    datas = getTemplate(cookies, "getPetTaskConfig", ())["datas"]
    print("\n任务      进度")
    print("--"*10)
    for i in datas:
        if not i["joinedCount"]:
            i["joinedCount"] = 0
        print(f"""{i["taskName"]}  {i["joinedCount"]}/{i["taskChance"]}""")

        if i["receiveStatus"] == "chance_full":
            continue
        if i["receiveStatus"] == "unreceive":
            print(getTemplate(cookies, "getFood",
                              (('taskType', i["taskType"]),)))

        if i["taskType"] == "SignEveryDay":  # 每日签到
            if i["receiveStatus"] == "chance_left":
                print("     >>>>>需要手动签到")
                # print(getTemplate(cookies, "sign", (('taskType', 'SignEveryDay'),)))

        if i["taskType"] == "FollowShop":  # 关注店铺
            shopIDs = [j["shopId"]
                       for j in i["followShops"] if not j["status"]]
            print(shopIDs)
            for shopId in shopIDs:
                # print(shopId)
                time.sleep(0.5)
                print(postTemplate(cookies, "followShop", {"shopId": shopId}))
                time.sleep(1)

        if i["taskType"] == "ScanMarket":  # 逛逛会场
            marketLists = [j["marketLink"]
                           for j in i["scanMarketList"] if not j["status"]]
            for addr in marketLists:
                data = {"marketLink": str(
                    addr), "taskType": "ScanMarket", "reqSource": "weapp"}
                print(postTemplate2(cookies, "scan", data))
                time.sleep(1)

        if i["taskType"] == "FollowChannel":  # 关注频道
            lists = [j["channelId"]
                     for j in i["followChannelList"] if not j["status"]]
            for addr in lists:
                data = {"channelId": str(
                    addr), "taskType": "FollowChannel", "reqSource": "weapp"}
                print(postTemplate2(cookies, "scan", data))
                time.sleep(1)

        if i["taskType"] == "ViewVideo":  # 激励视频
            for j in range(i["taskChance"]-i["joinedCount"]):
                print(f"""观看视频 [{j}]""")
                print(postTemplate(cookies, "scan", {
                      'taskType': "ViewVideo", 'reqSource': 'weapp'}))
                time.sleep(1)
                print(postTemplate2(cookies, "scan", {
                      'taskType': "ViewVideo", 'reqSource': 'weapp'}))

        if i["taskType"] == "FollowGood":  # 关注商品
            skus = [j["sku"] for j in i["followGoodList"] if not j["status"]]
            print(skus)
            for sku in skus:
                print(postTemplate(cookies, "followGood",
                                   {'sku': str(sku)}))   # bug
                print(postTemplate2(cookies, "followGood", {'sku': str(sku)}))
       
        if i["taskType"] == "PlayWeapp":   # 体验小程序
            appIds = [j["appId"] for j in i["weAppList"] if not j["status"]]
            for appId in appIds:
                print(postTemplate(cookies, "scan", {
                      'appId': str(appId), "taskType": "PlayWeapp"}))


def ScanMarket_extra(cookies):
    """
    补充app端的ScanMarket额外任务
    """
    params = (
        ('reqSource', 'h5'),
        ('taskType', 'ScanMarket'),
    )

    response = requests.get('https://jdjoy.jd.com/pet/getPetTaskConfig',
                            headers=headers_app, params=params, cookies=cookies)
    datas = response.json()["datas"][0]
    if datas["receiveStatus"] == "chance_full":
        return
    if datas["receiveStatus"] == "chance_left":
        print("额外任务")
        marketLists = [j["marketLinkH5"]
                       for j in datas["scanMarketList"] if not j["status"]]
        for addr in marketLists:
            data = {"marketLink": str(
                    addr), "taskType": "ScanMarket", "reqSource": "h5"}
            response = requests.post(
                'https://jdjoy.jd.com/pet/scan', headers=headers, cookies=cookies, data=json.dumps(data))
            print(response.text)
            time.sleep(1)


def desk(cookies):
    print("\n 【限时货柜】")
    response = requests.get('https://jdjoy.jd.com/pet/getDeskGoodDetails',
                            headers=headers_app, cookies=cookies)
    result = response.json()
    # print(result)
    deskGoods = result["data"]["deskGoods"]
    if not deskGoods:
        print("活动下线")
        return
    followCount = result["data"]["followCount"]
    taskChance = result["data"]["taskChance"]
    print(f""" {followCount}/{taskChance}""")
    if followCount == None:
        followCount = 0
    tt = [i["sku"]
          for i in deskGoods if not i["status"]][:(taskChance-followCount)]
    if len(tt) == 0:
        return
    for i in tt:
        data = f"""{{"taskType":"ScanDeskGood","reqSource":"h5","sku":"{i}"}}"""
        response = requests.post('https://jdjoy.jd.com/pet/scan',
                                 headers=headers_app, data=data, cookies=cookies)
        print(response.text)
        time.sleep(1)


def reward(cookies):
    print("\n【兑换京豆】")
    response = requests.get('https://jdjoy.jd.com/gift/getHomeInfo',
                            headers=headers_app, cookies=cookies)
    result = response.json()
    giftSaleInfos = result["data"]["levelSaleInfos"]["giftSaleInfos"]

    jd_bean = [i for i in giftSaleInfos if i["giftType"] == "jd_bean"]
    for i in jd_bean:
        print(f'{i["giftName"]:6}  需要{i["salePrice"]}积分 ')
        if i["leftStock"] == 0:
            print(">>>>>库存不足")
            continue
        data = {
            "orderSource": "pet", "saleInfoId": i["id"]
        }
        response = requests.post('https://jdjoy.jd.com/gift/exchange',
                                 headers=headers_app, data=json.dumps(data), cookies=cookies)
        print(response.text)
    
def combat(cookies):
    if combat_flag == 0:
        return
    print("\n【宠物赛跑】")
    data = getTemplate(
        cookies, "combat/detail/v2", (("help", "false"),))["data"]
    # print(data)
    petRaceResult = data["petRaceResult"]
    print(petRaceResult)
    if petRaceResult == "unbegin":
        print("比赛还未开始")
        return
    if petRaceResult == "time_over":
        print("比赛已结束，明早9点再来哦")
        return
    if petRaceResult == "unreceive":
        print("领取奖励")
        response = requests.get(f'https://jdjoy.jd.com/pet/combat/receive',
                                headers=headers, cookies=cookies)
        print(response.text)
        return
    if petRaceResult == "participate":
        print("===比赛排行榜===")

        def f(status):
            if status:
                return "(myself)"
            return " "
        for i in data["raceUsers"]:
            print(
                f"""{i["rank"]} --- {i["distance"]} -- {i["nickName"]}    {f(i["myself"])} """)
        result = requests.get(f'https://jdjoy.jd.com/pet/combat/getBackupInfo',
                              headers=headers, cookies=cookies).json()["data"]
        print("\n===应援团===")
        backupList = result["backupList"]
        if backupList:
            ii = [i["nickName"] for i in backupList]
            print(ii)
    if petRaceResult == "not_participate":
        print("准备参赛")
        data = requests.get(f'https://jdjoy.jd.com/pet/combat/match?teamLevel={teamLevel}',
                            headers=headers, cookies=cookies)
        print(data.text)
        time.sleep(5)  # 5秒延迟，多账号可能匹配到自己

def run():
    for cookies in jdCookie.get_cookies():
        feed(cookies, FEED_NUM)
        

    for cookies in jdCookie.get_cookies():
        print("\n")
        print(f"""[ {cookies["pt_pin"]} ]""")
        takeTask(cookies)
        reward(cookies)
        ScanMarket_extra(cookies)
        enterRoom(cookies)
        desk(cookies)
        combat(cookies)
        print("##"*25)
if __name__ == "__main__":
    run()