#coding:utf-8
__author__ = 'amen'
from datamodel.basic import *
token=GetAccessToken()
print(token)
#data=PostFile(token,r'D:\desktop\201402120700314c6c8.jpg')
#print data
#data=GetFile(token,data)
#print(data)

"""msgbody={
    "touser":'oSqzEjiF9BSgYUG1RNlskESCrG4A',
    "msgtype":"text",
    "text":
    {
         "content":u"你好"
    }
}

data=SendMessage(token,msgbody)
print(data)"""

print GetUserInfo(token,'oSqzEjq0iMnEG0JurYFi9blHV1zk')
#print GetUserWatch(token)
print CreateQRCode(token,5667788,1800)