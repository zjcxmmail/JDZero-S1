import jdCookie
import json
import requests
import time

"""

宠汪汪
1、从jdCookie.py处填写 cookie
2、FEED_NUM :自定义 每次喂养数量; 等级只和喂养次数有关，与数量无关
[x]3、推荐每次投喂10个，积累狗粮，然后去聚宝盆赌每小时的幸运奖，据观察，投入3000-6000中奖概率大，超过7000基本上注定亏本，即使是第一名
3、奖池缩水了，超过5000注定亏本
4、cron 0 */3 * * *  JD_chongWangWang.py  #每隔三小时运行一次，加快升级
"""

FEED_NUM=10   # [10,20,40,80]

def steal(cookies):

    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/415.131;apprpd/MyJD_GameMain;ref/MyJdGameEnterPageController;psq/12;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1453;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=0&lat=0',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ("itemsPerPage", "20"),
        ("currentPage", "1")
    )
    response = requests.get('https://jdjoy.jd.com/pet/getFriends',
                            headers=headers, params=params, cookies=cookies)
    result = json.loads(response.text)
    # print("friends列表：",result,"\n")
    baifangxiaojia = [i["friendPin"] for i in result["datas"]]
    # print(baifangxiaojia)
    for i in baifangxiaojia[-1:]:
        print(i)
        params = (
            ('friendPin', str(i)),
        )

        response = requests.get('https://jdjoy.jd.com/pet/enterFriendRoom',
                                headers=headers, params=params, cookies=cookies)
        result1 = json.loads(response.text)
        # print("enterFriendRoom",result1,"\n")
        if result1["data"]["friendHomeCoin"]:
            # print("捡垃圾laa")
            headers = {
                'Host': 'jdjoy.jd.com',
                'Content-Type': 'application/json',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/443.75;apprpd/MyJD_GameMain;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D0%26lat%3D0;psq/19;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1842;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
                'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=0&lat=0',
                'Accept-Language': 'zh-cn',
                'Accept-Encoding': 'gzip, deflate, br',
            }

            params = (
                ('friendPin', str(i)),
            )

            response = requests.get('https://jdjoy.jd.com/pet/getFriendCoin',
                                    headers=headers, params=params, cookies=cookies)
            print("getFriendCoin ", response.text, "\n")

    ff = [i["friendPin"] for i in result["datas"]
          if i["points"] == 0 and i["stealStatus"] == "can_steal"]
    for i in ff:
        # print(i)
        params = (
            ('friendPin', str(i)),
        )

        response = requests.get('https://jdjoy.jd.com/pet/enterFriendRoom',
                                headers=headers, params=params, cookies=cookies)

        params = (
            ('friendPin', str(i)),
        )

        response = requests.get('https://jdjoy.jd.com/pet/getRandomFood',
                                headers=headers, params=params, cookies=cookies)
        time.sleep(0.5)
    mm = [i["friendPin"] for i in result["datas"]
          if i["points"] == 0 and i["status"] == "not_feed"]
    for i in mm:
        params = (
            ('friendPin', str(i)),
        )

        response = requests.get('https://jdjoy.jd.com/pet/helpFeed',
                                headers=headers, params=params, cookies=cookies)
        print("helpFeed ", response.text)


def getTodayFeedInfo(cookies):
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/197.14;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|558;jdv/0|kong|t_1001226363_|jingfen|c205fb079be245169e93768e786ada79|1585781226992|1585781230;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8439659502069&lat=39.95722551778479',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    response = requests.get(
        'https://jdjoy.jd.com/pet/getTodayFeedInfo', headers=headers, cookies=cookies)
    # print(response.text)
    data = json.loads(response.text)
    print(f"""feedCount: {data["data"]["feedCount"]}""")
    return data["data"]["feedCount"]


def enterRoom(cookies):
    print("\n【喂养状态】")
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/197.14;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|558;jdv/0|kong|t_1001226363_|jingfen|c205fb079be245169e93768e786ada79|1585781226992|1585781230;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8439659502069&lat=39.95722551778479',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ("reqSource", "h5"),
    )

    response = requests.get('https://jdjoy.jd.com/pet/enterRoom',
                            headers=headers, params=params, cookies=cookies)

    data = json.loads(response.text)
    # print(data)
    petFood = data["data"]["petFood"]
    feedCount = data["data"]["feedCount"]
    petLevel = data["data"]["petLevel"]

    print(
        f"""  现有积分: {data["data"]["petCoin"]}
  现有狗粮: {petFood}
  喂养次数: {feedCount}
  宠物等级: {petLevel}
        """
    )


