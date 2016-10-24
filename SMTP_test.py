#! usr/bin/python3
# -*- coding:utf-8-*-
from email.mime.text import MIMEText
import smtplib


msg = MIMEText('hello, send by python...', 'plain', 'utf-8')
# input email address
from_addr = input('From:')
password = input('Password:')
# input delivery address
to_addr = input('To:')
smtp_server = input('SMTP server:')

server = smtplib.SMTP(smtp_server, 25)  # default SMTP Port is 25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()