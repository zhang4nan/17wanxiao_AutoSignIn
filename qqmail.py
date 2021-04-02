# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import time

import requests

yburl = 'https://free-api.heweather.com/s6/weather/forecast'
cyurl = 'https://free-api.heweather.com/s6/weather/lifestyle'

value = {
    'location': '咸阳',
    'key': '1fb7bd7b7a224138b85e1d2f570b86a1',
    'lang': 'zh'
}

ybreq = requests.get(yburl, params=value)
cyreq = requests.get(cyurl, params=value)

ybjs = ybreq.json()
cyjs = cyreq.json()

for i in range(1):
    yb = ybjs['HeWeather6'][0]['daily_forecast']
    cy = cyjs['HeWeather6'][0]['lifestyle'][1]
    gj = cyjs['HeWeather6'][0]['lifestyle'][0]
    d1 = u'\r\n\r\n咸阳' + '  ' + yb[i]['cond_txt_d'] + '\r\n' + yb[i]['date'] + '\r\n\r\n'
    d2 = gj['txt'] + ' \r\n' + cy['txt']
    d3 = d1 + ' \n' + d2


def sendEmail(mail, key, isSmailCode):
    if isSmailCode == 2:
        subject = "  打卡成功 "  # 主题
    else:
        subject = "  打卡失败 "  # 主题

    msg_from = '2420955917@qq.com'  # 发送方邮箱，
    passwd = ''.join(key)  # 填入发送方邮箱的授权码
    msg_to = ''.join(mail)   # 收件人邮箱
    content = timer()
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        send = smtplib.SMTP_SSL("smtp.qq.com", 465)   # 邮件服务器及端口号
        send.login(msg_from, passwd)
        send.sendmail(msg_from, msg_to, msg.as_string())
        return "邮箱推送成功"
    except Exception:
        return "邮箱推送失败"


def timer():
    now_time = int(time.time())
    now_time += 28800
    t = time.strftime("%m月%d号 %H点%M分 ", time.localtime(now_time))
    t += d3
    return t 
