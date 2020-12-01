import jdCookie
import json
import requests
import time
import random

"""
京小超 cron 5 * * * *  
基本完结

1.日常任务
2.自动领取金币、蓝币小费
3.货架与商品的解锁、上架、升级
4.*空货架*优先上架限时商品和领取限时商品的蓝币奖励
5.自动兑换京豆奖励 
6.优先安排生产最大单价商品 
7.限时商品*替换*普通商品

金币使用顺序:
1、解锁货架
2、检查货架可上架的产品(优先上架限时商品)
     若无,解锁一个对应类型的商品
     

金币使用顺序(额外):
1.解锁、升级商品(跳过低级商品)
2.升级货架


"""
# 参数设置,开启置1,关闭置0
flag_upgrade = 1              # 额外,自动升级   顺序:解锁升级商品(高等)、升级货架
flag_limitTimeProduct = 1     # 自动上架限时商品(替换普通商品,同类型至少两个商品)
flag_pk = 1                   # 自动加入zero的队伍
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
    totalGold = data["result"]["totalGold"]
    print(
        f"""totalGold:{format(totalGold,",")} (+{format(data["result"]["receivedGold"],",")})""")


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
        print(i["unlockStatus"], i["name"])
        # if i["unlockStatus"] == 1:
        #     # print(i)
        #     unlockproduct(cookies, i["productId"])
        #     break
        if i["upgradeStatus"] == 1:
            upgradeproduct(cookies, i["productId"])
            break
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
    data = getTemplate(cookies, "smtg_signList", {})["data"]
    if data["bizCode"] != 0:
        print(data["bizMsg"])
        return
    hadSigned = data["result"]["hadSigned"]
    if hadSigned == 1:
        print("每日签到 ok")
    if hadSigned == 2:
        print("每日签到 ", getTemplate(cookies, "smtg_sign", {}))
    hadReceivedAddedReward = data["result"]["hadReceivedAddedReward"]
    if hadReceivedAddedReward == 1:
        print("额外签到 ok")
    if hadReceivedAddedReward == 0:
        print("额外签到 ", getTemplate(cookies, "smtg_sign", {"channel": "1"}))


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
        if i["type"] in [1, 11]:  # 分享、指定入口
            print("doshareTask: ", getTemplate(cookies, "smtg_doShopTask",
                                               {"taskId": i["taskId"]}))
        if i["type"] in [2, 8, 10]:  # 会场,商铺
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


def limitTimePro(cookies):
    print("\n>>>>上架限时商品")
    if flag_limitTimeProduct != 1:
        print("flag_limitTimeProduct不为1 跳出")
        return
    data = getTemplate(cookies, "smtg_productList", {})[
        "data"]["result"]["productList"]
    productList = [i for i in data if i["productType"]
                   == 2 and i["groundStatus"] == 1]  # 未上架的限时
    if not productList:
        print("限时商品已经上架或暂时没有限时商品")
        return
    for i in productList:
        shelfCategory = i["shelfCategory"]
        data = getTemplate(cookies, "smtg_shelfList", {})[
            "data"]["result"]["shelfList"]
        shelfList = [i["shelfId"] for i in data if i["shelfCategory"]
                     == shelfCategory and i["groundStatus"] in [1, 2]]
        print(shelfList)
        if len(shelfList) > 1:
            ground(cookies, i["productId"], shelfList[-1])


def lottery(cookies):
    print("\n【招财进宝】")
    for _ in range(3):
        result = getTemplate(cookies, "smtg_drawLottery", {
                             "costType": 1, "channel": 1})["data"]
        if result["success"]:
            print(result["result"])
        else:
            print(result["bizMsg"])
            return


