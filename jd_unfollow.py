import jdCookie
import json
import requests
import time
import re

"""
jd取消关注店铺、商品  参考自 @uniqueque (https://github.com/uniqueque/QuantumultX/blob/master/Script/jd_unfollow.js)
当关注达到上限时，某些活动会提示火爆


"""
NUM = 50  # 执行一次，取消关注的数量
unfollowdShopsFlag = 1  # 取关店铺,停用置为0
unfollowdGoodsFlag = 1  # 取关商品,停用置为0


def unfollowdShops(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Referer': 'https://wqs.jd.com/my/fav/shop_fav.shtml'
    }
    params1 = (
        ('cp', 1),
        ('pageSize', NUM),
        ('sceneval', 2),
        ('callback', 'jsonp')
    )
    response = requests.get('https://wq.jd.com/fav/shop/QueryShopFavList',
                            headers=headers, params=params1, cookies=cookies)
    followShop = jsonp2json(response.text)
    totalNum1 = followShop["totalNum"]
    # print(totalNum1)
    if totalNum1 == "0":
        print(f"""店铺关注 0 --> 0""")
        return
    shopIds = [i["shopId"] for i in followShop["data"]]
    shopIds = ','.join(shopIds)
    params2 = (
        ('shopId', shopIds),
        ('sceneval', 2),
        ('callback', 'jsonp')
    )
    response = requests.get('https://wq.jd.com/fav/shop/batchunfollow',
                            headers=headers, params=params2, cookies=cookies)
    time.sleep(1)
    response = requests.get('https://wq.jd.com/fav/shop/QueryShopFavList',
                            headers=headers, params=params1, cookies=cookies)
    followShop = jsonp2json(response.text)
    totalNum2 = followShop["totalNum"]
    print(f"""店铺关注 {totalNum1} --> {totalNum2}""")


def unfollowdGoods(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Referer': 'https://wqs.jd.com/my/fav/goods_fav.shtml'
    }
    params1 = (
        ('cp', 1),
        ('pageSize', NUM),
        ('sceneval', 2),
        ('callback', 'jsonp')
    )
    response = requests.get('https://wq.jd.com/fav/comm/FavCommQueryFilter',
                            headers=headers, params=params1, cookies=cookies)
    followGood = jsonp2json(response.text)
    totalNum1 = followGood["totalNum"]
    if totalNum1 == "0":
        print(f"""商品关注 0 --> 0""")
        return
    commIds = [i["commId"] for i in followGood["data"]]
    commIds = ','.join(commIds)
    params2 = (
        ('commId', commIds),
        ('sceneval', 2),
        ('callback', 'jsonp')
    )
    response = requests.get('https://wq.jd.com/fav/comm/FavCommBatchDel',
                            headers=headers, params=params2, cookies=cookies)
    time.sleep(1)
    response = requests.get('https://wq.jd.com/fav/comm/FavCommQueryFilter',
                            headers=headers, params=params1, cookies=cookies)
    followGood = jsonp2json(response.text)
    totalNum2 = followGood["totalNum"]
    print(f"""商品关注 {totalNum1} --> {totalNum2}""")


def jsonp2json(jsonp):
    _dict = re.findall(r"try{jsonp\(([\s\S]*)\);}catch\(e\){}", jsonp)[0]
    return json.loads(_dict)

def run():
    print("尽量不要一次性全部取消，以免被风控")
    for cookies in jdCookie.get_cookies():
        print("\n")
        print(f"""[ {cookies["pt_pin"]} ]""")
        if unfollowdShopsFlag == 1:
            unfollowdShops(cookies)
        if unfollowdGoodsFlag == 1:
            unfollowdGoods(cookies)
        print("##"*25)
if __name__ == "__main__":
    run()