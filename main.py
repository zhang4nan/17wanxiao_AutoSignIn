import time
import json
import requests
import datetime
import logging
from campus import CampusCard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
# driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)


def initLogging():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="[%(levelname)s]; %(message)s")


def main():
    # sectets字段录入
    sckey, success, failure, result, phone, password = [], [], [], [], [], []
    # 多人循环录入
    while True:
        try:
            users = input()
            info = users.split(',')
            phone.append(info[0])
            password.append(info[1])
            sckey.append(info[2])
        except BaseException:
            break

    # 提交打卡
    for index, value in enumerate(phone):
        print("开始获取用户%s信息" % (value[-4:]))
        count = 0
        while count < 3:
            try:
                campus = CampusCard(phone[index], password[index])
                token = campus.user_info["sessionId"]
                driver.get('https://reportedh5.17wanxiao.com/collegeHealthPunch/index.html?token=%s#/punch?punchId=180'%token)
                time.sleep(2)
                strTime = GetNowTime()
                res = check_in(token)
                if res['code'] == '10000':
                    success.append(value[-4:])
                    logging.info(value[-4:] + "打卡成功-" + strTime)
                    result = res
                    break
                elif res['code'] != '10000':
                    failure.append(value[-4:])
                    logging.info(value[-4:] + "打卡异常-" + strTime)
                    count = count + 1
                    print('%s打卡失败，开始第%d次重试...' % (value[-6:], count))
                    time.sleep(30)

            except Exception as err:
                print(err)
                logging.warning('出现错误')
                failure.append(value[-4:])
                break
        print("-----------------------")
    fail = sorted(set(failure), key=failure.index)
    title = "成功: %s 人,失败: %s 人" % (len(success), len(fail))
    try:
        if len(sckey[0]) > 2:
            print('主用户开始微信推送...')
            WechatPush(
                title,
                'https://sc.ftqq.com/' +
                sckey[0] +
                '.send',
                success,
                fail,
                result)
    except BaseException:
        print("微信推送出错！%s")


# 时间函数
def GetNowTime():
    cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    strTime = cstTime.strftime("%H:%M:%S")
    return strTime


# 打卡参数配置函数
def GetUserJson(token):
    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"
    user_json = {
        "jsonData": {
            "templateid": "pneumonia",
            "token": token
        },
        "businessType": "epmpics",
        "method": "userComeApp"
    }
    res = requests.post(sign_url, json=user_json, verify=False).json()
    print("这是res")
    print(res)
    data = json.loads(res['data'])
    print("这是data")
    print(data)
    post_dict = {
        "add": data['add'],
        "areaStr": data['areaStr'],
        "businessType": "epmpics",
        "method": "submitUpInfo",
        "jsonData": {
            "deptid": data['deptStr']['deptid'],
            "gpsType": 1,
            "userid": data['userid'],
            "stuNo": data['stuNo'],
            "source": "app",
            "templateid": data['templateid'],
            "token": token,
            "reportdate": round(time.time() * 1000),
            "username": data['username'],
            "phonenum": data['phonenum'],
            "customerid": data['customerid'],
            "deptStr": data['deptStr'],
            "areaStr": data['areaStr'],
            "updatainfo": [{"propertyname": i["propertyname"], "value": i["value"]}
                           for i in data['cusTemplateRelations']],
        }
    }
    # print(post_dict)
    return post_dict


# 打卡提交函数
def check_in(token):
    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"
    jsons = GetUserJson(token)
    # print(jsons)
    # 提交打卡
    res = requests.post(sign_url, json=jsons, verify=False).json()
    print("要提交的res")
    print(res)
    return res


# 微信通知

def WechatPush(title, sckey, success, fail, result):
    strTime = GetNowTime()
    page = json.dumps(
        result.json(),
        sort_keys=True,
        indent=4,
        separators=(
            ',',
            ': '),
        ensure_ascii=False)
    content = f"""
        `{strTime}`
        #### 打卡成功用户：
        `{success}`
        #### 打卡失败用户:
        `{fail}`
        #### 主用户打卡信息:
        ```
        {page}
        ```
             """
    data = {
        "text": title,
        "desp": content
    }
    try:
        req = requests.post(sckey, data=data)
        if req.json()["errmsg"] == 'success':
            print("Server酱推送服务成功")
        else:
            print("Server酱推送服务失败")
    except BaseException:
        print("微信推送参数错误")


if __name__ == '__main__':
    main()
