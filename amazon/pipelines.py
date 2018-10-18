# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class AmazonPipeline(object):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     '''初始化时用于创建pipiline对象'''
    #     filename = crawler.settings.get('FILENAME')  # 读取settings.py中的配置，并获取变量（settings中变量名必须大写）
    #     return cls(filename)

    def open_spider(self, spider):
        '''爬虫开始执行时调用'''
        self.f = open('test.json','a')

    def close_spider(self, spider):
        '''爬虫关闭时调用'''
        self.f.close()

    def process_item(self, item, spider):
        print(spider,item)  # spider对象代表是哪个爬虫交给的，item为爬虫传递过来的实体
        tpl = '%s\n%s\n\n' % (item['title'], item['href'])
        self.f.write(tpl)

        return item    # 交给下一个pipeline处理；当有多个pipeline时，爬虫传递过来的item会经过每个pipeline处理
      #  raise DropItem()  # 丢弃item不交给其它pipeline处理，也可通过获取spider对象中的爬虫名称进行判断分别处理
