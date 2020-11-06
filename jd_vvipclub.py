import requests
import json
import jdCookie
import time

"""
入口: app首页 "领京东" ——  "摇京豆"
cron 5,8 0 * * *
"""

def template(cookies, functionId, body):
    headers = {
        'User-Agent': 'jdapp;iPhone;9.0.2;13.5.1',
        'Host': 'api.m.jd.com',
        'Referer': 'https://vip.m.jd.com/newPage/reward/123dd/slideContent?page=focus',
    }

    params = (
        ('appid', 'vip_h5'),
        ('functionId', functionId),
        ('body', json.dumps(body)),
        ('_', str(int(time.time()*1000))),
    )

    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    return response.json()


def shake(cookies):
    result = template(cookies, "vvipclub_luckyBox", {
        "info": "freeTimes"})
    return result["data"]["freeTimes"]

def run():
    for cookies in jdCookie.get_cookies():
        print(cookies["pt_pin"])
        browseTask = template(cookies, "vvipclub_lotteryTask", {
            "info": "browseTask", "withItem": True})["data"][0]
        time.sleep(1)
        attentionTask = template(cookies, "vvipclub_lotteryTask", {
            "info": "attentionTask", "withItem": True})["data"][0]
        m = browseTask["totalPrizeTimes"]-browseTask["currentFinishTimes"]
        print("browseTask: ",m)
        if m > 0:
            _ids = [i["id"] for i in browseTask["taskItems"] if not i["finish"]]
            for i in range(m):
                print(template(cookies, "vvipclub_doTask", {
                    "taskName": "browseTask", "taskItemId": _ids.pop()}))
                time.sleep(1)

        n = attentionTask["totalPrizeTimes"]-attentionTask["currentFinishTimes"]
        time.sleep(1)
        print("attentionTask: ",n)
        if n > 0:
            _ids = [i["id"] for i in attentionTask["taskItems"] if not i["finish"]]
            for i in range(n):
                print(template(cookies, "vvipclub_doTask", {
                    "taskName": "attentionTask", "taskItemId": str(_ids.pop())}))
                time.sleep(2)
        freeTimes = shake(cookies)
        print("freeTimes",freeTimes)
        for i in range(freeTimes):
            print(template(cookies, "vvipclub_shaking", {
                "type": "0"}))
            time.sleep(1)
        time.sleep(1)
        print("\n\n")
        print("##"*30)

if __name__ == "__main__":
    run()