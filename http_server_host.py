#-*-coding:utf-8-*-
import hashlib
import time

import web
from lxml import etree
import datamodel.basic

from datamodel.location import WeixinLocation
from datamodel.user import WeixinUser
import dbconfig
import tools.helper
import re

HOSTNAME='weixin.haomeiniu.com'

utf8_parser = etree.XMLParser(encoding='utf-8')
class WeiXin(object):
    token='2187hoijdsa7322'
    def GET(self):
        inputs=web.input()
        tmpArr=[self.token,inputs.timestamp,inputs.nonce]
        tmpArr.sort()
        s=hashlib.sha1()
        s.update(''.join(tmpArr))
        print "%s=%s"%(s.hexdigest(),inputs.signature)
        if s.hexdigest()==inputs.signature:
            return inputs.echostr
        return 'some error'
    def POST(self):
        inputs=web.input()
        tmpArr=[self.token,inputs.timestamp,inputs.nonce]
        tmpArr.sort()
        s=hashlib.sha1()
        s.update(''.join(tmpArr))
        if s.hexdigest()!=inputs.signature:
            return
        data=web.data()
        doc=etree.fromstring(data, parser=utf8_parser)
        msg_type=doc.xpath(r'//xml/MsgType/text()',smart_strings=False)
        self.to_user=doc.xpath(r'//xml/ToUserName/text()',smart_strings=False)[0]
        self.from_user=doc.xpath(r'//xml/FromUserName/text()',smart_strings=False)[0]
        self.time=doc.xpath(r'//xml/CreateTime/text()',smart_strings=False)[0]
        #self.msgid=doc.xpath(r'//xml/MsgId/text()',smart_string=False)[0]
        fun=getattr(self,'on_'+msg_type[0])
        res=None
        if fun:
            res=fun(doc)
        if res is not None:
            res_str=etree.tostring(res,encoding="UTF-8")
            return res_str
    def on_event(self,doc):
        """<Event><![CDATA[EVENT]]></Event>
        <EventKey><![CDATA[EVENTKEY]]></EventKey>"""
        event=doc.xpath(r'//xml/Event/text()',smart_strings=False)[0]
        if event=='CLICK':
            event_key=doc.xpath(r'//xml/EventKey/text()',smart_strings=False)
            if event_key:
                event_key=event_key[0]
                fun=getattr(self,'on_menu_'+event_key)
                if fun:
                    return fun()
        elif event=="LOCATION":
            return self.On_event_location(doc)
        elif event=='subscribe':
            return self.On_event_subscribe(doc)
        elif event=='unsubscribe':
            return self.On_event_unsubscribe()
        elif event=='SCAN':
            return self.On_event_scan(doc)
    def on_menu_ABOUT(self):
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('text')
        etree.SubElement(new_root,'Content').text=etree.CDATA(u'功能还在建设中<a href="http://www.baidu.com">百度首页</a>')
        return new_root
    def on_menu_PIC(self):
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('news')
        etree.SubElement(new_root,'ArticleCount').text=str(2)
        Articles=etree.SubElement(new_root,'Articles')
        self._add_picture_articles(Articles,u"美女",u'美女1','http://projects.unbit.it/images/logo_uWSGI.png','http://%s'%HOSTNAME)
        self._add_picture_articles(Articles,u"美女",u'美女2','http://%s/static/02.jpg'%HOSTNAME,'http://%s'%HOSTNAME)

        return new_root
    def on_menu_AUDIO(self):
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('music')
        music=etree.SubElement(new_root,'Music')
        etree.SubElement(music,'Title').text=etree.CDATA(u'音乐试听')
        etree.SubElement(music,'Description').text=etree.CDATA(u'就是音乐试听而已')
        etree.SubElement(music,'MusicUrl').text=etree.CDATA('http://%s/static/music01.mp3'%HOSTNAME)
        etree.SubElement(music,'HQMusicUrl').text=etree.CDATA('http://%s/static/music01.mp3'%HOSTNAME)
        return new_root
    def On_event_subscribe(self,doc):
        token=datamodel.basic.GetAccessToken()
        userdata=datamodel.basic.GetUserInfo(token,self.from_user)
        with dbconfig.Session() as session:
            weixin_user=WeixinUser()
            weixin_user.openid=self.from_user
            weixin_user.last_recv_time=time.time()
            weixin_user.subscribe=1
            weixin_user.province=userdata['province']
            weixin_user.city=userdata['city']
            weixin_user.headimgurl=userdata['headimgurl']
            weixin_user.language=userdata['language']
            weixin_user.country=userdata['country']
            weixin_user.sex=userdata['sex']
            weixin_user.nickname=userdata['nickname']
            session.merge(weixin_user)
            session.commit()
        scenceid=0
        eventkey=doc.xpath(r"/xml/EventKey/text()",smart_strings=False)
        if eventkey:
            match=re.match(r'qrscene_(?P<code>\d+)',eventkey[0])
            if match:
                scenceid=int(match.group('code'))
                print(scenceid)
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('text')
        etree.SubElement(new_root,'Content').text=etree.CDATA(u'%s,感谢您关注现场加,功能开发中,请期待(scenceid=%d)'%(userdata['nickname'],scenceid))
        return new_root
    def On_event_unsubscribe(self):
        with dbconfig.Session() as session:
            weixin_user=session.query(WeixinUser).filter(WeixinUser.openid==self.from_user).first()
            if weixin_user is not None:
                weixin_user.subscribe=0
                session.merge(weixin_user)
                session.commit()
    def _buildReplyBase(self):
        new_root=etree.Element('xml')
        etree.SubElement(new_root,'ToUserName').text=etree.CDATA(self.from_user)
        etree.SubElement(new_root,'FromUserName').text=etree.CDATA(self.to_user)
        etree.SubElement(new_root,'CreateTime').text=str(time.time())
        return new_root
    def on_text(self,doc):
        src_text=doc.xpath(r'//xml/Content/text()',smart_strings=False)[0]
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('text')
        etree.SubElement(new_root,'Content').text=etree.CDATA(u'RE:%s'%src_text)
        return new_root
    def _add_picture_articles(self,Articles,Title,Description,PicUrl,Url):
        item=etree.SubElement(Articles,'item')
        etree.SubElement(item,'Title').text=etree.CDATA(Title)
        etree.SubElement(item,'Description').text=etree.CDATA(Description)
        etree.SubElement(item,'PicUrl').text=etree.CDATA(PicUrl)
        etree.SubElement(item,'Url').text=etree.CDATA(Url)
    def on_location(self,doc):
        lat=float(doc.xpath(r'//xml/Location_X/text()',smart_strings=False)[0])
        long=float(doc.xpath(r'//xml/Location_Y/text()',smart_strings=False)[0])
        scale=int(doc.xpath(r'//xml/Scale/text()',smart_strings=False)[0])
        label=doc.xpath(r'//xml/Label/text()',smart_strings=False)[0]

        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('text')
        etree.SubElement(new_root,'Content').text=etree.CDATA('lat %.6f long %.6f %d %s'%(lat,long,scale,label))
        return new_root
    def On_event_location(self,doc):
        """<Latitude>23.137466</Latitude>
    <Longitude>113.352425</Longitude>
        <Precision>119.385040</Precision>"""
        lat=float(doc.xpath(r'//xml/Latitude/text()',smart_strings=False)[0])
        long=float(doc.xpath(r'//xml/Longitude/text()',smart_strings=False)[0])
        prec=float(doc.xpath(r'//xml/Precision/text()',smart_strings=False)[0])
        with dbconfig.Session() as session:
            wloc=WeixinLocation()
            wloc.openid=self.from_user
            wloc.lat=lat
            wloc.long=long
            wloc.prec=prec
            wloc.geokey=tools.helper.CombineGeo(long,lat)
            session.merge(wloc)
            session.commit()
    def On_event_scan(self,doc):
        scenceid=int(doc.xpath(r'/xml/EventKey/text()',smart_strings=False)[0])
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('text')
        etree.SubElement(new_root,'Content').text=etree.CDATA(u'扫描二维码(scenceid=%d)'%scenceid)
        return new_root
    def on_voice(self,doc):
        text=doc.xpath(r'/xml/Recognition/text()',smart_strings=False)[0]
        new_root=self._buildReplyBase()
        etree.SubElement(new_root,'MsgType').text=etree.CDATA('text')
        etree.SubElement(new_root,'Content').text=etree.CDATA(u'你想说:%s'%text)
        return new_root
urls = (
    '/weixin', WeiXin,
    )
webapp=web.application(urls, globals())
if __name__ == '__main__' :
    webapp.run()