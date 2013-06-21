# encoding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *
from datetime import date
import time
import json
from analysis import nutrition_energy_analysis


def home(request):
    return render_to_response('home.html')

def user_rank(request):
    return render_to_response('userRanking.html')

def analysis(request):
    term = request.GET.get('term')
    flag = nutrition_energy_analysis(term)
    return render_to_response('analysis.html', {'term': term, 'flag': flag})

def convert_date(date_string):
    a = time.strptime(date_string, '%Y-%m-%d')
    return date(year=a.tm_year, month=a.tm_mon, day=a.tm_mday)

def is_long_topic(content):
    content = content.split('/')
    if len(content) > 4:
        return True
    else:
        return False

def topic(request):
    param = request.GET
    sdate = convert_date(param['start_date'])
    edate = convert_date(param['end_date'])
    query_set = Topic.objects.filter(start_date__gte=sdate, start_date__lte=edate)
    topic_list = []
    for item in query_set:
        if is_long_topic(item.topic_content):
            topic_list.append(item)
    return render_to_response('topic.html', {'start_date': sdate, 'end_date': edate, 'topic_list': topic_list})

def related_weibo(request):
    mids = request.GET.get('mids')
    mid_list = mids.split(',')
    WeiboNew_list = WeiboNew.objects.filter(mid__in=mid_list)
    weibo_list = []
    for item in WeiboNew_list:
        weibo_list.append(item.context)
    weibo_list_json = json.dumps(weibo_list, encoding="gb2312")
    return HttpResponse(weibo_list_json)
