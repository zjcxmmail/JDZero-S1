import jdCookie
import json
import requests
import time


"""
1、此脚本用于东东农场 【好友】邀请助力 添加好友
2、效果:新加好友时为对方增加10g水;对方执行此脚本同理
3、此助力独立于助力得水，目前助力上限未知
4、欢迎补充一个足够多的shareCodes列表
5、cron 0 */3 * * *
"""
shareCodes = ["c081c648576e4e61a9697c3981705826",
              "f1d0d5ebda7c48c6b3d262d5574315c7",
              "13d13188218a4e3aae0c4db803c81985",
              "d2d5d435675544679413cb9145577e0f",  # DoveBoy
              "101e53c859b5424b8d29fb389aa5aca7",  # muzi13
              "58a45733c946470bb6436bf1ada57be2",  # leeyiding
              "62e6c1861d4c4fbebe1e40f109755100",  # GitCourser
              "f0c3537f49b74bf2a4c7399d8cccda65",  # zhudan
              "3de9821f43c14c33b3c482fd61136633",  # Matear890
              "01766d5c8676418da8f0cf4d49c0640b",  # sdogsq
              "6d06fa98969f4fd2aa8b03b3178cc597",  # sdogsq
              "0f3db2ee6707429eb07fca305121a3d4",  # zaccheo
              "804b416fde154c64a56e6662abd9b6bf",  # kasim
              "5d73bb7a53fd4aef8af8050531e2d6f5",  # watewq
              "8a8ac88e98904f40a25a41c9e492436e",  # zaccheo
              "ac0357128b554a928cad2456c0985db1",  # zaccheo
              "5fc25368858e4418a90975a7d0e23c6c",  # awei4287
              "3b2e1bee164249bca099b60d7e4b0082",  # wuli01
              "6447c9c61b0c4f9a89b6d497fcaf47c9",  # wuli01
              "e4ab3f1c4add4513b07ee88b9c9f7784",  # heros-sky
              ]  # 欢迎在此处填写


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
    _friendsList = [i for i in data["friends"]]
    if not _friendsList:
        print("好友列表为空  跳出")
        print(data)
        return
    lastId = _friendsList[-1]["id"]
    print(f"""fullFriend:{data["fullFriend"]}""")  # 好友添加总数有上限
    if data["fullFriend"]:
        print("好友达到上限,退出")
        return
    for i in range(countOfFriend//20):
        result = postTemplate(cookies, "friendListInitForFarm",
                              {"lastId": lastId})
        pageFriend = [i["shareCode"] for i in result["friends"]]
        if not result["friends"]:
            break

        lastId = [i for i in result["friends"]][-1]["id"]
        myFriendCode += pageFriend
    myshareCode = postTemplate(cookies, 'initForFarm', {})[
        "farmUserPro"]["shareCode"]

    shareCodes_diff = list(
        set(shareCodes).difference(myFriendCode, [myshareCode]))  # 去掉自己以及已是好友关系的shareCode
    print("准备助力的shareCodes:", shareCodes_diff)
    if not shareCodes_diff:
        print("脚本中的shareCodes暂时没发现新好友,退出助力")
    for i in shareCodes_diff:
        data = postTemplate(cookies, "initForFarm", {
            "shareCode": f"{i}-inviteFriend"})
        helpResult = data["helpResult"]
        print(helpResult)  # 目前code未知
        """-1 为自己   17 已经是好友   0 新增好友   猜测有每日上限"""
        if helpResult["code"] == "0":
            print(f"""成功添加好友 [{helpResult["masterUserInfo"]["nickName"]}]""")
        time.sleep(0.5)

def run():
    for cookies in jdCookie.get_cookies():
        print("######################################")
        print(f"""【 {cookies["pt_pin"]} 】""")
        help(cookies)
        print("\n\n######################################")

if __name__ == "__main__":
    run()