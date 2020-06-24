#!/usr/bin/env python
# coding: utf-8
# author:谈英杰
# date:2020/6/24
# function:通过微信小程序的数据库获取用户数据并进行自动运行帮用户参加摇号
# how to invoke/dependecy：通过微信的云数据库获取数据
# reference:https://www.yuque.com/ol1q37/gi94xp/pnfdhx
# background：应每隔三个月就需要去重新需要一次故开发此程序每过一段时间就自动续摇一次

import requests
import json
from selenium import webdriver
import time
from PIL import ImageGrab
import re
import os
from zidong import *

appid="wxae8d7c45066d6989&secret=c7b7c6a46c07b34801ddeb195acd2f9d"
env="dev-oh37x"

def get_access_token():
    """获取access_token"""
    req = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}".format(appid))
    access_token = eval(req.text)['access_token']
    return access_token

def get_vip(access_token):
    """获取openid"""
    query = "db.collection('users').where({is_vip:true}).get()"
    data = {}
    data["query"] = query
    data["env"] = env
    url = 'https://api.weixin.qq.com/tcb/databasequery?access_token={}'.format(access_token)
    r = requests.post(url, data = json.dumps(data)).json()
    # eval(r['data'][0])
    is_vip = json.loads(r["data"][0])#deserlizer serlizer dict2json str jsonstr 2 dict
    is_vip = is_vip["is_vip"]
    openid = json.loads(r["data"][0])#deserlizer serlizer dict2json str jsonstr 2 dict
    openid = openid["openid"]
    return (is_vip,openid)
    
def get_zhma(access_token, openid):
    """通过openid获取用户账号密码"""
    url = 'https://api.weixin.qq.com/tcb/databasequery?access_token={}'.format(access_token)
    data = { 'env':env,
    'query':'db.collection(\'accounts\').where({openid:"'+openid+'"}).get()'}
    r = requests.post(url, data=json.dumps(data)).json()
    username = eval(r['data'][0])['username']
    password = eval(r['data'][0])['password']
    return (username,password)

def update_rq(access_token,openid):
    """更新摇号日期"""
    url = 'https://api.weixin.qq.com/tcb/databaseupdate?access_token={}'.format(access_token)
    is_vip,openid=get_vip(access_token)

    date = time.strftime('%Y/%m/%d',time.localtime(time.time()))
    data = { 'env':env,
    'query':'db.collection(\'users\').where({openid:"'+openid+'"}).update({data: {crawlered_at: "'+date+'"}})'}
    r = requests.post(url, data=json.dumps(data)).json()

def main():
    access_token=get_access_token()
    url = 'https://api.weixin.qq.com/tcb/databasequery?access_token={}'.format(access_token)
    data = { 'env':env,
    'query':'db.collection(\'users\').get()'}
    r = requests.post(url, data=json.dumps(data)).json()
    for i in r['data']:
        is_vip,openid=get_vip(access_token)
        if get_vip(access_token)[0]==True:
            login_operation()
            update_rq(access_token,openid)

if __name__ == "__main__":
    main()