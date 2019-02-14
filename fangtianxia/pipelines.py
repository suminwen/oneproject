# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
class FangtianxiaPipeline(object):
    def __init__(self):
        self.newhouse = open('newhouse.json','wb')
        self.esfhouse = open('esfhouse.json','wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse,ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse,ensure_ascii=False)

    def process_item(self, item, spider):
        self.newhouse_exporter.export_item(item)
        self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.newhouse.close()
        self.esfhouse.close()
