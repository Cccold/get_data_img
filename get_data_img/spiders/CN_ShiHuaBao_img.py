# -*- coding:utf-8 -*-
import hashlib

import scrapy
import uuid

import scrapy
from pyquery import PyQuery as pq
import time
import datetime
import re
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


def get_title(yuan_title):
    tit_r = re.compile('[^<BR/>]+')
    t = tit_r.findall(yuan_title)
    tt = ''.join(t)
    if '\n' in tt:
        title = tt.replace('\n', '')
        return title
    return tt
    # print(title,type(title))

    # return tit_conn


def get_author2(er_author):
    if er_author:
        author_list = er_author.split(' ')
        for i in range(author_list.count('')):
            author_list.remove('')
        author_list2 = []
        i = 0
        while i < len(author_list):
            if 2 <= len(author_list[i]) <= 3:
                author_list2.append(author_list[i])
            elif len(author_list[i]) == 1:
                try:
                    author_list2.append(author_list[i] + author_list[i + 1])
                    i += 1
                except:
                    pass
            elif len(author_list[i]) > 3:
                pass
            i += 1
        author = ' '.join(author_list2)

    else:
        author = er_author
    return author


class CnShihuabaoImgSpider(scrapy.Spider):
    name = 'CN_ShiHuaBao_img'
    allowed_domains = ['219.232.112.99']
    start_urls = []

    def start_requests(self):
        '''得到当天时间'''
        primordial_date = get_date2(int(time.time())).split('-')
        '''切换成列表页url要求时间'''
        date_url_str = primordial_date[0] + '-' + primordial_date[1] + '/' + primordial_date[2]
        print(date_url_str)
        for i in range(2, 9):
            list_url = 'http://219.232.112.99/zgshb/html/' + date_url_str + '/node_{}.htm'.format(i)
            print(list_url)
            yield scrapy.Request(list_url, callback=self.parse,
                                 meta={'date_url_str': date_url_str, 'ctime': primordial_date})

    def parse(self, response):
        item = {}
        doc = pq(response.text)
        image_url = response.xpath('//*[@id="picMap"]//img/@src').extract_first().strip().replace('../', '')
        if 'http' not in image_url:
            image_url = 'http://219.232.112.99/zgshb/' + image_url
        else:
            image_url = image_url
        item['url'] = response.url
        item['mid'] = 4
        item['day'] = get_date2(int(time.time()))
        item['image_url'] = image_url
        item['plate'] = doc('.banst > STRONG').text()
        item['uuid'] = hashlib.md5(item['url'].encode("utf-8") + item['image_url'].encode("utf-8")).hexdigest()
        yield item
