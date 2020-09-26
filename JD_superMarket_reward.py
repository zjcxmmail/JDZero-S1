import jdCookie
import json
import requests
import time

# 京小超自动兑换京豆  cron 0 */12 * * *
# 参数设置,开启置1,关闭置0
flag_prize_1000 = 1  # 京豆打包兑换
flag_prize_1 = 1  # 单个京豆兑换,万能的京豆


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


def currentGold(cookies):
    """
    当前金币
    """
    result = getTemplate(cookies, "smtg_home", {})["data"]["result"]
    return result["totalGold"], result["totalBlue"]


def exchangeBean_1(cookies):
    if flag_prize_1 != 1:
        print("[万能的京豆]  自动兑换关闭  flag_prize_1")
        return
    print("[万能的京豆] 兑换开启")
    # _, totalBlue = currentGold(cookies)
    data = getTemplate(cookies, "smtg_queryPrize", {})[
        "data"]
    if data["bizCode"] != 0:
        print(data["bizMsg"])
        return
    prizeList = data["result"]["prizeList"]
    t1 = [i for i in prizeList if i["beanType"] == "Bean"]
    if t1:
        t1 = t1[0]
        print(t1)
        if t1["targetNum"] == t1["finishNum"]:
            print("万能的京豆   今日兑换完成")
            return
        for _ in range(t1["targetNum"]-t1["finishNum"]):
            data = getTemplate(cookies, "smtg_obtainPrize",
                               {"prizeId": t1["prizeId"]})["data"]
            print(data)
            if data["bizCode"] != 0:
                print(data["bizMsg"])
                return
            time.sleep(1)


def exchangeBean_1000(cookies):
    if flag_prize_1000 != 1:
        print("[京豆大礼包]  自动兑换关闭  flag_prize_1000")
        return
    print("[京豆大礼包] 兑换开启")
    _, totalBlue = currentGold(cookies)
    data = getTemplate(cookies, "smtg_queryPrize", {})[
        "data"]
    if data["bizCode"] != 0:
        print(data["bizMsg"])
        return
    prizeList = data["result"]["prizeList"]
    t1000 = [i for i in prizeList if i["beanType"] == "BeanPackage"]
    if t1000:
        t1000 = t1000[0]
        print(t1000)
        if t1000["targetNum"] == t1000["finishNum"]:
            print("京豆大礼包   今日兑换完成")
            return
        if t1000["blueCost"] > totalBlue:
            print("蓝币不足")
            return
        data = getTemplate(cookies, "smtg_obtainPrize",
                           {"prizeId": t1000["prizeId"]})["data"]
        print(data)
        if data["bizCode"] != 0:
            print(data["bizMsg"])


cookiesList = jdCookie.get_cookies()
print("\n >>>>>>【京豆大礼包】")
for cookies in cookiesList:
    print(f"""[{cookies["pt_pin"]}]""")
    exchangeBean_1000(cookies)
    print("\n\n")

print("##"*23)
print("\n >>>>>>【万能的京豆】")
for cookies in cookiesList:
    print(f"""[{cookies["pt_pin"]}]""")
    exchangeBean_1(cookies)
    print("\n\n")
