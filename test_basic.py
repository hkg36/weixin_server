__author__ = 'amen'
from datamodel.basic import *
token=GetAccessToken()
print(token)
data=PostFile(token,r'D:\desktop\201402120700314c6c8.jpg')
print data
data=GetFile(token,data)
print(data)