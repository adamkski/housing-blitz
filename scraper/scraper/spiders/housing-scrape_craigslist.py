import scrapy

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    start_urls = ["https://ottawa.craigslist.org/d/apartments-housing-for-rent/search/apa"]

    def parse(self, response):
        ad_links = response.css('p.result-info a::attr(href)').re("https://ottawa.craigslist.org/apa.*")
        yield from response.follow_all(ad_links, self.parse_ad)

        next_page = response.css('a.next').get() 
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_ad(self, response):
        attrs = []
        for attr in response.css('div.mapAndAttrs span'):
            attrs.append(''.join(attr.css('::text').getall()))

        yield {
            'web_link': response.request.url,
            'building_location': response.css('div.mapaddress::text').get(),
            'building_location_link': response.css('p.mapaddress a::attr(href)').get(),
            'building_type': response.css('span.housing::text').get(),
            'price': response.css('span.price::text').get(),
            'date_posted': response.css('time.timeago::attr(datetime)').get(),
            'rental_attr': attrs,
            'neighbourhood': response.css('span.postingtitletext small::text').get().strip(),
            'raw_description': ''.join(response.css('section#postingbody::text').getall()).strip()
        }

