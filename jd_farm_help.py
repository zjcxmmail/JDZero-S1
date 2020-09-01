import jdCookie
import json
import requests
import time


"""
1、此脚本用于东东农场 【好友】邀请助力 添加好友
2、效果:新加好友时为对方增加10g水;对方执行此脚本同理
3、此助力独立于助力得水，目前助力上限未知
4、欢迎补充一个足够多的shareCodes列表
"""
shareCodes = ["c081c648576e4e61a9697c3981705826",
              "f1d0d5ebda7c48c6b3d262d5574315c7",
              "13d13188218a4e3aae0c4db803c81985"]  # 欢迎在此处填写


def postTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', functionId),
    )
    data = {
        'body': json.dumps(body),
        "appid": "wh5",
        "clientVersion": "9.1.0"
    }
    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, params=params)
    return response.json()


def help(cookies):
    print("\n")
    data = postTemplate(cookies, "friendListInitForFarm",
                        {})
    print("他人运行此脚本为我助力")
    print(f"""今日新增好友: {data["inviteFriendCount"]}/10""")
    if data["inviteFriendCount"] > 0 and data["inviteFriendCount"] > data["inviteFriendGotAwardCount"]:
        print("领取邀请奖励")
        print(postTemplate(cookies, "awardInviteFriendForFarm", {}))
    print("\n>>>开始为他人助力")
    myFriendCode = [i["shareCode"]
                    for i in data["friends"] if "shareCode" in i]
    countOfFriend = data["countOfFriend"]
    lastId = [i for i in data["friends"]][-1]["id"]
    print(f"""fullFriend:{data["fullFriend"]}""")  # 好友添加总数有上限
    for i in range(countOfFriend//20):
        result = postTemplate(cookies, "friendListInitForFarm",
                              {"lastId": lastId})
        pageFriend = [i["shareCode"] for i in result["friends"]]

        lastId = [i for i in result["friends"]][-1]["id"]
        myFriendCode += pageFriend
    myshareCode = postTemplate(cookies, 'initForFarm', {})[
        "farmUserPro"]["shareCode"]

    shareCodes_diff = list(
        set(shareCodes).difference(myFriendCode, [myshareCode]))  # 去掉自己以及已是好友关系的shareCode
    print("准备助力的shareCodes:", shareCodes_diff)
    if not shareCodes_diff:
        print("脚本中的shareCodes暂时没发现新好友")
    for i in shareCodes_diff:
        data = postTemplate(cookies, "initForFarm", {
            "shareCode": f"{i}-inviteFriend"})
        helpResult = data["helpResult"]
        print(helpResult)  # 目前code未知
        """-1 为自己   17 已经是好友   0 新增好友   猜测有每日上限"""
        if helpResult["code"] == "0":
            print(f"""成功添加好友 [{helpResult["masterUserInfo"]["nickName"]}]""")
        time.sleep(0.5)


for cookies in jdCookie.get_cookies():
    print("######################################")
    print(f"""【 {cookies["pt_pin"]} 】""")
    help(cookies)
    print("\n\n######################################")
