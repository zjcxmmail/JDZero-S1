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
    for _ in range(5):
        # print(i)
        data = getTemplate(cookies, "smtg_receiveCoin", {"type": 2})["data"]
        # print(data)
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
    shelfList = getTemplate(cookies, "smtg_shelfList", {})[
        "data"]["result"]["shelfList"]

    for i in shelfList:
        print(i)
        print(f'位置: {i["index"]+1}')
        print(f"""货架等级: {i["level"]}/{i["maxLevel"]}""")
        # groundStatus 2 解锁有货  0 未解锁  1 解锁无货
        print("--"*20)


def productList(cookies):
    print("\n【我的商品】")
    productList = getTemplate(cookies, "smtg_productList", {})[
        "data"]["result"]["productList"]
    for i in productList:
        print(i)


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
        # print(i)
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


def ground(cookies, productId, shelfId):
    print(f">>>安排生产")
    data = getTemplate(cookies, "smtg_ground", {
                       "productId": productId, "shelfId": shelfId})
    print(data)


def unlockproduct(cookies, productId):
    print(f">>>解锁商品[{productId}]")
    data = getTemplate(cookies, "smtg_unlockProduct", {"productId": productId})
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
    time.sleep(1)


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    dailyTask(cookies)
    receiveCoin(cookies)
    receiveBlue(cookies)
    print("##"*25)
    print("\n\n")
