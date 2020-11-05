import requests
from pyDes import *
import base64
import time
import json
import random
import jdCookie

"""
京奇世界-王牌分拣员
自行抓包、填充 luckHome(cookies) 和 exchange(cookies)中的 data
对应的需要抓取的url  京东app内抓包，不是直接进点击
- https://api.m.jd.com/client.action?functionId=luckHome             # 进入抽奖页面
- https://api.m.jd.com/client.action?functionId=convertAward         # 实际抽奖
"""


def gain_coin(cookies):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1',
        'Host': 'api.m.jd.com',
        'Origin': 'https://jingqih5.m.jd.com',
    }
    body = {
        "ts": int(time.time()*1000),
        "token": get_token(cookies),
        "maxRound": 32,
        "eggRoundCount": 6,
        "roundStars": {"1": 5, "2": 5, "3": 6, "4": 5, "5": 7, "6": random.randint(6, 9), "7": 5, "8": 8, "9": 6, "10": random.randint(4, 6), "11": 6, "12": 16, "13": 6, "14": 7, "15": 6, "16": 4, "17": 9, "18": 6, "19": 8, "20": 6, "21": 9, "22": 10, "23": 6, "24": 6, "25": random.randint(4, 12), "26": 6, "27": 16, "28": 8, "29": 18, "30": 9, "31": 6, "32": 15}
    }
    body = json.dumps(body).replace(" ", "")
    body = ciphertext(body)
    params = (
        ('appid', 'orderCenter'),
        ('functionId', 'picker_submitResult'),
        ('clientVersion', '9.0.0'),
        ('client', 'apple'),
        ('body', body)
    )
    result = requests.post('https://api.m.jd.com/api',
                           headers=headers, params=params, cookies=cookies).json()
    gold = result["data"]["basicGoldCount"]+result["data"]["boxGoldCount"]
    print(f"""京奇世界\n新增金币 [{gold}]""")


def get_token(cookies):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.0;13.5.1',
        'Host': 'api.m.jd.com',
        'Origin': 'https://jingqih5.m.jd.com',
    }

    params = (
        ('appid', 'orderCenter'),
        ('functionId', 'picker_getUserInfo'),
        ('clientVersion', '9.0.0'),
        ('client', 'apple'),
        ('body', '5GlOj7xTF/w='),
    )

    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    return response.json()['data']["token"]


def ciphertext(data):
    k = triple_des("fn0chlrwxspujttbg9feqfat", CBC,
                   b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)

    return bytes.decode(base64.b64encode(k.encrypt(f"""{data}""")))


def luckHome(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'luckHome'),
    )

    data = {
        
    }    ### 此处填充
    if not data:
        print("需要填充 luckHome(cookies) 中的data")
        exit()

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = response.json()
    remainingTimes = result["limit"]["usableCnt"]
    print("remainingTimes: ", remainingTimes)
    return remainingTimes


def exchange(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167237 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'convertAward'),
    )

    data = {
        
    }   ### 此处填充
    if not data:
        print("需要填充 exchange(cookies) 中的data")
        exit()

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    result = response.json()
    print(result["popContent"]["rewardList"][0]["value"])


for cookies in jdCookie.get_cookies():
    print(f"""[ {cookies["pt_pin"]} ]""")
    remainingTimes = luckHome(cookies)
    if remainingTimes == 0:
        print("每日上限10次")
        print(">>>> 跳过游戏")
    for i in range(remainingTimes):
        gain_coin(cookies)
        time.sleep(3)
        exchange(cookies)
        time.sleep(1)
    print("\n\n")
