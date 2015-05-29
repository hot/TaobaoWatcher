#!/usr/bin/python
# -*- coding: utf-8 -*-

import Queue
import urllib2
import time
import requests
import re

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

def sendMail(addr):
    msg = MIMEText("hello from python")

    me = addr
    you = addr
    msg['Subject'] = 'test subject'
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('127.0.0.1')
    s.sendmail(me, [you], msg.as_string())
    s.quit()

while(True):
#20692491682
    data = store(42202954800, True)
    prices = getPrice(data)
    sendMail('yourmailAddr')
    #need handle page
    break
    #time.sleep(10)

