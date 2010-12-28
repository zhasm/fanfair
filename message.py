'''parse raw fanfou message and only return important items'''
from time import *
import time
import json
import re

ISOTIMEFORMAT='%Y-%m-%d %X'
TIMEFORMAT="%a %b %d %X +0000 %Y"

def unicode2utf8(ustr):
    '''print raw of "\u996d\u51c9\u4e86\u5426" unicode'''
    return eval("""u'''%s'''""" % ustr)

def epoch2str( x ):
    '''Convert unix epoch to string'''
    return strftime( "%Y-%m-%d %H:%M:%S", gmtime(x+3600*8) )

def time_from_0_to_8(timestr, timezone=8):

    #Sat Jan 03 23:08:54 +0000 2009
    x=time.strptime(timestr, TIMEFORMAT)
    m=time.mktime(x)+60*60*timezone
#    p=time.strftime(ISOTIMEFORMAT,time.localtime(m))
    return int(m)

def unescape(s):
    s=s.replace("&lt;","<")
    s=s.replace("&gt;",">")
    s=s.replace("&quot;",'"')
    s=s.replace("&apos;","'")
    s=s.replace("&amp;","&")
    s=s.replace("\\","")
    return s

def add_time(p_time, send_time):
    '''send_time: absolute time seconds;
       p_time: offset in string format
    '''

    now=time.localtime()
    print p_time
    match = re.search(
	    r"""(?:(?P<year>\d{4})-(?=\d+))?
	(?:(?:(?P<month>\d{1,2})-)?(?P<date>\d{1,2})\s+)?
	(?P<hour>\d{1,2}):(?P<mins>\d{1,2}) |
	(?P<min3>\d+)
	    """, p_time, re.VERBOSE)
    if match:
        min3 = match.group("min3")
        if min3:
            x=int(send_time)+int(min3)*60+3600*8
            #x=time.strftime(ISOTIMEFORMAT,time.localtime(x))
            return x
        year = match.group("year")
        if year==None:
            year=now.tm_year
        month = match.group("month")
        date = match.group("date")
        if month==None :
            month=now.tm_mon
        if date==None:
            date=now.tm_mday
        hour=match.group("hour")
        mins=match.group("mins")
        return time.strptime("%04d-%02d-%02d %02d:%02d:%00" % (int(year),int(month),int(date),int(hour),int(mins)), ISOTIMEFORMAT)




class Msg:
    def __init__(self, msg):
        #self.created_at=time_from_0_to_8(msg['created_at'])
        try:
            self.id=msg['id']
            self.at=time_from_0_to_8(msg['created_at'])
            self.userid=unicode2utf8(msg['user']['id'])
            self.username=unicode2utf8(msg['user']['screen_name'])
            self.text=unicode2utf8(msg['text'])
            self.text=unescape(self.text)
        except:
            print json.dumps(msg, indent=3)

    def get_msg(self):
        try:
            return {
                'id':self.id,
                'userid':self.userid,
                'text':self.text,
                'at':self.at
            }
        except:
            return None
    def show(self):
        try:
            print "{\n\tmsgID:\t", self.id
            print "\tAt:\t", epoch2str(self.at)
            print "\tFrom:\t", self.username
            print "\tMsg:\t", self.text
            print "}\n"
        except:
            pass
    def parse(self):
        msg=self.text


class Task():
    def __init__(self, messages):
        '''get a list of messages, and save them to DB'''
        self.msgs=messages

    def _parse_text(self, text):
        try:
            match=re.findall(r"@\S+\s+(?P<time>[-\d\s:]+)\s+(?P<todo>.*$)", text)
            if match:
                return match[0]
            else:
                return [None, None]
        except:
            raise

    def _parse_task(self):
        '''get the'''
        tasks=[]
        for msg in self.msgs:
            m=msg.get_msg()
            when, text=self._parse_text(m['text'])
            if when:
                when=add_time(when, m['at'])
                tasks.append([m['userid'], m['id'], text ,when])
        self.tasks=tasks

    def get(self):
        self._parse_task()
        return self.tasks
#        c=db.cursor()
#        c.executemany("""insert into task(userid, msg, msg_id, time) values(?,?,?,?)""",
#        conn.commit()
        pass



