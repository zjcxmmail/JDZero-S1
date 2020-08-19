import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# smtp发信服务
sender = ''                   # ① sender是邮件发送人邮箱
passWord = ''                 # ② passWord是服务器授权码
mail_host = 'smtp.qq.com'     # ③ mail_host是服务器地址（这里是QQsmtp服务器）
port = "465"                  # ④ QQsmtp服务器的端口号为465或587
receivers = ['']              # ⑤ receivers是邮件接收人，用列表保存，可以添加多个


def send_email(subject, msg_content):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg.attach(MIMEText(msg_content, 'text', 'utf-8'))
    try:
        s = smtplib.SMTP_SSL(mail_host, port)
        s.set_debuglevel(0)
        s.login(sender, passWord)
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender, to, msg.as_string())
            print('Success!')
        s.quit()
        print("All emails have been sent over!")
    except smtplib.SMTPException as e:
        print("Falied,%s", e)


if __name__ == "__main__":
    print(">>>检查有效性")
    send_email("test", "我是一封测试邮件\nfrom easyMail.py")
