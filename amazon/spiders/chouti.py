# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from scrapy.http.request import Request
from ..items import ChoutiItem
from scrapy.http.cookies import CookieJar
import json

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['http://dig.chouti.com']

    cookie_dict = {}  # 用作存储cookies
    has_urls_set = set() # 用作存储页码md5

    def parse(self, response):
        '''获取cookies并登录'''
        cookie_obj = CookieJar()
        cookie_obj.extract_cookies(response, response.request) 
        self.cookie_dict = cookie_obj._cookies  # 保存cookies

        yield Request(   # 发送POST请求并带上用户名密码cookies
            url = 'http://dig.chouti.com/login',
            method = 'POST',
            body = 'phone=用户名&&password=密码&&oneMonth=1',
            headers = {'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'},
            cookies = cookie_obj._cookies,
            callback = self.check_login
            )

    def check_login(self, response):
        '''检查登录结果'''
        result = json.loads(response.text)
        code = result['result']['code']
        # if code == '9999':
        #     print('登录成功。')
        yield Request(url='http://dig.chouti.com/', callback=self.dianzan)   # 回调给点赞函数
        # else:
        #     print('登录失败。', result['result']['message'])

    def dianzan(self, response):
        '''点赞及翻页'''
        doc = pq(response.text)
        id_list = doc('.part2').items()
        for id in id_list:
            link_id = id.attr('share-linkid')
            url = 'http://dig.chouti.com/link/vote?linksId=%s' % link_id  # 获取点赞链接
            yield Request(url=url, method='POST', cookies=self.cookie_dict, callback=self.show)  # 回调给查看结果函数

        page_list = doc('.ct_pagepa').items()   # 获取当前所有页码
        for a in page_list:
            uri = a.attr.href
            md5_url = self.md5(uri)
            if md5_url not in self.has_urls_set:  # url去重
                self.has_urls_set.add(md5_url)
                page_url = 'http://dig.chouti.com%s' % uri

                yield Request(url=page_url, callback=self.dianzan)   # 回调给自己翻页点赞

    def show(self, response):
        '''查看点赞结果'''
        print(response.text)

    def md5(self,url):
        '''用作url加密'''
        import hashlib
        obj = hashlib.md5()
        obj.update(bytes(url,encoding='utf-8'))

        return obj.hexdigest()