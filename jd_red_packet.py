import requests
import time
import json
import jdCookie

# 全民开红包   by @changer2222
# cron 5,8 0 * * *


def getTaskIndex(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'taskHomePage'),
    )

    data = {
        "appid": "jd_mp_h5",
        'body': '{}',
        'loginType': 2,
    }

    response = requests.post('https://api.m.jd.com/api', headers=headers,
                             params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    taskList = result["data"]["result"]["taskInfos"]
    for i in taskList:
        # print(i)
        taskId = i["taskType"]
        taskTitle = i["title"]
        taskStatus = i["innerStatus"]
        # print(taskId, taskTitle, taskStatus)
        if taskStatus == 4:
            print("taskId [", taskId, taskTitle, "]     ok")  # 已经领取奖励
        elif taskStatus == 3:
            print("taskId [", taskId, taskTitle, "]     领取红包")  # 任务完成，未领取领取奖励
            getredpacket(cookies, taskId)
        # elif taskId == 0:
        #     print("taskId [", taskId, taskTitle, "]  需要手动执行")   # 单独的接口
            # getCoupon(cookies, taskId)
            # getredpacket(cookies, taskId)
        elif taskStatus != 4 and taskId != 0:  # 执行任务并领取奖励
            print("执行任务", taskId, taskTitle)
            takeTask(cookies, taskId)
            getredpacket(cookies, taskId)
        # print("\n")


def getCoupon(cookies, taskId):  # TODO

    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', 'startTask'),
    )
    data = {
        "appid": "jd_mp_h5",
        'body':  f"""{{"taskType":"{taskId}"}}""",
    }
    response = requests.post('https://api.m.jd.com/api', headers=headers,
                             params=params, cookies=cookies, data=data)
    print(response.text)
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'getCouponConfig'),
    )

    data = {
        "appid": "jd_mp_h5",
        'body':  json.dumps({"pageClickKey": "CouponCenter"})
    }

    response = requests.post('https://api.m.jd.com/client.action', headers=headers,
                             params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    print(result)


def getredpacket(cookies, taskId):
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://happy.m.jd.com',
    }
    params = (
        ('appid', 'jd_mp_h5'),
        ('functionId', 'receiveTaskRedpacket'),
        ('loginType', '2'),
        ('client', 'jd_mp_h5'),
        ('clientVersion', '9.0.6'),
    )

    data = {
        'body': json.dumps({"clientInfo": '{}', "taskType": taskId})
    }

    response = requests.post('https://api.m.jd.com/api', headers=headers,
                             params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    print(result)


def takeTask(cookies, taskId):
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'startTask'),
    )

    data = {
        "appid": "jd_mp_h5",
        'body':  f"""{{"taskType":"{taskId}"}}""",
        'loginType': 2,
    }

    response = requests.post('https://api.m.jd.com/api', headers=headers,
                             params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    print(result)

    params = (
        ('functionId', 'getTaskDetailForColor'),
    )
    response = requests.post('https://api.m.jd.com/api', headers=headers,
                             params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    print(result)
    if "data" not in result:
        print(f'taskId: {taskId} 任务列表为空,手动进入app内检查')
        return
    taskList = result["data"]["result"]["advertDetails"]
    for i in taskList:
        detailId = i["id"]
        detailTitle = i["name"]
        detailStatus = i["status"]
        print(detailId, detailTitle, detailStatus)
        if detailStatus == 2:
            print("taskId [", taskId, detailId, detailTitle, "]  ok")
        if detailStatus != 2:
            print("执行任务", taskId, detailId, detailTitle)
            detailTask(cookies, taskId, detailId)


def detailTask(cookies, taskId, detailId):
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'taskReportForColor'),
    )

    data = {
        "appid": "jd_mp_h5",
        'body':  f"""{{"taskType":"{taskId}","detailId":"{detailId}"}}""",
        'loginType': 2,
    }

    requests.post('https://api.m.jd.com/api', headers=headers,
                  params=params, cookies=cookies, data=data)

def run():
    print("天天红包\n")
    for cookies in jdCookie.get_cookies():
        print(cookies["pt_pin"])
        print("###"*20)
        getTaskIndex(cookies)
        print("\n")
if __name__ == "__main__":
    run()