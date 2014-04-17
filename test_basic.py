#coding:utf-8
__author__ = 'amen'
from datamodel.basic import *
#token=GetAccessToken()
#print(token)
#data=PostFile(token,r'D:\desktop\201402120700314c6c8.jpg')
#print data
#data=GetFile(token,data)
#print(data)

msgbody={
    "touser":'o8Td4jjhPJIsxqZVjuv8xzyLY-hU',
    "msgtype":"text",
    "text":
    {
         "content":u"你好"
    }
}

data=SendMessage("Ywqc7mGgFEOBsESyMNhWikFCSOkX_NzBiORx17tGMkh9OfdzC6Db3A3tZAJaEOX-V69Wn1_bisWO9SgsW2M7MhjYVCQ2OzcHa0QBHd-sezwoGkTb-tzy-wfG5pp6-s0Iil6NJX6vewy7x2NMCawsEg",msgbody)
print(data)

#print GetUserInfo(token,'oSqzEjq0iMnEG0JurYFi9blHV1zk')
#print GetUserWatch(token)
#print CreateQRCode(token,5667788,1800)
