import scrapy

from pep_parse.items import PepParseItem
# scrapy startproject pep_parse .
# scrapy genspider pep peps.python.org
# scrapy crawl pep
# scrapy shell "http://peps.python.org/"


# В первый файл нужно вывести список всех PEP: номер, название и статус.


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['http://peps.python.org/']

    def parse(self, response):
        rows = response.css('section#numerical-index tbody tr')
        for row in rows:
            data = {
                'status': row.css('td::text').get()[1:],
                'number': row.css('td + td a::text').get(),
                'name': row.css('td + td + td a::text').get(),
            }
            yield PepParseItem(data)
