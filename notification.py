import requests
import os
import smtplib
from email.mime.text import MIMEText
import time


#######################
# 通知服务
#######################

needYou2Know = 0   # [0,1,2,3]  0:不通知     1:server酱      2:SMTP邮件服务        3:bark服务

SCKEY = ''        # Server酱的SCKEY

email_dict = {
    "sender": '',                 # ① sender是邮件发送人邮箱
    "passWord": '',               # ② passWord是服务器授权码
    "mail_host": 'smtp.qq.com',   # ③ mail_host是服务器地址（这里是QQsmtp服务器）
    "port": 465,                  # ④ QQsmtp服务器的端口号为465或587
    "receiver": ''                # ⑤ receiver是邮件接收人
}

BARK = ''         # bark服务,自行搜索
##################################################################


def n0(a, b):
    """空函数,即不使用通知服务"""
    print(">>>>未开启通知服务")
    return


def send_email(subject, msg_content):
    """SMTP邮件服务,暂不支持读取Secrets"""
    if not email_dict["sender"]:
        print("SMTP服务的未设置!!\n取消推送")
        return
    print("SMTP服务启动")
    mail_host = email_dict["mail_host"]
    mail_user = email_dict["sender"]
    mail_pass = email_dict["passWord"]
    sender = mail_user
    receiver = email_dict["receiver"]
    message = MIMEText(msg_content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, email_dict["port"])  # ssl加密
        # smtpObj = smtplib.SMTP(mail_host, 25)                    # 明文发送
        smtpObj.login(mail_user, mail_pass)
        print("邮件登录成功")
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)


def serverJ(title, content):
    """server酱服务"""
    sckey = SCKEY
    if "SCKEY" in os.environ:
        """
        判断是否运行自GitHub action,"SCKEY" 该参数与 repo里的Secrets的名称保持一致
        """
        sckey = os.environ["SCKEY"]

    if not sckey:
        print("server酱服务的SCKEY未设置!!\n取消推送")
        return
    print("serverJ服务启动")
    data = {
        "text": title,
        "desp": content
    }
    response = requests.post(f"https://sc.ftqq.com/{sckey}.send", data=data)
    print(response.text)

def bark(title, content):
    """bark服务"""
    bark_token = BARK
    if "BARK" in os.environ:
        """
        判断是否运行自GitHub action,"BARK" 该参数与 repo里的Secrets的名称保持一致
        """
        bark_token = os.environ["BARK"]
    if not bark_token:
        print("bark服务的bark_token未设置!!\n取消推送")
        return
    response = requests.get(
        f"""https://api.day.app/{bark_token}/{title}/{content}""")
    print(response.text)
    
    
notify = [n0, serverJ, send_email, bark][needYou2Know]

if __name__ == "__main__":
    print("通知服务测试")
    start = time.time()
    notify("JD_tools脚本通知服务", "needYou2Know\n通知服务测试")
    print("耗时: ", time.time()-start, "s")
