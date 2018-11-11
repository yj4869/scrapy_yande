# -*- coding: utf-8 -*-
import scrapy
from yande.items import YandeItem


class YandesSpider(scrapy.Spider):
    name = 'yandes'
    #allowed_domains = ['https://yande.re']
    url = 'https://yande.re/post?page='
    #初始页数
    offset = 1
    #标签页下的图片，这里默认选择了监督的图，建议现在网站上找到对应标签再修改等号后的标签名
    #若只需爬取首页的图片，可以置空tags的内容
    tags = '&tags=kantoku'
    start_urls = [url+str(offset)+tags]

    def parse(self, response):
        for each in response.xpath('//ul/li'):
            #避免爬取大量空白信息
            if len(each.xpath('./a[@class="directlink largeimg"]/@href').extract())>0:
                item = YandeItem()
                item['imgno'] = each.xpath('./@id').extract_first()
                #如此命名为了保证和图片下载模块中的默认url名一致
                item['image_urls'] = each.xpath('./a[@class="directlink largeimg"]/@href').extract()
                item['imgsize'] = each.xpath('./a/span[@class="directlink-res"]/text()').extract_first()
                item['imginfo'] = each.xpath('./div/a/img/@title').extract_first()
                yield item

        if self.offset<1:
            #yande外站链接较慢，尤其是下载跟不上进度，只建议每次爬取1页。若不需下载可尝试多页
            self.offset +=1

        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)