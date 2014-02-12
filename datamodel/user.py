#coding:utf-8
from sqlalchemy import *

import dbconfig


class WeixinUser(dbconfig.DBBase):
    __tablename__ = 'weixin_user'
    openid = Column(String(64), primary_key=True,nullable=False)
    add_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    phone = Column(String(32),index=True)
    subscribe=Column(SmallInteger)
    nickname=Column(String(32))
    sex=Column(Integer)
    language=Column(String(16))
    city=Column(String(16))
    province=Column(String(16))
    country=Column(String(16))
    headimgurl=Column(String(1024))
    subscribe_time=Column(Integer)
    info_update=Column(Integer)
    last_recv_time=Column(Integer)


