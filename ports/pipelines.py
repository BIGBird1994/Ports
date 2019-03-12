# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import urllib.parse

class PortsPipeline(object):
    def __init__(self):
        super().__init__()
        username = urllib.parse.quote_plus('ports')
        password = urllib.parse.quote_plus('123456')
        conn = MongoClient(host='mongodb://%s:%s@120.133.26.190' % (username, password), port=2000)
        self.col = conn['raw_data']['ports_detail']
    
    def process_item(self, item, spider):
        try:
            self.col.insert(dict(item))
            return item
        except Exception as e:
            print(e)
