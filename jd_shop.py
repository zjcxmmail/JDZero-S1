import requests
import json
import jdCookie

# 领京豆--进店领豆 
# 每天运行一次  2或4京豆 聊胜于无
# cron 5,8 0 * * *

def getTaskIndex(cookies):
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'queryTaskIndex'),
    )

    data = {
        'body': '{}',
        "appid": "ld"
    }

    response = requests.post('https://api.m.jd.com/client.action', headers=headers,
                             params=params, cookies=cookies, data=data)
    result = json.loads(response.text)
    if "taskList" not in result["data"] or not result["data"]["taskList"]:
        print("...来晚了")
        return
    taskList = result["data"]["taskList"]
    for i in taskList:
        taskId = i["taskId"]
        taskStatus = i["taskStatus"]
        if taskStatus == 3:
            print("taskId [", taskId, "]  ok")
        if taskStatus != 3:
            print("执行任务")
            takeTask(cookies, taskId)


def takeTask(cookies, taskId):
    headers = {
        'User-Agent': 'JD4iPhone/167169 (iPhone; iOS 13.4.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('functionId', 'takeTask'),
    )

    data = {
        'body': f"""{{"taskId":"{taskId}"}}""",
        "appid": "ld"
    }

    response = requests.post('https://api.m.jd.com/client.action',
                             headers=headers, params=params, cookies=cookies, data=data)
    print(response.text)

def run():
    print("进店领豆  每天运行一次  2或4京豆\n")
    for cookies in jdCookie.get_cookies():
        print(cookies["pt_pin"])
        getTaskIndex(cookies)
        print("\n")

if __name__ == "__main__":
    run()