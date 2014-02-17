#-*-coding:utf-8-*-
import urllib2
import json
from datamodel.basic import *

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

token=GetAccessToken()
print DeleteMemu(token)
print SetMenu(token,menu_body)