#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response
from fanfou import Fanfou
from hashlib import md5
import os
from os.path import dirname as dirname
from snippets import *
from django.template.loader import get_template
from json import dumps
cache={}

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding) 


def index(request):

    ''' s=request.session
        return HttpResponse('session infor : %r' % cache.items())
    '''
    return render_to_response("index.html")

def login(request):

    username=request.GET.get('id', '')
    password=request.GET.get('sn', '') 
    if not username or not password: 
        return HttpResponse("0")
        
    fanfou=Fanfou(username, password)
    return HttpResponse(fanfou.verify(), mimetype="text/javascript")

    '''        
    if fanfou.verify():
        return HttpResponse("1")
    else:
        return HttpResponse("2")

    id=md5(username+password).hexdigest()
    s['session_id']=id
    cache[id]=fanfou '''


def who(request):
    s=request.session
    if not s.has_key("session_id"):
        return HttpResponse("no session! error!")
    fanfou=cache[s['session_id']]
    return HttpResponse(fanfou.id+fanfou.sn)



