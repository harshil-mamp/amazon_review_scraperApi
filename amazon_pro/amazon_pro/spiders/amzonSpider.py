import scrapy
from scraper_api import ScraperAPIClient
client = ScraperAPIClient('40064940d9878bb50ac9811151fe2cb4')
scraperAPI=True
class reviewSpider(scrapy.Spider):
    name = 'review'


    def start_requests(self):
        url = 'https://www.amazon.in/product-reviews/B09GB5B4BK/'
        yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse)

    def parse(self, response):
        for single_r in response.css('[data-hook="review"]'):
            title = single_r.css('.a-text-bold span::text')[1].extract()
            rating = single_r.css('.a-text-bold span::text')[0].extract()
            username = single_r.css('.a-profile-name::text')[0].extract()
            description = single_r.css('.review-text-content span::text')[0].extract()
            date = single_r.css('.review-date::text')[0].extract()

            item = {
                'title': title,
                'rating': rating,
                'username': username,
                'description': description,
                'date': date
            }
            yield item

        next_page = response.css('li.a-last a::attr(href)').get()
        # print(f"----------------{next_page}")
        # if next_page:
        #     yield scrapy.Request(next_page)
        # next_page = response.xpath('//a[contains(text(),"Next page")]/@href').get()
        print(f"--------------{next_page}")
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)
        if next_page:
            if scraperAPI:
                yield scrapy.Request(client.scrapyGet(response.urljoin(next_page)), callback=self.parse)
            else:
                next_page = 'http://www.amazon.com' + next_page
                yield scrapy.Request(next_page)

