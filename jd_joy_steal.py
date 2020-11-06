import requests
import time
import json
import jdCookie

"""
宠汪汪偷好友积分与狗粮，上限20次
cron 2 0,6 * * *
"""
headers = {
    'Host': 'jdjoy.jd.com',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'jdapp;iPhone;9.0.0;13.5',
    'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=0&lat=0',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
}



def getTemplate(cookies, functionId, params):
    params += (('reqSource', 'weapp'),)
    response = requests.get(f'https://jdjoy.jd.com/pet/{functionId}',
                            headers=headers, params=params, cookies=cookies)
    return response.json()



def getFriendsPins(cookies):
    lastPage = getTemplate(cookies, "getFriends", ((
        "itemsPerPage", "20"), ("currentPage", "1")))["page"]["lastPage"]

    friends = []
    for i in range(lastPage):
        result = getTemplate(cookies, "getFriends", ((
            "itemsPerPage", "20"), ("currentPage", str(i+1))))["datas"]
        friends += result
        time.sleep(0.3)
    return [i["friendPin"] for i in friends if i["stealStatus"]]


def steal(cookies, pin):
    print(pin)
    result = getTemplate(
        cookies, "enterFriendRoom", (('friendPin', str(pin)),))["data"]

    print(f"""hasRandomFood: {result["hasRandomFood"]}""")
    print(f"""randomLeftFood: {result["randomLeftFood"]}""")
    print(f"""stealFood: {result["stealFood"]}""")
    if result["friendHomeCoin"]:  # 捡积分
        print(result["friendHomeCoin"])
        print(">>>>get coin")
        result = getTemplate(cookies, "getFriendCoin",
                             (('friendPin', str(pin)),))
        print(result)
        time.sleep(1)
    if "stealFood" not in result:
        return
    if result["stealFood"]:       # 偷狗粮
        print(">>>>get food")
        print(getTemplate(cookies, "doubleRandomFood",
                             (('friendPin', str(pin)),)))
        time.sleep(1)                     
        result = getTemplate(cookies, "getRandomFood",
                             (('friendPin', str(pin)),))
        print(result)
        time.sleep(1)
    print("\n\n")


def run():
    for cookies in jdCookie.get_cookies():
        print("\n")
        print(f"""【 {cookies["pt_pin"]} 】""")
        FriendsPins = getFriendsPins(cookies)
        for pin in FriendsPins:
            steal(cookies, pin)
        print("###"*20)

if __name__ == "__main__":
    run()

