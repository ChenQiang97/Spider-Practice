# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    # 自动调用,解析爬取到的内容
    def parse(self, response):
        quotes = response.css(".quote")
        for quote in quotes:
            item = QuoteItem()
            # .text::text  选定标签内文本内容
            text = quote.css(".text::text").extract_first()
            author = quote.css(".author::text").extract_first()
            # 多条内容
            tags = quote.css(".tags .tag::text").extract()
            item["text"] = text
            item["author"] = author
            item["tags"] = tags
            yield item

        # 下一页url
        next = response.css(".pager .next a::attr(href)").extract_first()
        # 拼接
        url = response.urljoin(next)
        # 自身回调
        yield scrapy.Request(url, callback=self.parse)
