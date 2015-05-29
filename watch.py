#!/usr/bin/python
# -*- coding: utf-8 -*-

import Queue
import urllib2
import time
import requests
import re
import sys

import smtplib
from email.mime.text import MIMEText


itemPage = """http://h5.m.taobao.com/awp/core/detail.htm?id=42202954800"""

def store(itemID, bSave):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'detailskip.taobao.com',
        'Referer': 'http://item.taobao.com/item.htm?id={}'.format(itemID),    #this is id!!!
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36'\
                      ' (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36',
    }

    #url = 'http://detailskip.taobao.com/json/sib.htm?itemId=42202954800'\
    #      '&sellerId=1052965317&p=1&rcid=50013886'\
    #      '&sts=404574208,1170936092640149508,144115188075888768,4297129987'\
    #      '&chnl=pc&price=183301&shopId=&vd=1&skil=false&pf=1&al=false'\
    #      '&ap=0&ss=0&free=1&st=1&ct=1&prior=1&ref='

    url = 'http://detailskip.taobao.com/json/sib.htm?itemId={}'\
          '&p=1'.format(itemID)

    res = requests.get(url, headers=headers)
    html = res.text

    if bSave:
        with open("page.html", 'w') as outfile:
            html = html.encode('utf-8')
            outfile.write(html)
            print "page saved!!"

    return html

def getPrice(data):
    result = re.findall('price:"(\d+\.\d+)"', data)
    result = [float(x) for x in result]
    print(result)
    return result

def sendGMail(mailAddr, passwd, text):
    gmail_user = mailAddr
    gmail_pwd = passwd
    FROM = 'user@gmail.com'
    TO = [mailAddr] #send to self
    SUBJECT = "Good prices"

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, text)
    try:
        #server = smtplib.SMTP(SERVER) 
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def send163Mail(receiver, title, body):
        host = 'smtp.163.com'
        port = 25
        sender = 'xx@xx.com'
        pwd = 'XXXXXX'

        msg = MIMEText(body, 'html')
        msg['subject'] = title
        msg['from'] = sender
        msg['to'] = receiver

        s = smtplib.SMTP(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())

        print 'The mail named %s to %s is sended successly.' % (title, receiver)

def main(argv):
    mailAddr, passwd = argv
    print(mailAddr, passwd)

    while(True):
    #20692491682
        data = store(42202954800, True)
        prices = getPrice(data)
        sendGMail(mailAddr, passwd, prices)
        #need handle page
        break
        #time.sleep(10)


if __name__ == "__main__":
   main(sys.argv[1:])