def pk(cookies):
    print("\n【PK有礼】")  # TODO
    data = getTemplate(cookies, "smtg_getTeamPkDetailInfo", {})[
        "data"]["result"]
    if "result" not in data["data"]:
        print(data["data"])
        return
    data = data["data"]["result"]
    print(f'joinStatus:{data["joinStatus"]}')
    print(f'pkStatus:{data["pkStatus"]}')

    if data["joinStatus"] == 1:
        if "teamId" not in data:
            return

        print(f'已经加入队伍【{data["teamId"]}】')
        print(">>>pk对比\n对方/我方")
        print(
            f'{data["pkUserPkInfo"]["teamCount"]}/{data["currentUserPkInfo"]["teamCount"]}')
        print(f'邀请人数:{data["inviteCount"]}/50')
        print(f'京豆奖励:{data["prizeInfo"]["inviteJdBeanCount"]}')

    if data["pkStatus"] == 2 and data["prizeInfo"]["pkPrizeStatus"] == 2:
        print("开始领取")
        resopnse = getTemplate(cookies, "smtg_receivedPkTeamPrize", {})
        print(resopnse)

    if data["pkStatus"] == 3:
        print("pk暂停")
        
    
    if data["joinStatus"] == 0 and flag_pk == 1:
        try:
            resopnse = requests.get(
            "https://raw.githubusercontent.com/Zero-S1/tmp/main/jd_smPkInfo.json", timeout=2)
            print(resopnse.text)
        except:
            print("无法连接github 跳过")
        tmp=resopnse.json()
        if tmp["pkActivityId"] != data["pkActivityId"]:
            print("还未更新,等待下次运行")
            return
        print("自动加入pk队伍")
        # print(tmp)
        result1 = getTemplate(cookies, "smtg_joinPkTeam", {"teamId": tmp["teamId"],
                                                           "inviteCode": random.choice(tmp["inviteCode"]), "sharePkActivityId": data["pkActivityId"], "channel": "3"})
        print(result1)
    


def manage(cookies):
    print("\n>>>>安排上货(单价最大商品)")
    shelfList = getTemplate(cookies, "smtg_shelfList", {})[
        "data"]["result"]["shelfList"]
    shelfList_unlock = [
        i for i in shelfList if i["groundStatus"] in [1, 2]]  # 可以上架的货架
    for i in shelfList_unlock:
        productList = getTemplate(cookies, "smtg_shelfProductList", {"shelfId": i["shelfId"]})[
            'data']["result"]["productList"]  # 该货架可上架的商品
        _productNow = [i for i in productList if i["groundStatus"] == 2]
        productList = [i for i in productList if i["productType"] == 1]
        list2 = sorted(
            productList, key=lambda productList: productList["previewTotalPriceGold"])
        if len(list2) and _productNow and _productNow[0]["productId"] == list2[-1]["productId"]:
            continue
        ground(cookies, list2[-1]["productId"], i["shelfId"])


def exchangeBean_1(cookies):
    if flag_prize_1 != 1:
        print("[万能的京豆]  自动兑换关闭  flag_prize_1")
        return
    print("\n[万能的京豆] 兑换开启")
    data = getTemplate(cookies, "smtg_queryPrize", {})[
        "data"]
    if data["bizCode"] != 0:
        print(data["bizMsg"])
        return
    prizeList = data["result"]["prizeList"]
    t1 = [i for i in prizeList if i["beanType"] == "Bean"]
    if t1:
        t1 = t1[0]
        if t1["targetNum"] == t1["finishNum"]:
            print("万能的京豆   今日兑换完成")
            return
        for _ in range(t1["targetNum"]):
            data = getTemplate(cookies, "smtg_obtainPrize",
                               {"prizeId": t1["prizeId"]})["data"]
            if data["bizCode"] != 0:
                print(data["bizMsg"])
                return
            time.sleep(1)


def exchangeBean_1000(cookies):
    if flag_prize_1000 != 1:
        print("[京豆大礼包]  自动兑换关闭  flag_prize_1000")
        return
    print("\n[京豆大礼包] 兑换开启")
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
        if t1000["targetNum"] == t1000["finishNum"]:
            print("京豆大礼包   今日兑换完成")
            return
        if t1000["blueCost"] > totalBlue:
            print("蓝币不足")
            return
        data = getTemplate(cookies, "smtg_obtainPrize",
                           {"prizeId": t1000["prizeId"]})["data"]
        if data["bizCode"] != 0:
            print(data["bizMsg"])

def run():
    cookiesList = jdCookie.get_cookies()
    for cookies in cookiesList:
        print(f"""[ {cookies["pt_pin"]} ]""")
        receiveCoin(cookies)
        receiveBlue(cookies)
        shelfList(cookies)
        upgrade(cookies)
        sign(cookies)
        dailyTask(cookies)
        # manage(cookies)
        limitTimePro(cookies)
        pk(cookies)
        lottery(cookies)
        exchangeBean_1000(cookies)
        exchangeBean_1(cookies)
        print("##"*25)
        print("\n\n")

if __name__ == "__main__":
    run()