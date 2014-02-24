#coding:utf-8
from sqlalchemy import *

import dbconfig

class WeixinRealUser(dbconfig.DBBase):
    __tablename__ = 'weixin_realuser'
    openid = Column(String(64), primary_key=True,nullable=False)
    phone=Column(String(32),index=true,nullable=False)
    name=Column(String(16))
    phone_check_time=Column(TIMESTAMP)