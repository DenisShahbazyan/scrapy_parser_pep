import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        rows = response.css('section#numerical-index tbody tr')
        for row in rows:
            next_link = row.css('td a::attr(href)').get()
            if next_link is not None:
                yield response.follow(next_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'status': response.css('dt:contains("Status") + dd::text').get(),
            'number': response.css('h1.page-title::text').get().split()[1],
            'name': response.css(
                'h1.page-title::text'
            ).get().split('–')[-1].strip(),
        }
        yield PepParseItem(data)
