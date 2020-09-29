# -*- coding:utf-8 -*-
import datetime
import hashlib
import re
import time
import uuid

import scrapy
from pyquery import PyQuery as pq
from lxml.html import fromstring
from ..items import GetImgSpidersItem


def get_date(content):
    # if isinstance(content, unicode):
    # content = content.encode(encoding='UTF-8')
    pattern = r'(20\d{2})年(\d{1,2})月(\d{1,2})日'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        clien_date = result_str
        return result_str
    # 匹配2017-6-20
    pattern = r'(20\d{2})-(\d{1,2})-(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        return result_str
    # 匹配2017.6.20
    pattern = r'(20\d{2})\.(\d{1,2})\.(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        return result_str
    # 匹配2017/6/20
    pattern = r'(20\d{2})/(\d{1,2})/(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        return result_str
    # 匹配6月20日
    pattern = r'(\d{1,2})月(\d{1,2})日'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(0, 2):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '2017-' + '-'.join(result)
        # print(result_str)
        return result_str
    pattern = r'(\d{1,2})-(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(0, 2):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '2017-' + '-'.join(result)
        # print(result_str)
        return result_str
    return u''


def get_date2(timestamp):
    timestamp = str(timestamp)
    timestamp = int(timestamp[:10])
    date = datetime.datetime.utcfromtimestamp(timestamp)
    return get_date(str(date))


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'app.zgsyb.com.cn',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
}

headers2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'app.zgsyb.com.cn',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
}


class CnShiyoubaoImgSpider(scrapy.Spider):
    name = 'CN_ShiYouBao_img'
    allowed_domains = ['app.zgsyb.com', 'app.zgsyb.com.cn']
    start_urls = ['http://shiyou.com/']

    def start_requests(self):
        '''得到当天时间'''
        primordial_date = get_date2(int(time.time())).split('-')
        '''切换成列表页url要求时间'''
        date_url_str = primordial_date[0] + primordial_date[1] + '/' + primordial_date[2]
        print(date_url_str)
        for i in range(1, 9):
            list_url = 'http://app.zgsyb.com.cn/paper/layout/' + date_url_str + '/l0{}.html'.format(i)
            # list_url = 'http://app.zgsyb.com.cn/paper/layout/' + '202009/08' + '/l03.html'
            yield scrapy.Request(list_url, headers=headers, callback=self.parse, meta={'plate_id': str(i)})

    def parse(self, response):
        r = r'<img class="preview" src="(.*?)"'
        img_url = ''.join(re.findall(r, response.text)).replace('../', '')
        if 'http' not in img_url:
            image_url = 'http://app.zgsyb.com.cn/paper/' + img_url
        else:
            image_url = img_url
        item = {}
        plate_id = response.meta['plate_id']
        doc = pq(response.text)
        plate = doc('title').text().strip()
        item['mid'] = 1
        item['day'] = get_date2(int(time.time()))
        item['url'] = response.url
        item['image_url'] = image_url
        item['plate'] = '第{}版：{}'.format(plate_id, plate)
        item['uuid'] = hashlib.md5(item['url'].encode("utf-8") + item['image_url'].encode("utf-8")).hexdigest()
       # print(item)
        yield item
