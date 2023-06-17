import scrapy
from scraper_api import ScraperAPIClient
from ..items import AmazonProItem
client = ScraperAPIClient('40064940d9878bb50ac9811151fe2cb4')
scraperAPI=True


class reviewSpider(scrapy.Spider):
    name = 'review'
    # start_urls='https://www.amazon.in/product-reviews/B09GB5B4BK/'


    def start_requests(self):
        url = ['https://www.amazon.in/product-reviews/B09GB5B4BK/',
               'https://www.amazon.in/product-reviews/B09GB5B4BK/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=2',
               'https://www.amazon.in/product-reviews/B09GB5B4BK/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=3',
               'https://www.amazon.in/product-reviews/B09GB5B4BK/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=4'

               ]
        for i in url:
            yield scrapy.Request(client.scrapyGet(url=i), callback=self.parse)

    

    def parse(self, response):

        

        for single_r in response.css('[data-hook="review"]'):
            item_obj=AmazonProItem()
            title = single_r.css('.a-text-bold span::text')[1].extract()
            rating = single_r.css('.a-text-bold span::text')[0].extract()
            username = single_r.css('.a-profile-name::text')[0].extract()
            description = single_r.css('.review-text-content span::text').extract()
            date = single_r.css('.review-date::text')[0].extract()

           
            item_obj['title'] = title
            item_obj['rating'] = rating
            item_obj['username'] = username
            item_obj['description'] = description
            item_obj['date'] = date
            
            
            yield item_obj
        
        next_page = response.css('li.a-last a::attr(href)').get()
        # next_page='https://www.amazon.in/product-reviews/B09GB5B4BK/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=2'
        print(f"--------------{next_page}")
        
        

        # if next_page is not None:
        #     print("inside if------------------------------")
        #     yield scrapy.Request(response.urljoin(next_page))


        # next_page = response.xpath('//a[text()="Next page"]/@href').get()

        # # next_page = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a/@href').get()
        # if next_page:
        #         if scraperAPI:
        #             yield scrapy.Request(client.scrapyGet(response.urljoin(next_page)), callback=self.parse)
        #         else:
        #             next_page = 'http://www.amazon.com'+next_page
        #             yield scrapy.Request(next_page)



     

        
        # if next_page:
        #     yield scrapy.Request(next_page)

        # next_page = response.xpath('//a[contains(text(),"Next page")]/@href').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

