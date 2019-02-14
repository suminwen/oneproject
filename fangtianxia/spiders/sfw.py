# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia.items import NewHouseItem
from fangtianxia.items import EsfHouseItem

class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.html']

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province = province_text
            if province_text =='其它':
                continue
            city_td = tds[1]
            city_links = city_td.xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                city_url = city_link.xpath('.//@href').get()
                #构建新房的URL
                new_url = city_url.split('//')
                scheme = new_url[0]
                domin = new_url[1]
                if 'bj' in domin:
                    newhouse_url = 'http://newhouse.fang.com/house/s/'
                    esf_url = 'http://esf.fang.com/'
                else:
                    newhouse_url = scheme + '//' +"newhouse." + domin +"house/s/"
                    #构建二手房的URL
                    esf_url = scheme + '//' + "esf." + domin
                # print("城市：%s %s" %(province,city))
                # print("新房url：%s" %newhouse_url)
                # print("二手房url：%s" %esf_url)

                yield scrapy.Request(url=newhouse_url,callback=self.parse_newhouse,meta={"info":(province,city)})
                yield scrapy.Request(url=esf_url,callback= self.parse_esf,meta={"info":(province,city)})

    def parse_newhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath('//div[contains(@class,"nl_con")]/ul/li')
        for li in lis:
            name1 = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            if name1 :
                name = name1.strip()
            house_type_list = li.xpath('.//div[contains(@class,"house_type")]/a/text()').getall()
            roows = "".join( list(filter(lambda x:x.endswith("居"),house_type_list)))
            area = "".join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())
            area = re.sub(r'\s|/|－','',area)
            address = li.xpath('.//div[@class="address"]/a/@title').get()
            district_text = "".join(li.xpath('.//div[@class="address"]/a//text()').getall())
            # district = re.sub(r'\s','',district)
            if district_text:
                district_text = re.search(r'.*\[(.+)\].*',district_text).group(1)
            district = district_text
            sale = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            price = "".join(li.xpath('.//div[@class="nhouse_price"]//text()').getall())
            price = re.sub(r'\s','',price)
            origin_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
            item = NewHouseItem(province=province,city=city,name=name,roows= roows,area=area,address=address,district=district,sale=sale,price=price,origin_url=origin_url)
            yield item
        next_url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(url= response.urljoin(next_url),callback= self.parse_newhouse,meta={'info':(province,city)})

    def parse_esf(self,response):
        province,city = response.meta.get('info')
        dls = response.xpath('//div[@class="shop_list shop_list_4"]/dl')
        for dl in dls:
            item = EsfHouseItem(province=province,city=city)
            name = dl.xpath('.//p[@class="add_shop"]/a/text()').get()
            if name:
                name = re.sub(r'\s',"",name)
            item['name'] = name
            infos = dl.xpath('.//p[@class="tel_shop"]//text()').getall()
            infos = list(map(lambda x:re.sub(r'\s','',x),infos))
            for info in infos:
                if "厅" in info:
                    item['rooms'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['toward'] = info
                elif "年" in info:
                    item['year'] = info
                elif "㎡" in info:
                    item['area'] = info
            item['address'] =dl.xpath('.//p[@class="add_shop"]/span/text()').get()
            item['price'] ="".join( dl.xpath('.//span[@class="red"]//text()').getall())
            item['unit'] = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').get()
            datal_url = dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
            item['origin_url'] = response.urljoin(datal_url)
            yield item
        next_url = response.xpath('//div[@class="page_al"]/p[-2]/a/@href').get()
        if next_url:
            yield scrapy.Request(url= response.urljoin(next_url),callback= self.parse_esf,meta={'info':(province,city)})





