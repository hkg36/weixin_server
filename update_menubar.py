#-*-coding:utf-8-*-
import urllib2
import json
APPID='wx1ece1ba1edd153d8'
APPSECRET='5430fab192812a77ea767d314adf9631'

"""
会员专区 会员注册 会员福利 门店查询 我的订单
辣妈课程 热门活动 宝贝课程 妈妈教室 孕妈故事
微型杂志 宝贝故事 童言无忌
"""
menu_body= {
     "button":[
      {
           "name":u"会员专区",
           "sub_button":[
            {
               "type":"click",
               "name":u"会员注册",
               "key":"PIC"
            },
             {
               "type":"click",
               "name":u"会员福利",
               "key":"AUDIO"
            },
              {
               "type":"click",
               "name":u"门店查询",
               "key":"ABOUT"
            },
               {
               "type":"click",
               "name":u"我的订单",
               "key":"ABOUT"
            }]
       },
      {
           "name":u"辣妈课程",
           "sub_button":[
            {
               "type":"click",
               "name":u"热门活动",
               "key":"ABOUT"
            },
             {
               "type":"click",
               "name":u"宝贝课程",
               "key":"ABOUT"
            },
              {
               "type":"click",
               "name":u"妈妈教室",
               "key":"ABOUT"
            },
              {
               "type":"click",
               "name":u"孕妈故事",
               "key":"ABOUT"
            } ]
       },
      {
           "name":u"微型杂志",
           "sub_button":[
            {
               "type":"click",
               "name":u"宝贝故事(1)",
               "key":"ABOUT"
            },
             {
               "type":"click",
               "name":u"宝贝故事(2)",
               "key":"ABOUT"
            },
              {
               "type":"click",
               "name":u"宝贝故事(3)",
               "key":"ABOUT"
            },
               {
               "type":"click",
               "name":u"宝贝故事(4)",
               "key":"ABOUT"
            },
              {
               "type":"click",
               "name":u"童言无忌",
               "key":"ABOUT"
            }]
       }]
 }

post_body=json.dumps(menu_body,ensure_ascii=False).encode('utf-8')
print post_body
resbody=urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(APPID,APPSECRET)).read()
data=json.loads(resbody)
access_token=data['access_token']

req=urllib2.Request('https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s'%access_token)
print urllib2.urlopen(req).read()

import pycurl
import StringIO

url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'%access_token
crl = pycurl.Curl()
crl.setopt(pycurl.FOLLOWLOCATION, 1)
crl.setopt(pycurl.MAXREDIRS, 5)
crl.setopt(pycurl.AUTOREFERER,1)
crl.setopt(pycurl.SSL_VERIFYHOST,0)
crl.setopt(pycurl.SSL_VERIFYPEER,0)

crl.setopt(pycurl.CONNECTTIMEOUT, 60)
crl.setopt(pycurl.TIMEOUT, 300)
#crl.setopt(pycurl.PROXY,proxy)
crl.setopt(pycurl.HTTPPROXYTUNNEL,1)
crl.fp = StringIO.StringIO()
crl.setopt(crl.POSTFIELDS,  post_body)
crl.setopt(pycurl.URL, url.encode('utf-8'))
crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
crl.perform()

print crl.fp.getvalue()