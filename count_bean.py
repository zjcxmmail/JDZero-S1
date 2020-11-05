import requests
import json
import jdCookie
import re
from datetime import datetime, timedelta
import notification

"""
统计当天获得的京豆,当项目过多时,可能不全
cron 30 18 * * *
"""


def totalBean(cookies):
    headers = {
        'Host': 'wq.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://wqs.jd.com/my/jingdou/my.shtml?sceneval=2',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('sceneid', '80027'),
        ('sceneval', '2'),
        ('callback', 'getUserInfoCb'),
    )

    response = requests.get('https://wq.jd.com/user/info/QueryJDUserInfo',
                            headers=headers, params=params, cookies=cookies)
    result = response.text
    regex = r"\"jdNum\" : (\d+)"
    matches = re.findall(regex, result, re.MULTILINE)
    if matches:
        return matches[0]
    return None


def jingDetailList(cookies, page):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://bean.m.jd.com',
        'Host': 'bean.m.jd.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://bean.m.jd.com/beanDetail/index.action?resourceValue=bean',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {'page': str(page)}
    response = requests.post('https://bean.m.jd.com/beanDetail/detail.json',
                             headers=headers, cookies=cookies, data=data)
    result = response.json()
    if not result:
        return []
    beanList = result["jingDetailList"]
    return beanList


def countTodayBean(cookies):
    income = 0
    expense = 0
    page_1 = jingDetailList(cookies, 1)
    todayBeanList = [int(i["amount"])
                     for i in page_1 if _datatime in i["date"]]
    income_tmp = [i for i in todayBeanList if i > 0]
    expense_tmp = [i for i in todayBeanList if i < 0]
    income += sum(income_tmp)
    expense += sum(expense_tmp)
    page = 1
    while(len(page_1) == len(todayBeanList)):
        page += 1
        page_1 = jingDetailList(cookies, page)
        todayBeanList = [int(i["amount"])
                         for i in page_1 if _datatime in i["date"]]
        income_tmp = [i for i in todayBeanList if i > 0]
        expense_tmp = [i for i in todayBeanList if i < 0]
        income += sum(income_tmp)
        expense += sum(expense_tmp)
    return income, expense


utc_dt = datetime.utcnow()  # UTC时间
bj_dt = utc_dt+timedelta(hours=8)  # 北京时间
_datatime = bj_dt.strftime("%Y-%m-%d", )
now = bj_dt.strftime("%Y-%m-%d %H:%M:%S")
message = ""
for cookies in jdCookie.get_cookies():
    total = totalBean(cookies)
    income, expense = countTodayBean(cookies)
    message += f'\n\n【{cookies["pt_pin"]}】 \n当前京豆: {total} \n今日收入: +{income} \n今日支出: {expense}'

    print("\n")
print(f"⏰ 京豆统计 {now}")
print(message)
notification.notify(f"⏰ 京豆统计 {now}", message)
