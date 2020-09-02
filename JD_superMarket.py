import jdCookie
import json
import requests
import time

"""
京小超 cron 5 * * * * 

1.日常任务、商圈pk任务、领取pk奖励
2.自动领取金币、蓝币小费
3.货架与商品的解锁、上架、升级
4.优先上架限时商品和领取限时商品的蓝币奖励
5.自动兑换京豆奖励

金币使用顺序:
1、解锁货架
2、检查货架可上架的产品(优先上架限时商品)
     若无,解锁一个对应类型的商品
     

金币使用顺序(额外):
1.解锁、升级商品(跳过低级商品)
2.升级货架

TODO:
优先安排生产
"""
# 参数设置,开启置1,关闭置0
flag_prize_1000 = 1  # 京豆打包兑换(优先)
flag_prize_1 = 1  # 单个京豆兑换
flag_upgrade = 0  # 额外,自动升级   顺序:解锁升级商品(高等)、升级货架

# 商圈助力码
inviteCodes = ["IhM_beyxYPwg82i6iw", "YF5-KbvnOA", "eU9YaLm0bq4i-TrUzSUUhA"]


def getTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.8;13.6;Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Host': 'api.m.jd.com',
        'Referer': 'https://jdsupermarket.jd.com/game',
        'Origin': 'https://jdsupermarket.jd.com',
    }

    params = (
        ('appid', 'jdsupermarket'),
        ('functionId', functionId),
        ('clientVersion', '8.0.0'),
        ('client', 'm'),
        ('body', json.dumps(body)),
    )

    response = requests.get('https://api.m.jd.com/api',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def postTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.8;13.6;Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Host': 'api.m.jd.com',
        'Referer': 'https://jdsupermarket.jd.com/game',
        'Origin': 'https://jdsupermarket.jd.com',
    }

    params = (
        ('appid', 'jdsupermarket'),
        ('functionId', functionId),
        ('clientVersion', '8.0.0'),
        ('client', 'm'),
        ('body', json.dumps(body)),
    )

    response = requests.get('https://api.m.jd.com/api',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def receiveBlue(cookies):
    print("\n【限时商品蓝币领取】")
    data = getTemplate(cookies, "smtg_receiveCoin", {"type": 1})["data"]
    print(data)
    print(data["bizMsg"])
    print("\n【领取小费】")
    for _ in range(10):
        data = getTemplate(cookies, "smtg_receiveCoin", {"type": 2})["data"]
        if data["bizCode"] != 0:
            print(data["bizMsg"])
            return
        print(
            f"""totalBlue:{data["result"]["totalBlue"]}(+{data["result"]["receivedBlue"]})""")
        time.sleep(4)


def receiveCoin(cookies):
    print("\n【收银台收钱】")
    data = getTemplate(cookies, "smtg_receiveCoin", {"type": 0})["data"]
    if data["bizCode"] == 802:
        print(data["bizMsg"])
        return
    print(
        f"""totalGold:{data["result"]["totalGold"]}(+{data["result"]["receivedGold"]})""")


def upgrade(cookies):
    if flag_upgrade == 0:
        return
    print(">>>检查升级商品")
    data = getTemplate(cookies, "smtg_productList", {})[
        "data"]["result"]["productList"]

    productList = [i for i in data if i["productType"] == 1]
    shelfCategory_1 = [i for i in productList if i["shelfCategory"] == 1][-3:]
    shelfCategory_2 = [i for i in productList if i["shelfCategory"] == 2][-3:]
    shelfCategory_3 = [i for i in productList if i["shelfCategory"] == 3][-2:]

    for i in shelfCategory_1+shelfCategory_2+shelfCategory_3:
        if i["unlockStatus"] == 1:
            unlockproduct(cookies, i["productId"])
            return
        if i["upgradeStatus"] == 1:
            upgradeproduct(cookies, i["productId"])
            return
    print(">>>检查升级货架")
    shelfList = getTemplate(cookies, "smtg_shelfList", {})[
        "data"]["result"]["shelfList"]
    shelfList_upgrade = [i for i in shelfList if i["upgradeStatus"] == 1]
    if len(shelfList_upgrade) == 0:
        return
    tt = sorted(shelfList_upgrade, key=lambda keys: keys['upgradeCostGold'])
    upgradeShelf(cookies, tt[0]["shelfId"])


def shelfList(cookies):
    print("\n【我的货架】")
    print("#######################################")
    shelfList = getTemplate(cookies, "smtg_shelfList", {})[
        "data"]["result"]["shelfList"]

    for i in shelfList:
        # print(i)
        print(f'shelfId: {i["shelfId"]} ({i["name"]})')
        print(f"""货架等级: {i["level"]}/{i["maxLevel"]}""")
        # print(f"""groundStatus:{i["groundStatus"]}""")  # 1可上架 23已上架 0 不可上架
        # print(f"""unlockStatus:{i["unlockStatus"]}""")  # 2已解锁  1 可解锁 0不可解锁
        # print(f"""upgradeStatus:{i["upgradeStatus"]}""")  # 1可升级 0 不可
        if i["unlockStatus"] in [0, 1]:
            print(">>>>货架未解锁")
        if i["unlockStatus"] == 1:
            unlockShelf(cookies, i["shelfId"])
        if i["groundStatus"] == 1:
            shelfProductList(cookies, i["shelfId"])  # 检查可上架
        if i["groundStatus"] in [2, 3]:
            productTypeDict = {1: "", 2: "(限时商品)"}
            print(
                f"""[{i["productInfo"]["name"]}]{productTypeDict[i["productInfo"]["productType"]]}""")
        print("--"*20)


def sign(cookies):
    print("\n【每日签到】")
    hadSigned = getTemplate(cookies, "smtg_signList", {})[
        "data"]["result"]["hadSigned"]
    if hadSigned == 1:
        print("sign ok")
        return
    if hadSigned == 2:
        print(getTemplate(cookies, "smtg_sign", {}))


def productList(cookies):
    print("\n【我的商品】")
    productList = getTemplate(cookies, "smtg_productList", {})[
        "data"]["result"]["productList"]
    for i in productList:
        print(i["productId"])
        if i["productType"] == 2:
            print("限时商品")
            continue


def currentGold(cookies):
    """
    当前金币
    """
    result = getTemplate(cookies, "smtg_home", {})["data"]["result"]
    return result["totalGold"], result["totalBlue"]


def dailyTask(cookies):
    print("\n【店铺任务】")
    taskList = getTemplate(cookies, "smtg_queryShopTask", {})[
        "data"]["result"]["taskList"]
    for i in taskList:
        print(f"""{i["title"]:>5}   {i["finishNum"]}/{i["targetNum"]}""")
        if i["taskStatus"] == 1 and i["prizeStatus"] == 1:
            print("obtainShopTaskPrize: ", getTemplate(cookies, "smtg_obtainShopTaskPrize",
                                                       {"taskId": i["taskId"]}))
        if i["taskStatus"] == 1:
            continue
        if i["type"] == 1:  # 分享
            print("doshareTask: ", getTemplate(cookies, "smtg_doShopTask",
                                               {"taskId": i["taskId"]}))
        if i["type"] in [2, 8]:  # 会场,商铺
            itemId = i["content"][list(i["content"].keys())[0]]["itemId"]
            print("doShopTask: ", getTemplate(cookies, "smtg_doShopTask",
                                              {"taskId": i["taskId"], "itemId": itemId}))
        if i["type"] == 6:
            productList = getTemplate(cookies, "smtg_productList", {})[
                "data"]["result"]["productList"]
            productListUpgrade = [
                i for i in productList if "upgradeStatus" in i and i["upgradeStatus"] == 1]
            if productListUpgrade:
                upgradeproduct(cookies, productListUpgrade[-1]["productId"])


def ground(cookies, productId, shelfId):
    print(f">>>安排生产")
    data = getTemplate(cookies, "smtg_ground", {
                       "productId": productId, "shelfId": shelfId})
    print(data)


def unlockproductbyCategory(cookies, Category):
    """
    根据类型解锁一个商品,货架可上架商品时调用
    """
    productList = getTemplate(cookies, "smtg_productList", {})[
        "data"]["result"]["productList"]
    productListByCategory = [
        i for i in productList if "unlockStatus" in i and i["unlockStatus"] == 1 and str(i["shelfCategory"]) == str(Category)]
    if not productListByCategory:
        print("该类型商品暂时无法解锁")
        return
    unlockproduct(cookies, productListByCategory[-1]["productId"])


def unlockproduct(cookies, productId):
    print(f">>>解锁商品[{productId}]")
    data = getTemplate(cookies, "smtg_unlockProduct", {"productId": productId})
    print(data)


def upgradeproduct(cookies, productId):
    print(f">>>升级商品[{productId}]")
    data = getTemplate(cookies, "smtg_upgradeProduct",
                       {"productId": productId})
    print(data)


def upgradeShelf(cookies, shelfId):
    print(f">>>升级货架[{shelfId}]")
    data = getTemplate(cookies, "smtg_upgradeShelf", {"shelfId": shelfId})
    print(data)
    time.sleep(1)


def unlockShelf(cookies, shelfId):
    print(f">>>解锁货架[{shelfId}]")
    data = getTemplate(cookies, "smtg_unlockShelf", {"shelfId": shelfId})
    print(data)


def shelfProductList(cookies, shelfId):
    print(f">>>检查货架[{shelfId}]可上架产品")
    productList = getTemplate(cookies, "smtg_shelfProductList", {"shelfId": shelfId})[
        'data']["result"]["productList"]

    if not productList:
        print("无可上架产品")
        unlockproductbyCategory(cookies, shelfId.split("-")[-1])
        return
    limitTimeProduct = [i["productId"]
                        for i in productList if i["productType"] == 2]  # 此处限时商品未分配才会出现
    if limitTimeProduct:
        print("优先上架限时产品")
        ground(cookies, limitTimeProduct[0], shelfId)
        return
    ground(cookies, productList[-1]["productId"], shelfId)
    return


def queryPrize(cookies):
    if not flag_prize_1 and not flag_prize_1000:
        return
    print("\n【兑换京豆查询】")
    _, totalBlue = currentGold(cookies)
    prizeList = getTemplate(cookies, "smtg_queryPrize", {})[
        "data"]["result"]["prizeList"]
    t = [i for i in prizeList if i["type"] == 3]
    if flag_prize_1000 == 1:
        tt = t[1]
        if tt["targetNum"] == tt["finishNum"]:
            print("[京豆大礼包]今日兑换完成")
            return
        if tt["blueCost"] <= totalBlue:
            print(getTemplate(cookies, "smtg_obtainPrize",
                              {"prizeId": tt["prizeId"]}))
        else:
            print("[京豆大礼包] Blue不足")
    if flag_prize_1 == 1:
        tt = t[0]
        if tt["targetNum"] == tt["finishNum"]:
            print("[万能的京豆]今日兑换完成")
            return
        if totalBlue < tt["blueCost"]:
            print("[万能的京豆] Blue不足")
            return

        for i in range(tt["targetNum"]-tt["finishNum"]):
            data = getTemplate(cookies, "smtg_obtainPrize",
                               {"prizeId": tt["prizeId"]})["data"]
            # print(data)
            if data["bizCode"] == 507:
                print("[万能的京豆] 个人兑换次数限制")
                return
            time.sleep(1)
            if data["result"]["exchangeNum"] == tt["targetNum"] or data["result"]["blue"] < tt["blueCost"]:
                print("[万能的京豆] 无法兑换")
                return


def limitTimePro(cookies):
    data = getTemplate(cookies, "smtg_productList", {})[
        "data"]["result"]["productList"]
    productList = [i for i in data if i["productType"]
                   == 2 and i["groundStatus"] == 1]  # 未上架的限时
    for i in productList:
        shelfCategory = i["shelfCategory"]
        data = getTemplate(cookies, "smtg_shelfList", {})[
            "data"]["result"]["shelfList"]
        shelfList = [i["shelfId"] for i in data if i["shelfCategory"]
                     == shelfCategory and i["groundStatus"] == 2]
        for j in shelfList:
            productList = getTemplate(cookies, "smtg_shelfProductList", {"shelfId": j})[
                'data']["result"]["productList"]
            productList=[i for i in productList if i["productType"]==1]
            list2=sorted(productList,key=lambda productList: productList["previewTotalPriceGold"])
            print(list2[-1])


def businessCircle(cookies):
    data = getTemplate(cookies, "smtg_businessCirclePKDetail", {})[
        "data"]
    if data["bizCode"] != 0:
        # print(data)
        print(data["bizMsg"])
        if data["bizCode"] == 206:
            print(getTemplate(cookies, "smtg_joinBusinessCircle", {
                  "circleId": "IhM_beyxYPwg82i6iw_1598314711414"}))
        # return
    result = getTemplate(cookies, "smtg_businessCircleIndex", {})[
        "data"]["result"]
    pkPrizeStatus = result["pkPrizeStatus"]
    if pkPrizeStatus == 2:
        print("领取PK奖励")
        result = getTemplate(cookies, "smtg_getPkPrize", {})["data"]["result"]
        print(result)
        return
    
    pkStatus = result["pkStatus"]
    print("pkStatus: ",pkStatus)
    if pkStatus==2:
        return
    print(f"""pkPrizeStatus:{pkPrizeStatus}\n""")
    print("\n【我的商圈】")
    # print(getTemplate(cookies, "smtg_quitBusinessCircle", {}))
    result = data["result"]
    print(f"""inviteCode:{result["inviteCode"]}""")
    BusinessCircleVO = result["businessCircleVO"]
    # print(f"""circleId:{BusinessCircleVO["circleId"]}""")
    otherBusinessCircleVO = result["otherBusinessCircleVO"]
    print(
        f"""memberCount(对方/我方): {otherBusinessCircleVO["memberCount"]}/{BusinessCircleVO["memberCount"]}""")
    print(
        f"""hotPoint(对方/我方): {otherBusinessCircleVO["hotPoint"]}/{BusinessCircleVO["hotPoint"]}""")
    result = getTemplate(cookies, "smtg_queryPkTask", {})["data"]["result"]
    print(f'我的贡献:{result["self"]["current"]}/{result["self"]["target"]}')
    for i in inviteCodes:
        getTemplate(cookies, "smtg_doAssistPkTask", {"inviteCode": i})
    for i in result["taskList"]:
        if i["prizeStatus"] == 1:
            print(getTemplate(cookies, "smtg_obtainPkTaskPrize",
                              {"taskId": i["taskId"]}))
        if i["taskStatus"] == 1:
            continue
        if i["assignmentType"] != 0:
            for j in range(10):
                if str(j) in i["content"]:
                    print(postTemplate(cookies, "smtg_doPkTask",
                                       {"taskId": i["taskId"], "itemId": i["content"][str(j)]["itemId"]}))
                    break
        print("\n")


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    # limitTimePro(cookies)
    # continue
    queryPrize(cookies)
    businessCircle(cookies)
    shelfList(cookies)
    upgrade(cookies)
    sign(cookies)
    dailyTask(cookies)
    receiveCoin(cookies)
    receiveBlue(cookies)
    print("##"*25)
    print("\n\n")
