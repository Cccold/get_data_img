# -*- coding:utf-8 -*-
import datetime
import hashlib
import re
import time
import uuid
import hashlib
import scrapy
from lxml.html import fromstring
from pyquery import PyQuery as pq
from ..items import GetImgSpidersItem
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Cookie': 'JSESSIONID=553F6D8B21411E4A9D427AE8A27C172D',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    # 'Referer': 'http://124.207.49.121/pc/page.do?pName=zghgb&pDate=20200909',
}


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
class CnHuagongbaoImgSpider(scrapy.Spider):
    name = 'CN_HuaGongbao_img'
    allowed_domains = ['http://124.207.49.121', '124.207.49.121']
    start_urls = []
    def start_requests(self):
        primordial_date = get_date2(int(time.time())).replace('-', '')
        url = 'http://124.207.49.121/pc/page.do?pName=zghgb&pDate=' + primordial_date
       # url = 'http://124.207.49.121/pc/page.do?pName=zghgb&pDate=20200921'
        yield scrapy.Request(url, callback=self.parse, headers=headers)

    def parse(self, response, **kwargs):
        li_list = response.xpath('//*[@id="page_list_context"]/ul/li')
        for li in li_list:
            y_url = li.xpath('.//a/@href').extract_first()
            if y_url:
                list_url = 'http://124.207.49.121/' + y_url
                subname = li.xpath('.//a/text()').extract_first().strip()
                yield scrapy.Request(list_url, callback=self.get_detail_url, meta={'subname': subname})

    def get_detail_url(self, response):
        doc = pq(response.text)
        item = {}
        item['mid'] = 5
        item['url'] = response.url
        item['image_url'] = response.xpath('//*[@id="img_box"]//img/@src').extract_first()
        item['uuid'] = hashlib.md5(item['url'].encode("utf-8") + item['image_url'].encode("utf-8")).hexdigest()
        item['day'] =  get_date2(int(time.time()))
        item['plate'] = doc('title').text()
        yield item
