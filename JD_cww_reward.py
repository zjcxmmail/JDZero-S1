import requests
import json
import time
import jdCookie

"""
宠汪汪积分兑换
每日京豆库存会在0:00、8:00、16:00更新，数量有限，及时运行
"""
# 运行一次，确认好兑换id，此处修改
_id = None  # 210,


def getExchangeRewards(cookies):
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    response = requests.get(
        'https://jdjoy.jd.com/pet/getExchangeRewards', headers=headers, cookies=cookies)

    result = response.json()
    datas = result["datas"]
    score = datas[0]["score"]
    todayExchanged = datas[0]["todayExchanged"]
    petLevel = int((datas[0]["petLevel"]-0.5)/5)+1
    print(f"""当前积分: {score} \n今日兑换: {todayExchanged}""")
    print(f"""兑换等级: {petLevel}""")

    rewardList = []
    for i in datas:
        for j in i["rewardDetailVOS"]:
            rewardList.append(
                {"petLevel": j["petLevel"], "id": j["id"], "petScore": j["petScore"], "rewardName": j["rewardName"], "leftStock": j["leftStock"]})
    print("【所有奖品】")
    for i in rewardList:
        print(i)

    print("\n【可兑奖品】\n 等级符合，积分足够，数量有限")
    for i in rewardList:
        if i["petScore"] <= score and i["petLevel"] <= petLevel:
            print(i)
    return todayExchanged


def exchange(cookies, _id):
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://jdjoy.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1',
        'Accept-Language': 'zh-cn',
    }
    data = {"id": _id}
    response = requests.post(
        'https://jdjoy.jd.com/pet/exchange', headers=headers, cookies=cookies, data=json.dumps(data))
    print(response.text)


for cookies in jdCookie.get_cookies():
    print("\n")
    print(f"""[ {cookies["pt_pin"]} ]""")
    todayExchanged = getExchangeRewards(cookies)
    if not todayExchanged:
        if _id:
            exchange(cookies, _id)
        else:
            print("\n!!!!!运行一次，修改需要的兑换的_id")
    else:
        print("今日已经兑换")