def feed(cookies, feedCount):
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/197.14;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|558;jdv/0|kong|t_1001226363_|jingfen|c205fb079be245169e93768e786ada79|1585781226992|1585781230;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8439659502069&lat=39.95722551778479',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('feedCount', str(feedCount)),
    )
    response = requests.get('https://jdjoy.jd.com/pet/feed',
                            headers=headers, params=params, cookies=cookies)
    data = json.loads(response.text)
    print("【feed】\n ", data["errorCode"])


def getPetTaskConfig(cookies):
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/197.14;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|558;jdv/0|kong|t_1001226363_|jingfen|c205fb079be245169e93768e786ada79|1585781226992|1585781230;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8439659502069&lat=39.95722551778479',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('reqSource', 'h5'),
    )
    response = requests.get('https://jdjoy.jd.com/pet/getPetTaskConfig',
                            headers=headers, params=params, cookies=cookies)
    data = json.loads(response.text)
    datas = data["datas"]

    SignEveryDay = [i for i in datas if i["taskType"]
                    == "SignEveryDay"][0]  # 每日签到 需要跳转小程序
    list_FollowShop = [i for i in datas if i["taskType"]
                       == "FollowShop"][0]  # 关注店铺
    # print(FollowShop)
    list_ThreeMeals = [i for i in datas if i["taskType"]
                       == "ThreeMeals"][0]  # 每日三餐
    _ThreeMeals = list_ThreeMeals["receiveStatus"] == "unreceive"
    list_FollowGood = [i for i in datas if i["taskType"]
                       == "FollowGood"][0]  # 关注商品
    list_ScanMarket = [i for i in datas if i["taskType"]
                       == "ScanMarket"]  # 逛会场  #todo
    _inviteUser = [i for i in datas if i["taskType"] == "InviteUser"][0]
    # unreceive 未领取 ；chance_full 已完成 ；chance_left ；继续
    inviteUserReceiveStatus = _inviteUser["receiveStatus"]

    def isTrue(_list):
        if _list["joinedCount"] == None:
            #print("error")
            # print(_list)
            return True
        else:
            return _list["joinedCount"] < _list["taskChance"]
    if len(list_ScanMarket) == 0:
        _ScanMarket = False
    else:
        ScanMarket = list_ScanMarket[0]
        _ScanMarket = isTrue(ScanMarket)

    list_FollowChannel = [i for i in datas if i["taskType"]
                          == "FollowChannel"][0]  # 浏览频道

    _FollowShop = isTrue(list_FollowShop)
    _FollowGood = isTrue(list_FollowGood)
    # _ScanMarket = isTrue(ScanMarket)
    _FollowChannel = isTrue(list_FollowChannel)
    print("\n【任务列表】")
    if _FollowShop:
        task_FollowShop(cookies)
    else:
        print("-[关注店铺] 达成")
    if _FollowGood:
        task_FollowGood(cookies)
    else:
        print("-[关注商品] 达成")
    if _ScanMarket:
        task_ScanMarket(cookies)
    else:
        print("-[逛逛会场] 达成")
    if _FollowChannel:
        task_FollowChannel(cookies)
    else:
        print("-[关注频道] 达成")
    if _ThreeMeals:
        task_ThreeMeals(cookies)
    else:
        print("-[目前三餐] 达成")


def inviteUser(cookies):
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/200.75;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/29;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|608;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.844947077455&lat=39.95759369826216',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('taskType', 'InviteUser'),
    )
    response = requests.get('https://jdjoy.jd.com/pet/getInviteFood',
                            headers=headers, params=params, cookies=cookies)
    print(response.text)


def task_FollowShop(cookies):
    print("开始执行 [关注店铺]")
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/197.26;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/5;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|574;jdv/0|kong|t_1001226363_|jingfen|c205fb079be245169e93768e786ada79|1585781226992|1585781230;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8449566674551&lat=39.9575858633718',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('reqSource', 'h5'),
    )

    response = requests.get('https://jdjoy.jd.com/pet/getFollowShops',
                            headers=headers, params=params, cookies=cookies)
    data = json.loads(response.text)
    shopIDs = [i["shopId"] for i in data["datas"] if i["status"] == False]
    # exit()
    for shopId in shopIDs:

        headers = {
            'Host': 'jdjoy.jd.com',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/197.14;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|558;jdv/0|kong|t_1001226363_|jingfen|c205fb079be245169e93768e786ada79|1585781226992|1585781230;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8439659502069&lat=39.95722551778479',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        params = (
            ('reqSource', 'h5'),
            ('iconCode', 'follow_shop'),
            ('linkAddr', str(shopId)),
        )

        response = requests.get('https://jdjoy.jd.com/pet/icon/click',
                                headers=headers, params=params, cookies=cookies)
        data = json.loads(response.text)
        # print(data)
        time.sleep(0.5)
        headers = {
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/198.163;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/16;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|587;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jdjoy.jd.com',
            'Origin': 'https://jdjoy.jd.com',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8448457935535&lat=39.95758421830264',
        }

        data = {
            'shopId': str(shopId),
            'reqSource': 'h5'
        }

        response = requests.post('https://jdjoy.jd.com/pet/followShop',
                                 headers=headers, cookies=cookies, data=data)
        print(response.text)


