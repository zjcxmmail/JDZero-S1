import requests
import re
import json
import time
import jdCookie

"""
1、自动运行 cron 5 * * * * python jd_speed.py
2、每天4个京豆，聊胜于无
"""



cookiesList =jdCookie.get_cookies()  # 多账号准备

headers = {
    'Host': 'api.m.jd.com',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': 'jdapp;iPhone;8.5.5;13.4;9b812b59e055cd226fd60ebb5fd0981c4d0d235d;network/wifi;supportApplePay/3;hasUPPay/0;pushNoticeIsOpen/0;model/iPhone9,2;addressid/138109592;hasOCPay/0;appBuild/167121;supportBestPay/0;jdSupportDarkMode/0;pv/104.43;apprpd/MyJD_GameMain;ref/MyJdGameEnterPageController;psq/9;ads/;psn/9b812b59e055cd226fd60ebb5fd0981c4d0d235d|272;jdv/0|direct|-|none|-|1583449735697|1583796810;adk/;app_device/IOS;pap/JA2015_311210|8.5.5|IOS 13.4;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
    'Accept-Language': 'zh-cn',
    'Referer': 'https://h5.m.jd.com/babelDiy/Zeus/6yCQo2eDJPbyPXrC3eMCtMWZ9ey/index.html?lng=116.845095&lat=39.957701&sid=ea687233c5e7d226b30940ed7382c5cw&un_area=5_274_49707_49973',
    'Accept-Encoding': 'gzip, deflate, br',
}


def _jsonp2dict(jsonp):
    _dict = re.findall("\((.*)\)", jsonp)[0]
    return dict(json.loads(_dict))


def flyTask_start(cookies, source_id):
    body = f"""{{"source":"game","source_id":"{source_id}"}}"""
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'flyTask_start'),
        ('body', body),
        ('jsonp', '__jsonp1585234167916'),
        ('_', str(int(time.time())*1000)),
    )

    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)

    result = _jsonp2dict(response.text)
    print(result)


def flyTask_state(cookies):
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'flyTask_state'),
        ('body', '{"source":"game"}'),
        ('jsonp', '__jsonp1585235064779'),
        ('_', '1585235066058'),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    data = result["data"]

    if "beans_num" not in data:
        # "脚本失效", "js_speed Cookie过期")
        exit()
    beans_num = data["beans_num"]
    distance = data["distance"]
    destination = data["destination"]
    done_distance = data["done_distance"]
    source_id = data["source_id"]  # 根据source_id 启动flyTask_start()
    task_status = data["task_status"]   # 0,没开始；1，已开始
    return task_status, source_id, done_distance, destination  # 检查某个参数，再启动——start


def _spaceEvent_handleEvent(cookies, eventId, option):
    body = f"""{{"source":"game","eventId":"{eventId}","option":"{option}"}}"""
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'spaceEvent_handleEvent'),
        ('body', body),
        ('t', str(int(time.time())*1000)),
        ('jsonp', '__jsonp1585274197091'),
        ('_', str(int(time.time())*1000)),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)

    result = _jsonp2dict(response.text)
    print(result)


def spaceEvent_list(cookies):
    print("检查特殊事件ing")
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'spaceEvent_list'),
        ('body', '{"source":"game"}'),
        ('jsonp', '__jsonp1585274197090'),
        ('_', str(int(time.time())*1000)),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)["data"]
    events = []
    for i in result:
        if i["status"] == 1:
            for j in i["options"]:
                if j["type"] == 1:
                    events.append([i["id"], j["value"]])
    return events


def energeProp_list(cookies):
    print("检查可领取燃料列表ing")
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'energyProp_list'),
        ('body', '{"source":"game"}'),
        ('jsonp', '__jsonp1585236158778'),
        ('_', str(int(time.time())*1000)),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)["data"]
    new = []

    for i in result:
        _time = i["thaw_time"]

        if _time == 0:
            new.append(i["id"])
    return new


def energeProp_usaleList(cookies):
    print("检查暂存的燃料ing")
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'energyProp_usalbeList'),
        ('body', '{"source":"game"}'),
        ('jsonp', '__jsonp1585237174341'),
        ('_', str(int(time.time())*1000)),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)["data"]
    if len(result) == 0:
        return None
    else:
        return [i['id'] for i in result]


def _energyProp_gain(cookies, energy_id,):
    print("领取燃料")

    body = f"""{{"source":"game","energy_id":{energy_id}}}"""
    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'energyProp_gain'),
        ('body', body),
        ('jsonp', '__jsonp1585236158787'),
        ('_', str(int(time.time())*1000)),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    print(result)


def _energyProp_use(cookies, energy_id):
    print("使用燃料")

    params = (
        ('appid', 'memberTaskCenter'),
        ('functionId', 'energyProp_use'),
        ('body', f"""{{"source":"game","energy_id":"{energy_id}"}}"""),
        ('jsonp', '__jsonp1585237174342'),
        ('_', str(int(time.time())*1000)),
    )
    response = requests.get('https://api.m.jd.com/',
                            headers=headers, params=params, cookies=cookies)
    result = _jsonp2dict(response.text)
    print(result)

def run():
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for cookies in cookiesList:
        task_status, source_id, done_distance, destination = flyTask_state(cookies)
        if task_status == 0:
            print(f"开启新任务:{destination}")
            flyTask_start(cookies, source_id)
        else:
            print(f"任务进行中:{destination}")

        able_energeProp_list = energeProp_list(cookies)
        if len(able_energeProp_list) != 0:
            print("领取燃料ing")
            for i in able_energeProp_list:
                _energyProp_gain(cookies,  i)

        else:
            print("     没有可领取的燃料")

        spaceEvents = spaceEvent_list(cookies)  # 检查特殊事件
        if len(spaceEvents) != 0:
            print("处理特殊事件ing")
            for i in spaceEvents:
                _spaceEvent_handleEvent(cookies, str(i[0]), i[1])
        else:
            print("     没有可处理的特殊事件")

        usaleList = energeProp_usaleList(cookies)  # 检查暂存的燃料
        if usaleList:
            for i in usaleList:
                _energyProp_use(cookies, i)
        else:
            print("     暂无可用燃料")
        task_status, source_id, done_distance, destination = flyTask_state(cookies)
        if task_status == 0:
            print(f"开启新任务:{destination}")
            flyTask_start(cookies, source_id)
        else:
            print(f"任务进行中:{destination}")
        print("*"*20)

        print("\n\n")

if __name__ == "__main__":
    run()