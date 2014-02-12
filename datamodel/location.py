#coding:utf-8
from sqlalchemy import *

import dbconfig


class WeixinLocation(dbconfig.DBBase):
    __tablename__ = 'weixin_location'
    openid = Column(String(64), primary_key=True,nullable=False)
    add_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    lat=Column(Float,nullable=False)
    long=Column(Float,nullable=False)
    prec=Column(Float)
    geokey=Column(BigInteger,index=True,nullable=False)
