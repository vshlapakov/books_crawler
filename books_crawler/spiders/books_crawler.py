# -*- coding: utf-8 -*-
import scrapy

class BooksToScrapeSpider(scrapy.Spider):
    name = 'books-toscraps'
    allowed_domains = ['toscrape.com']
    start_urls = [
        'http://books.toscrape.com',
    ]

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'HTTPCACHE_ENABLED': True,
    }

    def parse(self, response):
        for category in response.css('div.side_categories > ul > li > ul > li'):
            category_href = category.css('a::attr(href)').extract_first()
            yield response.follow(category_href, self.parse_category_books)

    def parse_category_books(self, response):
        for books in response.css('article.product_pod'):
            yield {
                # Used title rather than text because some book's text had ellipsis
                'book title': books.css('h3 > a::attr(title)').extract_first(),
                'book price': books.css('p.price_color::text').extract_first(),
                # Used response.urljoin to make absolute URL
                'book image URL': response.urljoin(books.css('div.image_container > a > img::attr(src)').extract_first()),
                'book details page URL': response.urljoin(books.css('div.image_container > a::attr(href)').extract_first())
            }

        for next_href in response.xpath('//li/a[text()="next"]'):
            yield response.follow(next_href, self.parse_category_books)
            