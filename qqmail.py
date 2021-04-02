# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import time


def sendEmail(mail, key, isSmailCode):
    if isSmailCode == 2:
        subject = " ♡ 打卡成功"  # 主题
    else:
        subject = "----------失败"  # 主题

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
    now_time +=28800
    t = time.strftime("%m月%d号 %H点%M分", time.localtime(now_time))
    return t
