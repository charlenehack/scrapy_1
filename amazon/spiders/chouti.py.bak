# -*- coding: utf-8 -*-
import scrapy
import sys,io
from pyquery import PyQuery as pq
from scrapy.http.request import Request
from ..items import ChoutiItem

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['http://dig.chouti.com']

    has_urls_set = set()

    def parse(self, response):
        #content = str(response.body,encoding='utf-8')
        content = response.body.decode('utf-8')
        doc = pq(content)
        show_content = doc('.show-content.color-chag').items()  # 获取所有文章标题及链接
        for s in show_content:
            title = s.text()
            href = s.attr.href

            item_obj = ChoutiItem(title=title, href=href)
            yield item_obj   # 将item对象传递给pipeline

        page_list = doc('.ct_pagepa').items()   # 获取当前所有页码
        for a in page_list:
            uri = a.attr.href
            md5_url = self.md5(uri)
            if md5_url not in self.has_urls_set:  # url去重
                self.has_urls_set.add(md5_url)
                page_url = 'http://dig.chouti.com%s' % uri
                #print(page_url)

                obj = Request(url=page_url, callback=self.parse)
                yield obj   # 将新要访问的url添加到调度器

    def md5(self,url):
        '''用作url加密'''
        import hashlib
        obj = hashlib.md5()
        obj.update(bytes(url,encoding='utf-8'))

        return obj.hexdigest()