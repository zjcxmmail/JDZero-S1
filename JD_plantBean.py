import requests
import re
import time
import json

'''
1、抓包，登录 https://bean.m.jd.com 点击签到并且出现签到日历后
2、返回抓包，搜索关键词 functionId=signBean 复制Cookie中的pt_key与pt_pin填入以下两个空白处
3、注意，cookies会过期,大约为一个月
4、python3 环境，需要requests包
5、自动运行 cron 5 6-23 * * * python JD_plantBean.py
[x]6、每周一10:00开始，可以*手动*领取上一轮的奖励；约为88个京豆
6、添加 周一自动兑换京豆
'''
cookies1 = {
    'pt_key': '',    # 类似  "AAJeidSDSFg8osfddsVIMLfefwnlTWRjTW58M3sO9DHASBBKltQ"
    'pt_pin': '',    # 类似  "jd_3f45d54g45g4"
}

cookiesList = [cookies1]  # 多账号准备

headers = {
    'Host': 'api.m.jd.com',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': 'jdapp;iPhone;8.5.5;13.4;adk/;app_device/IOS;pap/JA2015_311210|8.5.5|IOS 13.4;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
    'Accept-Language': 'zh-cn',
    'Referer': 'https://bean.m.jd.com/plantBean/index.action?source=wojing',
    'Accept-Encoding': 'gzip, deflate, br',
}


