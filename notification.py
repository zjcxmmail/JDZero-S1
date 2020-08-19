import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#######################
# 通知服务
#######################

needYou2Know = 0    # [0,1,2]  0:不通知     1:server酱      2:SMTP邮件服务

SCKEY = ''        # Server酱的SCKEY
email_dict = {
    "sender": '',                 # ① sender是邮件发送人邮箱
    "passWord": '',               # ② passWord是服务器授权码
    "mail_host": 'smtp.qq.com',   # ③ mail_host是服务器地址（这里是QQsmtp服务器）
    "port": "465",                # ④ QQsmtp服务器的端口号为465或587
    "receivers": ['']             # ⑤ receivers是邮件接收人，用列表保存，可以添加多个
}
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
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email_dict["sender"]
    msg.attach(MIMEText(msg_content, 'text', 'utf-8'))
    try:
        s = smtplib.SMTP_SSL(email_dict["mail_host"], email_dict["port"])
        s.set_debuglevel(0)
        s.login(email_dict["sender"], email_dict["passWord"])
        # 给receivers列表中的联系人逐个发送邮件
        for item in email_dict["receivers"]:
            msg['To'] = to = item
            s.sendmail(email_dict["sender"], to, msg.as_string())
            print('Success!')
        s.quit()
        print("All emails have been sent over!")
    except smtplib.SMTPException as e:
        print("Falied,%s", e)


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


notify = [n0, serverJ, send_email][needYou2Know]

if __name__ == "__main__":
    print("通知服务测试")
    notify("JD_tool脚本通知", "needYou2Know")
