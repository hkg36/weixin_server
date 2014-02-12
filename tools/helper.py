__author__ = 'amen'
try:
    import GeoCombine
except Exception,e:
    GeoCombine=None
import json
import datetime
import time


def CombineGeo(long,lat):
    lat_int=int((lat+90)*10e6)
    long_int=int((long+180)*10e6)
    if GeoCombine:
        return GeoCombine.Combine(long_int,lat_int)
    else:
        result=0;
        for i in xrange(32): #sizeof(unsigned int)*8;i++)
            mid=long_int&(0x1<<i);
            result|=mid<<i;

        for i in xrange(32):
            mid=lat_int&(0x1<<i);
            result|=mid<<(i+1);
        return result;

class AutoFitJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return time.mktime(obj.timetuple())
        return json.JSONEncoder.default(self, obj)
if __name__ == '__main__':
    print CombineGeo(147.9873,32.5678)