#!/usr/bin/python
# -*- coding:utf-8 -*-
from urlparse import urlparse
import datetime
import base64
import hmac
import hashlib
import json
import urllib2
import os


#id and secret
ak_id = 'LTAIWmpLokrDNY3u'
ak_secret = 'wfVXMK0NcrK3uVr3dlF2qLw2K5XOI7'

def confidence(img1,img2,mode=1):
    
    #模式1，输入图像base64编码
    if mode ==1:
        print 'encoding...'
        img1=image_encode(img1)
        img2=image_encode(img2)
        options = {
            'url': 'https://dtplus-cn-shanghai.data.aliyuncs.com/face/verify',
            'method': 'POST',
            'body': json.dumps({"type":mode,"content_1":img1,"content_2":img2}, separators=(',', ':')),
            'headers': {
                'accept': 'application/json',
                'content-type': 'application/json',
                'date':  get_current_date(),
                'authorization': ''
            }
        }
    #模式0，输入图像链接
    elif mode == 0:
        options = {
            'url': 'https://dtplus-cn-shanghai.data.aliyuncs.com/face/verify',
            'method': 'POST',
            'body': json.dumps({"type":mode,"image_url_1":img1,"image_url_2":img2}, separators=(',', ':')),
            'headers': {
                'accept': 'application/json',
                'content-type': 'application/json',
                'date':  get_current_date(),
                'authorization': ''
            }
        }
        
    body = ''
    if 'body' in options:
        body = options['body']
    #print body
    bodymd5 = ''
    if not body == '':
        bodymd5 = to_md5_base64(body)
    #print bodymd5
    urlPath = urlparse(options['url'])
    if urlPath.query != '':
        urlPath = urlPath.path + "?" + urlPath.query
    else:
        urlPath = urlPath.path

    #print urlPath    
    stringToSign = options['method'] + '\n' + options['headers']['accept'] + '\n' + bodymd5 + '\n' + options['headers']['content-type'] + '\n' + options['headers']['date'] + '\n' + urlPath
    signature = to_sha1_base64(stringToSign, ak_secret)
    #print stringToSign
    #print signature
    authHeader = 'Dataplus ' + ak_id + ':' + signature
    options['headers']['authorization'] = authHeader
    #print authHeader
    request = None
    method = options['method']
    url = options['url']
    #print method
    #print url
    if 'GET' == method or 'DELETE' == method:
        request = urllib2.Request(url)
    elif 'POST' == method or 'PUT' == method:
        request = urllib2.Request(url, body)
    request.get_method = lambda: method
    for key, value in options['headers'].items():
        request.add_header(key, value)
    try:
        print 'connecting..'
        conn = urllib2.urlopen(request)
        
        response = conn.read()
        #返回可信度
        return json.loads(response)['confidence']
    except urllib2.HTTPError, e:
        print e.read()
        raise SystemExit(e)
    
def get_current_date():
    date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
    return date
   
    
def to_md5_base64(strBody):
    hash = hashlib.md5()
    hash.update(strBody)
    return hash.digest().encode('base64').strip()

    
def to_sha1_base64(stringToSign, secret):
    hmacsha1 = hmac.new(secret, stringToSign, hashlib.sha1)
    return base64.b64encode(hmacsha1.digest())
    
def image_encode(fileName):
    fileSize = os.path.getsize(fileName)
    with open(fileName,'rb') as f:
        data = base64.b64encode(f.read())
    return data


if __name__ == "__main__" :
    print confidence("https://b-ssl.duitang.com/uploads/item/201605/15/20160515065257_seVXJ.thumb.700_0.jpeg","http://p0.qhimgs4.com/t0198839e2297c13be1.jpg",0)
    print confidence("img1.jpeg","img2.jpeg")
