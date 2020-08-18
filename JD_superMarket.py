import jdCookie
import json
import requests
import time

"""
京小超
1.日常任务
2.领小费 蓝币
3.领金币
cron 5 * * * *

金币使用顺序:
1、解锁货架
2、检查货架可上架的产品(优先上架限时商品)
    若无,解锁一个对应类型的商品
3、不升级货架和商品

"""


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


def receiveBlue(cookies):
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


def shelfList(cookies):
    print("\n【我的货架】")
    print("#######################################")
    shelfList = getTemplate(cookies, "smtg_shelfList", {})[
        "data"]["result"]["shelfList"]

    for i in shelfList:
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
        print(f"""unlockStatus:{i["unlockStatus"]}""")
        print(f"""upgradeStatus:{i["upgradeStatus"]}""")
        print(f"""priceGold:{i["priceGold"]}""")


def currentGold(cookies):
    """
    当前金币
    """
    return getTemplate(cookies, "smtg_home", {})["data"]["result"]["totalGold"]


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
                        for i in productList if i["productType"] == 2]
    if limitTimeProduct:
        print("优先上架限时产品")
        ground(cookies, limitTimeProduct[0], shelfId)
        return
    ground(cookies, productList[-1]["productId"], shelfId)
    return


def obtainPrize(cookies, prizeId):
    """
    蓝币兑奖，自行调用
    """
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.8;13.6;Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Host': 'api.m.jd.com',
        'Referer': 'https://jdsupermarket.jd.com/game',
        'Origin': 'https://jdsupermarket.jd.com',
    }
    params = (
        ('appid', 'jdsupermarket'),
        ('functionId', 'smtg_obtainPrize'),
        ('clientVersion', '8.0.0'),
        ('client', 'm'),
        ('body', json.dumps({"prizeId": prizeId})),
    )

    response = requests.post('https://api.m.jd.com/api', headers=headers,
                             params=params, cookies=cookies)
    print(response.text)


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    shelfList(cookies)
    sign(cookies)
    dailyTask(cookies)
    receiveCoin(cookies)
    receiveBlue(cookies)
    print("##"*25)
    print("\n\n")