def task_FollowGood(cookies):
    print("开始执行 [关注商品]")
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/198.170;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D116.8450025448939%26lat%3D39.9575563136237;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|590;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8449961073334&lat=39.95755426160679',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('reqSource', 'h5'),
        ('taskType', 'FollowGood'),
    )

    response = requests.get('https://jdjoy.jd.com/pet/getPetTaskConfig',
                            headers=headers, params=params, cookies=cookies)
    data = json.loads(response.text)
    skus = [i["sku"] for i in data["datas"][0]
            ["followGoodList"] if i["status"] == False]
    for sku in skus:
        params = (
            ('reqSource', 'h5'),
            ('iconCode', 'follow_good'),
            ('linkAddr', str(sku)),
        )

        response = requests.get('https://jdjoy.jd.com/pet/icon/click',
                                headers=headers, params=params, cookies=cookies)
        time.sleep(0.5)
        headers = {
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/198.170;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D116.8450025448939%26lat%3D39.9575563136237;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|590;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'jdjoy.jd.com',
            'Origin': 'https://jdjoy.jd.com',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8449961073334&lat=39.95755426160679',
        }

        data = {
            'sku': str(sku),
            'reqSource': 'h5'
        }

        response = requests.post('https://jdjoy.jd.com/pet/followGood',
                                 headers=headers, cookies=cookies, data=data)
        print(response.text)


def task_ScanMarket(cookies):
    print("开始执行 [逛逛会场]")
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/198.170;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D116.8450025448939%26lat%3D39.9575563136237;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|590;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8449961073334&lat=39.95755426160679',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('reqSource', 'h5'),
        ('taskType', 'ScanMarket'),
    )

    response = requests.get('https://jdjoy.jd.com/pet/getPetTaskConfig',
                            headers=headers, params=params, cookies=cookies)
    data = json.loads(response.text)
    marketLists = [i["marketLinkH5"] for i in data["datas"]
                   [0]["scanMarketList"] if i["status"] == False]
    # shopIDs = [i["shopId"] for i in data["datas"] if i["status"] == False]
    # print(marketLists)
    for addr in marketLists:
        # print(addr)
        headers = {
            'Host': 'jdjoy.jd.com',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/198.170;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D116.8450025448939%26lat%3D39.9575563136237;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|590;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8449961073334&lat=39.95755426160679',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        params = (
            ('reqSource', 'h5'),
            ('iconCode', 'scan_market'),
            ('linkAddr', addr),
        )

        response = requests.get('https://jdjoy.jd.com/pet/icon/click',
                                headers=headers, params=params, cookies=cookies)
        # print(response.text)
        time.sleep(0.5)

        headers = {
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/198.170;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D116.8450025448939%26lat%3D39.9575563136237;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|590;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Content-Type': 'application/json',
            'Host': 'jdjoy.jd.com',
            'Origin': 'https://jdjoy.jd.com',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.8449961073334&lat=39.95755426160679',
        }
        data = f"""{{"marketLink":"{str(addr)}","taskType":"ScanMarket","reqSource":"h5"}}"""
        response = requests.post(
            'https://jdjoy.jd.com/pet/scan', headers=headers, cookies=cookies, data=data)
        print(response.text)


def task_FollowChannel(cookies):
    print("开始执行 [关注频道]")
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/200.75;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/29;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|608;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.844947077455&lat=39.95759369826216',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('reqSource', 'h5'),
    )

    response = requests.get('https://jdjoy.jd.com/pet/getFollowChannels',
                            headers=headers, params=params, cookies=cookies)
    data = json.loads(response.text)
    # print(data)
    channelIds = [i["channelId"]
                  for i in data["datas"] if i["status"] == False]
    # print(channelIds)
    for i in channelIds:
        headers = {
            'Host': 'jdjoy.jd.com',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/200.75;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/29;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|608;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.844947077455&lat=39.95759369826216',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        params = (
            ('reqSource', 'h5'),
            ('iconCode', 'follow_channel'),
            ('linkAddr', str(i)),
        )
        response = requests.get('https://jdjoy.jd.com/pet/icon/click',
                                headers=headers, params=params, cookies=cookies)
        # print(response.text)
        time.sleep(0.5)
        headers = {
            'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/200.75;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/29;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|608;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Content-Type': 'application/json',
            'Host': 'jdjoy.jd.com',
            'Origin': 'https://jdjoy.jd.com',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.844947077455&lat=39.95759369826216',
        }

        data = f"""{{"channelId":"{str(i)}","taskType":"FollowChannel","reqSource":"h5"}}"""

        response = requests.post('https://jdjoy.jd.com/pet/scan',
                                 headers=headers, cookies=cookies, data=data)

        print(response.text)


