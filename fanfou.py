#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        test.py
#created:        2010-12-18 22:42

import re
import pycurl
import json
import urllib
import StringIO
import time
#necessary to force chinese encoding(utf8)
import sys
from message import Msg

'''force utf-8 encoding system'''
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def time_from_0_to_8(timestr,timezone=8):
    '''convert fanfou time string(from API) to readable string format.
       like:
from: Sat Jan 03 23:08:54 +0000 2009 
to:   2009-01-04 07:08:54'''

    TIMEFORMAT="%a %b %d %X +0000 %Y"
    #Sat Jan 03 23:08:54 +0000 2009
    ISOTIMEFORMAT='%Y-%m-%d %X'
    x=time.strptime(timestr, TIMEFORMAT)
    m=time.mktime(x)+60*60*timezone
    p=time.strftime(ISOTIMEFORMAT,time.localtime(m))
    return p

def timestr_add_mins(timestr,mins=0,future=""):
    '''
    receive time str, format like: 2009-06-10 13:00:33
    and integer mins
    return seconds;
    '''
    ISOTIMEFORMAT='%Y-%m-%d %X'
    x=time.strptime(timestr, ISOTIMEFORMAT)
    m=time.mktime(x)+60*mins
    p=time.strftime(ISOTIMEFORMAT,time.localtime(m))
    return p

def unicode2utf8(ustr):
    '''print raw of "\u996d\u51c9\u4e86\u5426" unicode'''
    return eval("""u'''%s'''""" % ustr)

api={
    'exists':'http://api.fanfou.com/friendships/exists.json',
    'friends':'http://api.fanfou.com/friends/ids.json',
    'followers':'http://api.fanfou.com/followers/ids.json',
    "reply": "http://api.fanfou.com/statuses/replies.json",
    "show": "http://api.fanfou.com/users/show.json",
    "test": "http://api.fanfou.com/help/test.json",
    "timeline": "http://api.fanfou.com/statuses/user_timeline.json",
    "update": "http://api.fanfou.com/statuses/update.json",
    "verify": "http://api.fanfou.com/account/verify_credentials.json",
}

class Fanfou:
    def __init__(self, id="", sn=""):
        self.id=id
        self.sn=sn
        self.output = StringIO.StringIO()
        self.init_curl()

    def verify(self):
        c=self.curl
        self.output.truncate(0)
        url=api['verify']
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, self.output.write)
        c.perform()
        return self.output.getvalue()
             
    def __del__(self):
        try:
            self.curl.close()
            self.output.close()
        except:
            pass
    def init_curl(self):
        c=pycurl.Curl()
        id= u"%s:%s" % (self.id,self.sn)
        print id 
        c.setopt(c.USERPWD, str(id))
#        c.setopt(c.URL, api['test'])
#        c.setopt(c.VERBOSE, 1)
#        self.output.truncate(0)
#        c.setopt(c.WRITEFUNCTION, self.output.write)
#        c.perform()
#        if not self.get()=='ok':
#            exit()
        self.curl=c

    def get(self):
        value=self.output.getvalue()
        value=value.replace("false", "False")
        value=value.replace("true", "True")
        value=re.sub(r"(?<=\])[^\]]+$", '', value)
        return eval(value)

    def get_friends(self, api_type="friends"):
        c=self.curl 
        url=api[api_type]
        c.setopt(c.URL, url)
        self.output.truncate(0)
        c.perform()
        return self.get() 

           
    def get_msg(self, msg_type, count=20, since_id="", max_id="", page=1, extra=""):
        c=self.curl
        data={
            "count":count,
            "since_id": since_id,
            "max_id": max_id,
            "page": page,
        }
        url=api[msg_type]+"?"+urllib.urlencode(data)+extra
        c.setopt(c.URL, url)
        self.output.truncate(0)
        c.perform()
        return self.get() 

    def show(self, id):
        c=self.curl
        data={
            "id":id,
        }
        url=api['show']+"?"+urllib.urlencode(data)
        c.setopt(c.URL, url)
        self.output.truncate(0)
        c.perform()
        return self.get() 

def main():
    fanfou=Fanfou("******", "******")
    t=Timer()
    frs=fanfou.get_friends()
    fos=fanfou.get_friends("followers")
    mutual=list(set(frs) & set(fos))
    not_following_me=list(set(frs)-set(fos)) #follow me but i do not follow back
    im_not_following=list(set(fos)-set(frs))  #i follow them but not followed by them
    d={}
    t.start()
    for f in not_following_me:
        id=unicode2utf8(f)
        person=fanfou.show(id)
        d[id]=person
    t.stop()
    print "total %d secs, %d ids, and %f for each" % (t.get(), len(not_following_me),  (t.get()+0.0) / len(not_following_me))

if __name__=='__main__':
    main()
