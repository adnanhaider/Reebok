import logging
import scrapy
import os
from scrapy import Spider
from scrapy.http import request
from Reebok.items import Manual


logger = logging.getLogger(__name__)

class Reebok(Spider):
    name = "reebok"
    start_urls = [
        "https://www.reebokfitness.info/support",
        "https://www.reebokfitness.info/support?lang=de",
        "https://www.reebokfitness.info/support?lang=es",
        "https://www.reebokfitness.info/support?lang=fr"
        ]

    def parse(self, response):
        urls = response.css('a._2wYm8::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.do_parse1)

    def do_parse1(self, response):
        url = response.css('a._2wYm8::attr(href)').get()
        yield scrapy.Request(url=url, callback=self.do_parse2)
    
    def do_parse2(self, response):
        product = response.css('._1ncY2 div._1Q9if p.font_8 *::text').getall()[-2]
        lang = response.css('html::attr(lang)').get()
        c_url = response.request.url
        ul = response.css('._1ozXL ._1vNJf')
        
        for li in ul:
            manual = Manual()      
            pdf = li.css('a._2wYm8::attr(href)').get()
            model = li.css('._1Q9if *::text').get()
            

            manual["product"] = product
            manual["brand"] = 'Reebok'
            manual["thumb"] = ''
            # print(len(product.strip().split(' ')), '======' , pdf)
            if int(len(product.strip().split(' '))) - 1:
                for element in product.strip().split(' '):
                    if element in model:
                        model = model.replace(element, '').strip()
                    
            elif product in model:
                model = model.replace(product, '').strip()
            if not model:
                model = li.css('._1Q9if span *::text').get()
            manual['model'] = " ".join(model.split())
            manual["source"] = 'reebokfitness.info'
            manual["file_urls"] = pdf
            manual["url"] = c_url
            manual["type"] = 'Manual'
            manual["product_lang"] = lang

            # if 'en' in lang:
            #     manual["product_lang"] =  lang 
            # else:
            #     manual["product_lang"] = ''

            yield manual
   