def task_ThreeMeals(cookies):
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/200.75;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/29;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|608;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.844947077455&lat=39.95759369826216',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('taskType', 'ThreeMeals'),
    )
    response = requests.get('https://jdjoy.jd.com/pet/getFood',
                            headers=headers, params=params, cookies=cookies)
    print(response.text)


def get_desk(cookies):

    print("【618限时任务】")
    headers = {
        'Host': 'jdjoy.jd.com',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'jdapp;iPhone;8.5.8;13.4.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167169;supportBestPay/0;jdSupportDarkMode/0;pv/200.75;apprpd/MyJD_Main;ref/MyJdMTAManager;psq/29;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|608;jdv/0|direct|-|none|-|1587263154256|1587263330;adk/;app_device/IOS;pap/JA2015_311210|8.5.8|IOS 13.4.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=116.844947077455&lat=39.95759369826216',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    response = requests.get('https://jdjoy.jd.com/pet/getDeskGoodDetails',
                            headers=headers, cookies=cookies)
    result = json.loads(response.text)
    deskGoods = result["data"]["deskGoods"]
    followCount = result["data"]["followCount"]
    if followCount == None:
        followCount = 0
    tt = [i["sku"] for i in deskGoods if i["status"] == False][:10-followCount]
    if len(tt) == 0:
        print("     达成")

    for i in tt:
        headers = {
            'Host': 'jdjoy.jd.com',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/441.145;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D0%26lat%3D0%23%2Fpages%2FotherPage%2FgoodsCounter;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1797;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=0&lat=0',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        params = (
            ('reqSource', 'h5'),
            ('iconCode', 'follow_good_desk'),
            ('linkAddr', f"{i}"),
        )

        response = requests.get('https://jdjoy.jd.com/pet/icon/click',
                                headers=headers, params=params, cookies=cookies)
        # print(response.text)
        time.sleep(0.5)
        data = f"""{{"taskType":"ScanDeskGood","reqSource":"h5","sku":"{i}"}}"""
        headers = {
            'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167237;supportBestPay/0;jdSupportDarkMode/0;pv/441.145;apprpd/MyJD_Main;ref/https%3A%2F%2Fjdjoy.jd.com%2Fpet%2Findex%3Fun_area%3D5_274_49707_49973%26lng%3D0%26lat%3D0%23%2Fpages%2FotherPage%2FgoodsCounter;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|1797;jdv/0|kong|t_2009624187_|tuiguang|efb0dd46e275438e8ab51051ff404872|1590504165577|1590504173;adk/;app_device/IOS;pap/JA2015_311210|9.0.0|IOS 13.5.1;Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Content-Type': 'application/json',
            'Host': 'jdjoy.jd.com',
            'Origin': 'https://jdjoy.jd.com',
            'Referer': 'https://jdjoy.jd.com/pet/index?un_area=5_274_49707_49973&lng=0&lat=0',
        }

        response = requests.post('https://jdjoy.jd.com/pet/scan',
                                 headers=headers, data=data, cookies=cookies)
        print(response.text)
        # time.sleep(10)
def task_video(cookies):
    print("\n【 激励视频 】")
    headers = {
        'Host': 'draw.jdfcloud.com',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'reqSource': 'weapp',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e22) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxccb5c536b0ecd1bf/605/page-frame.html',
        'Connection': 'keep-alive',
    }
    params = (('reqSource', 'weapp'),)

    response = requests.get('https://draw.jdfcloud.com//pet/getPetTaskConfig',
                            headers=headers, params=params, cookies=cookies)
    petTask = json.loads(response.text)["datas"]
    ViewVideo = [i for i in petTask if i["taskType"]
                 == "ViewVideo"][0]
    joinedCount = ViewVideo["joinedCount"]
    if not joinedCount:
        joinedCount = 0
    if ViewVideo["taskChance"] == joinedCount:
        print(" 今日观看完毕")
        return
    for i in range(ViewVideo["taskChance"]-joinedCount):
        print(f"""观看视频 [{i}]""")
        data = {
            'taskType': "ViewVideo",
            'reqSource': 'weapp'
        }

        response = requests.post('https://draw.jdfcloud.com//pet/scan',
                                 headers=headers, cookies=cookies, data=json.dumps(data))
        print(response.text)
        time.sleep(1)

for cookies in jdCookie.get_cookies():
    print("\n")
    print(f"""[ {cookies["pt_pin"]} ]""")
    getPetTaskConfig(cookies)
    task_video(cookies)
    enterRoom(cookies)   
    #get_desk(cookies) #活动下线
    feed(cookies, FEED_NUM)
    print("--"*25)
