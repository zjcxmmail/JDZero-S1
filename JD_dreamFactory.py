import jdCookie
import json
import requests
import time


"""
京喜工厂（弃坑）
1、从jdCookie.py处填写 cookie
2、需要进入小游戏中手动选择物品
[x]2、sharePin 为自己的助力码，但是需要别人为自己助力
[x]3、欢迎留下sharePin互助

目前功能:
收取发电机、投入电力    cron 0 * * * * JD_dreamFactory.py  
领电力-每日计划 (部分)
领电力-生产成就 
[x]助力他人,目前无法实现

"""


sharePins = ["G2WdboiKq_xHaIrDNf72pg==",]

headers = {
    'Host': 'wq.jd.com',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': 'jdapp;iPhone;9.0.4;13.5.1;;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
    'Accept-Language': 'zh-cn',
    'Referer': 'https://wqsd.jd.com/pingou/dream_factory/index.html',
    'Accept-Encoding': 'gzip, deflate, br',
}


def userInfo(cookies):
    params = (
        ('zone', 'dream_factory'),
        ('pin', ''),
        ('sharePin', ''),
        ('shareType', ''),
        ('materialTuanPin', ''),
        ('materialTuanId', ''),
        ('sceneval', '2'),
    )

    response = requests.get('https://wq.jd.com/dreamfactory/userinfo/GetUserInfo',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def taskList(cookies):
    params = (
        ('source', 'dreamfactory'),
        ('bizCode', 'dream_factory'),
        ('sceneval', '2'),
        ('g_login_type', '1'),
    )

    response = requests.get('https://wq.jd.com/newtasksys/newtasksys_front/GetUserTaskStatusList',
                            headers=headers, params=params, cookies=cookies)
    return response.json()["data"]["userTaskStatusList"]


def help(cookies, assistCondition, encryptPin):
    for sharePin in sharePins:
        if sharePin == encryptPin:
            continue
        params = (
            ('zone', 'dream_factory'),
            ('pin', ''),
            ('sharePin', sharePin),
            ('shareType', '2'),
            ('materialTuanPin', ''),
            ('materialTuanId', ''),
            ('sceneval', '2'),
        )

        response = requests.get('https://wq.jd.com/dreamfactory/userinfo/GetUserInfo',
                                headers=headers, params=params, cookies=cookies)
        time.sleep(0.4)
        assistCondition = response.json()["data"]["assistCondition"]
        assistConditionMsg = assistCondition["assistConditionMsg"]
        print(assistConditionMsg)
        if "您今日帮助TA的机会已用完，请明天再来~" == assistConditionMsg:
            # print("跳过")
            return
        if not assistConditionMsg:
            print("开始助力")
            params = (
                ('zone', 'dream_factory'),
                ('sharepin', sharePin),
            )

            response = requests.get('https://jxa.jd.com/wq.jd.com/dreamfactory/friend/AssistFriend',
                                    headers=headers, params=params, cookies=cookies)
            print(response.text)
    # return response.json()


def collect(cookies, factoryid, productionId):
    params = (
        ('zone', 'dream_factory'),
        ('apptoken', ''),
        ('pgtimestamp', ''),
        ('phoneID', ''),
        ('factoryid', str(factoryid)),
        ('doubleflag', '1'),
        ('sceneval', '2'),
    )

    response = requests.get('https://wq.jd.com/dreamfactory/generator/CollectCurrentElectricity',
                            headers=headers, params=params, cookies=cookies)
    print("[收取发电机]\n", response.text)
    params = (
        ('zone', 'dream_factory'),
        ('productionId', str(productionId)),
        ('sceneval', '2'),
        ('g_login_type', '1'),
    )
    response = requests.get('https://wq.jd.com/dreamfactory/userinfo/InvestElectric',
                            headers=headers, params=params, cookies=cookies)
    print("[投入电力]\n", response.text)


def getAward(cookies, taskId):
    params = (
        ('source', 'dreamfactory'),
        ('bizCode', 'dream_factory'),
        ('taskId', str(taskId)),
        ('sceneval', '2'),
        ('g_login_type', '1'),
    )
    response = requests.get('https://wq.jd.com/newtasksys/newtasksys_front/Award',
                            headers=headers, params=params, cookies=cookies)
    print("getAward\n", response.text)


def doTask(cookies, taskId):
    params = (
        ('source', 'dreamfactory'),
        ('bizCode', 'dream_factory'),
        ('taskId', str(taskId)),
        ('sceneval', '2'),
        ('g_login_type', '1'),
    )
    response = requests.get('https://wq.jd.com/newtasksys/newtasksys_front/DoTask',
                            headers=headers, params=params, cookies=cookies)
    print("doTask\n", response.text)


def doTask_5(cookies):
    params = (
        ('bizCode', 'dream_factory'),
        ('taskId', '16'),
        ('source', 'dreamfactory'),
        ('sceneval', '2'),
        ('g_login_type', '1'),
    )

    response = requests.get('https://wq.jd.com/newtasksys/newtasksys_front/GetUserTaskStatusList',
                            headers=headers, params=params, cookies=cookies)
    result = response.json()["data"]["userTaskStatusList"][0]
    # print(result)
    if result["targetTimes"] == result["completedTimes"]:
        getAward(cookies, '16')
        return
    params = (
        ('func', 'pinlike'),
        ('recpos', '5914'),
        ('param', '{"pagenum":1,"count":20}'),
        ('sceneval', '2'),
        ('g_login_type', '1'),
    )

    response = requests.get('https://wq.jd.com/mcoss/data/get',
                            headers=headers, params=params, cookies=cookies)
    feeds = response.json()["data"]["feeds"]
    for _ in range(5):
        params = (
            ('bizCode', 'dream_factory'),
            ('taskId', '16'),
            ('configExtra', json.dumps(
                {"hasBrowseSkuIds": f""",{feeds[0]["id"]},{feeds[1]["id"]},{feeds[2]["id"]},{feeds[3]["id"]},{feeds[4]["id"]}"""})),
            ('source', 'dreamfactory'),
            ('sceneval', '2'),
            ('g_login_type', '1'),
        )

        response = requests.get('https://wq.jd.com/newtasksys/newtasksys_front/DoTask',
                                headers=headers, params=params, cookies=cookies)
        time.sleep(0.5)
    # print(response.text)
    getAward(cookies, '16')


def box(cookies, taskId):
    status = 0
    i = 0
    while status == 0:
        params = (
            ('zone', 'dream_factory'),
            ('taskid', str(taskId)),
            ('counts', str(i)),
            ('source', 'dreamfactory'),
            ('sceneval', '2'),
            ('g_login_type', '1'),
        )
        response = requests.get('https://wq.jd.com/dreamfactory/generator/GetBoxInfo',
                                headers=headers, params=params, cookies=cookies)
        print(response.text)
        status = response.json()["data"]["status"]
        print(status)
        i += 1


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    factoryInfo = userInfo(cookies)
    # print(factoryInfo)
    factoryId = factoryInfo["data"]["factoryList"][0]["factoryId"]
    production = factoryInfo["data"]["productionList"][0]
    productionId = production["productionId"]
    encryptPin = factoryInfo["data"]["user"]["encryptPin"]
    assistCondition = factoryInfo["data"]["assistCondition"]
    # print(f"""\n我的sharePin: {encryptPin}\n""")
    print(
        f"""生产进度: {int(production["investedElectric"]/production["needElectric"]*10000)/100}%""")
    collect(cookies, factoryId, productionId)
    # help(cookies, assistCondition, encryptPin)
    userTaskStatusList = taskList(cookies)
    achievementsTask = [
        i for i in userTaskStatusList if i["dateType"] == 1]  # 生产成就
    dailyTask = [i for i in userTaskStatusList if i["dateType"] == 2]  # 每日计划

    print("\n   【生产成就(未完成)】")
    for i in achievementsTask:
        if i["awardStatus"] == 1:  # 已经领取，跳过
            continue
        print(i["taskName"],
              f"""        {i["completedTimes"]}/{i["targetTimes"]}""")
        if i["completedTimes"] >= i["targetTimes"]:
            getAward(cookies, i["taskId"])

    print("\n\n   【每日计划(未完成)】")
    for i in dailyTask:
        if i["awardStatus"] == 1:  # 已经领取，跳过
            continue
        print(i["taskName"],
              f"""        {i["completedTimes"]}/{i["targetTimes"]}""")
        if i["taskType"] == 2 or i["taskType"] == 3:  # 看广告+给工厂打广告  dotask 和getAward
            print(i)
            doTask(cookies, i["taskId"])
            time.sleep(0.5)
            getAward(cookies, i["taskId"])
        if i["taskType"] == 6:  # 集市浏览5  getAward
            print(i)
            doTask_5(cookies)
        if i["taskType"] == 1:
            if i["taskId"] == 3:  # 每日开工打卡
                getAward(cookies, i["taskId"])
            if i["taskId"] == 86:  # 登录APP领取奖励   #TODO
                pass
        if i["taskType"] == 9:  # 开宝箱相关
            if i["completedTimes"] == i["targetTimes"]:
                getAward(cookies, i["taskId"])
                continue
            box(cookies, i["taskId"])
            getAward(cookies, i["taskId"])
        if i["taskType"] in [4, 5, 10]:   # 累计  getAward
            if i["completedTimes"] >= i["targetTimes"]:
                getAward(cookies, i["taskId"])
    # exit()

    print("\n")
    print("##"*30)