def plantBeanIndex(cookies):
    """
    种豆得豆首页
    """
    params = (
        ('functionId', 'plantBeanIndex'),
        ('body', '{"plantUuid":"7pt22jcko7ljrbpeask7r6avre3h7wlwy7o5jii","monitor_refer":"","wxHeadImgUrl":"","shareUuid":"","followType":"1","monitor_source":"plant_m_plant_index","version":"8.4.0.0"}'),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.5'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585181731771_80279'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    if "data" not in result:
        print("cookie 可能已经过期")
    name = result['data']['plantUserInfo']['plantNickName']
    code = result["code"]
    data = result["data"]
    roundList = data["roundList"][1]  # 本回合
    awardState = data["roundList"][0]["awardState"]   # 5 可以收
    if awardState == '5':
        receive(cookies, data["roundList"][0]['roundId']) # 周一兑换京豆

    growth = roundList['growth']  # 当前成长值
    nutrients = roundList['nutrients']  # 当前营养液
    roundId = roundList['roundId']  # 当前id
    timeNutrientsRes = data["timeNutrientsRes"]  # 水车换营养液
    awardList = data["awardList"]  # 每日任务列表
    accessFlag = data["accessFlag"]  # 未知
    roundAccessFag = data['roundAccessFag']  # 未知
    timeNutrsCalenFlag = data["timeNutrsCalenFlag"]  # 未知
    return roundId, name, (growth, nutrients), timeNutrientsRes, awardList, (accessFlag, roundAccessFag, timeNutrsCalenFlag)


def _jsonp2dict(jsonp):
    _dict = re.findall(r"jsonp\w+\((.*)\)", jsonp)[0]
    return json.loads(_dict)

def receive(cookie, roundId):
    params = (
        ('functionId', 'receivedBean'),
        ('body', f"""{{"roundId":"{roundId}","monitor_source":"plant_m_plant_index","monitor_refer":"plant_index","version":"8.4.0.0"}}"""),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.10'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4.1'),
        ('uuid', '9b812b59e055cd226fd60ebb5fd0981c4d0d235d'),
        ('jsonp', 'jsonp_1588557832190_37229'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    print(response.text)
    
def waterwheel(timeNutrientsRes, roundId, cookies):
    """
    水车 换取营养液 游戏
    6:00-21:00每小时生产一瓶，超过三个小时自动停止
    领取后方可继续生产
    """
    t = timeNutrientsRes
    try:
        nutrCount = t["nutrCount"]  # 如果不为0，就领取
        print(f"目前水车上的营养液数:{nutrCount}")
        if nutrCount != '0':
            print("收取营养液ing")
            _get_nutrient_from_waterwheel(cookies, roundId)
    except:
        print("暂时不能领取")


def _awardList(awardList):
    """
    每天任务列表
    """
    daily_signin1 = awardList[0]["limitFlag"]
    shop_2_1 = awardList[1]["childAwardList"][0]["limitFlag"]
    product_2_2 = awardList[1]["childAwardList"][1]["limitFlag"]
    channel_2_3 = awardList[1]["childAwardList"][2]["limitFlag"]
    mall_4 = awardList[3]["limitFlag"]
    double_5_1 = awardList[4]["childAwardList"][0]["limitFlag"]
    return (daily_signin1, shop_2_1, product_2_2, channel_2_3, mall_4, double_5_1)


def use_nutrient(cookies, roundId):
    """
    使用营养液换取成长值
    """
    params = (
        ('functionId', 'cultureBean'),
        ('body', f"""{{"roundId":"{roundId}","monitor_source":"plant_m_plant_index","monitor_refer":"plant_index","version":"8.4.0.0"}}"""),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.6'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585191072780_34553'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    print("浇水ing")

    print(result)


def _get_nutrient_from_waterwheel(cookies, roundId):
    """
    从水车领取营养液
    """
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'jdapp;iPhone;8.5.6;13.4;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167151;supportBestPay/0;jdSupportDarkMode/0;pv/117.5;apprpd/MyJD_Main;ref/https%3A%2F%2Fbean.m.jd.com%2FplantBean%2Findex.action%3Fsource%3Dwojing%26lng%3D116.845191%26lat%3D39.957801%26sid%3Dea687233c5e7d226b30940ed7382c5cw%26un_area%3D5_274_49707_49973;psq/0;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|334;jdv/0|androidapp|t_335139774|appshare|Wxfriends|1585284828744|1585284833;adk/;app_device/IOS;pap/JA2015_311210|8.5.6|IOS 13.4;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://bean.m.jd.com/plantBean/index.action?source=wojing',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('functionId', 'receiveNutrients'),
        ('body', f"""{{"roundId":"{roundId}","monitor_source":"plant_m_plant_index","monitor_refer":"plant_receiveNutrients","version":"8.4.0.0"}}"""),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.6'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585192356255_16292'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    print(result)


def _productTaskList(cookies):
    """
    关注任务-浏览商品
    limit=6
    """  # limit=6
    params = (
        ('functionId', 'productTaskList'),
        ('body', '{"monitor_source":"plant_m_plant_index","monitor_refer":"plant_productTaskList","version":"8.4.0.0"}'),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.5'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585199203575_48826'),
    )
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'jdapp;iPhone;8.5.5;13.4;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167121;supportBestPay/0;jdSupportDarkMode/0;pv/103.2;apprpd/MyJD_Main;ref/https%3A%2F%2Fbean.m.jd.com%2FplantBean%2Findex.action%3Fsource%3Dwojing%26un_area%3D5_274_49707_49973%26lng%3D116.8438383685941%26lat%3D39.95744163210918;psq/3;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|219;jdv/0|direct|-|none|-|1583449735697|1583796810;adk/;app_device/IOS;pap/JA2015_311210|8.5.5|IOS 13.4;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://bean.m.jd.com/plantBean/index.action?source=wojing',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    productInfoList = result["data"]["productInfoList"]
    lists = sum(productInfoList, [])
    lists = list(filter(lambda i: i["taskState"] == "2", lists))
    limit = 6

    for i in lists:
        time.sleep(0.4)
        productTaskId = i['productTaskId']
        skuId = i["skuId"]
        taskState = i["taskState"]
        body = f"""{{"productTaskId":"{productTaskId}","skuId":"{skuId}","monitor_source":"plant_m_plant_index","monitor_refer":"plant_productNutrientsTask","version":"8.4.0.0"}}"""
        params = (
            ('functionId', 'productNutrientsTask'),
            ('body', body),
            ('appid', 'ld'),
            ('client', 'apple'),
            ('clientVersion', '8.5.5'),
            ('networkType', 'wifi'),
            ('osVersion', '13.4'),
            ('jsonp', 'jsonp_1585199207082_64917'),
        )
        headers = {
            'Host': 'api.m.jd.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': 'jdapp;iPhone;8.5.5;13.4;;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167121;supportBestPay/0;jdSupportDarkMode/0;pv/105.24;apprpd/MyJD_Main;ref/https%3A%2F%2Fbean.m.jd.com%2FplantBean%2Findex.action%3Fsource%3Dwojing%26lng%3D116.845010%26lat%3D39.957812%26sid%3Dea687233c5e7d226b30940ed7382c5cw%26un_area%3D5_274_49707_49973;psq/2;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|236;jdv/0|direct|-|none|-|1583449735697|1583796810;adk/;app_device/IOS;pap/JA2015_311210|8.5.5|IOS 13.4;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Accept-Language': 'zh-cn',
            'Referer': 'https://bean.m.jd.com/AttentionProduct',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        response = requests.get('https://api.m.jd.com/client.action',
                                headers=headers, params=params, cookies=cookies)
        result = _jsonp2dict(response.text)
        time.sleep(1)
        if "data" in result:
            if result["data"]["nutrState"] == '1':
                limit -= 1
                print(result)
        if limit == 0:
            break


def _shopTaskList(cookies):
    """
    关注任务-浏览店铺
    # limit=4
    """
    params = (
        ('functionId', 'shopTaskList'),
        ('body', '{"monitor_source":"plant_m_plant_index","monitor_refer":"plant_shopList","version":"8.4.0.0"}'),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.5'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585206113100_24906'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)

    result = _jsonp2dict(response.text)
    time.sleep(1)
    data = result["data"]
    goodShopList = data["goodShopList"]
    moreShopList = data["moreShopList"]
    shopList = goodShopList + moreShopList
    limit = 4
    for i in shopList:
        time.sleep(0.4)
        shopTaskId = i["shopTaskId"]
        shopId = i["shopId"]
        body = f"""{{"shopTaskId":"{shopTaskId}","shopId":"{shopId}","monitor_source":"plant_m_plant_index","monitor_refer":"plant_shopNutrientsTask","version":"8.4.0.0"}}"""

        params = (
            ('functionId', 'shopNutrientsTask'),
            ('body', body),
            ('appid', 'ld'),
            ('client', 'apple'),
            ('clientVersion', '8.5.5'),
            ('networkType', 'wifi'),
            ('osVersion', '13.4'),
            ('jsonp', 'jsonp_1585206964789_33053'),
        )

        response = requests.get('https://api.m.jd.com/client.action',
                                headers=headers, params=params, cookies=cookies)
        result = _jsonp2dict(response.text)
        if "data" in result:
            if result["data"]["nutrState"] == '1':
                limit -= 1
                print(result)
        if limit == 0:
            break


def _double_signin(cookies):
    """
    receiveNutrientsTask
    金融双签
    """
    params = (
        ('functionId', 'receiveNutrientsTask'),
        ('body', '{"awardType":"7","monitor_source":"plant_m_plant_index","monitor_refer":"plant_receiveNutrientsTask","version":"8.4.0.0"}'),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.6'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585269770133_17771'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = response.text
    print(result)


def _plantChannelTaskList(cookies):
    # 直接返回json，非jsonp
    params = (
        ('functionId', 'plantChannelTaskList'),
        ('body', '{}'),
        ('appid', 'ld'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = json(response.text)

    data = result["data"]
    channelList = data["goodChannelList"] + data["normalChannelList"]
    limit = 3
    for i in channelList:
        time.sleep(1)
        channelTaskId = i["channelTaskId"]
        channelId = i["channelId"]
        body = f"""{{"channelTaskId":"{channelTaskId}","channelId":"{channelId}"}}"""
        params = (
            ('functionId', 'plantChannelNutrientsTask'),
            ('body', body),
            ('appid', 'ld'),
        )
        response = requests.get('https://api.m.jd.com/client.action',
                                headers=headers, params=params, cookies=cookies)
        result = json(response.text)
        nutrNum = result["data"]["nutrNum"]
        limit -= nutrNum
        print(result)
        if limit == 0:
            break


def _purchaseRewardTask(cookies, roundId):
    """
    逛逛会场
    """
    params = (
        ('functionId', 'purchaseRewardTask'),
        ('body', f"""{{"roundId":"{roundId}","monitor_source":"plant_m_plant_index","monitor_refer":"plant_purchaseRewardTask","version":"8.4.0.0"}}"""),
        ('appid', 'ld'),
        ('client', 'apple'),
        ('clientVersion', '8.5.5'),
        ('networkType', 'wifi'),
        ('osVersion', '13.4'),
        ('jsonp', 'jsonp_1585269759756_14899'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    result = response.text
    print(result)


print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

for cookies in cookiesList:
    roundId, name, (growth, nutrients), timeNutrientsRes, awardList, flags = plantBeanIndex(
        cookies)

    print(f"  [ {name} ]")
    print(f"成长值:{growth},营养液:{nutrients}")

    daily_signin1, shop_2_1, product_2_2, channel_2_3, mall_4, double_5_1 = _awardList(
        awardList)
    print("每日任务检查")
    print("--"*10)

    if daily_signin1 == "2":
        print("[每日签到]   达成")

    else:
        # print("执行 [每日签到]") # todo
        pass
    if shop_2_1 == "2":
        print("[浏览店铺]   达成")
    else:
        print("执行 [浏览店铺]")
        _shopTaskList(cookies)

    if product_2_2 == "2":
        print("[挑选商品]   达成")
    else:
        print("执行 [挑选商品]")
        _productTaskList(cookies)

    if channel_2_3 == "2":
        print("[关注频道]   达成")
    else:
        print("执行 [关注频道]")
        _plantChannelTaskList(cookies)

    if mall_4 == "2":
        print("[逛逛会场]   达成")
    else:
        print("执行 [逛逛会场]")
        _purchaseRewardTask(cookies, roundId)

    if double_5_1 == "2":
        print("[金融双签]   达成")
    else:
        print("执行 [金融双签]")
        _double_signin(cookies)
    print("--"*10)

    waterwheel(timeNutrientsRes, roundId, cookies)  # 水车收营养液

    roundId, _, (_, nutrients), _, _, _ = plantBeanIndex(cookies)
    if nutrients != "0":
        use_nutrient(cookies, roundId)         # 营养液换成长值
    else:
        print("跳过浇水")
    print("*"*8+"检查完毕"+"*"*8)
    print("\n")
