# import scrapy
# from scraper_api import ScraperAPIClient
# from amazon_pro.items import AmazonProItem
# import math
# import re
# import logging

# client = ScraperAPIClient('b90c4dcc61e317892bb64c328c931de7')
# scraperAPI = False
# logging.basicConfig(filename='scraper_amazom.log', level=logging.ERROR)
# # logging.basicConfig(filename='scraper_amazom_critical.log', level=logging.CRITICAL)

# class ReviewSpider(scrapy.Spider):
#     name = 'review'
#     max_page_limit = 10 
#     total_review_re_pattern = r', (\d+(?:,\d+)*) with reviews'

#     def __init__(self, asin=None, *args, **kwargs):
#         super(ReviewSpider, self).__init__(*args, **kwargs)
#         self.asin =asin

#     def start_requests(self):
#         # asin_list = ['B00AM1Z67O', 'B00DJ4FMK2']
#         # for asin_number in asin_list:
#         print(self.asin)
#         # import pdb;pdb.set_trace
#         url = self.get_url(asin=self.asin)[0]
#         print(url)
#         if scraperAPI:
#             yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse, errback=self.handle_error)
#         else:
#             yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)

#     def parse(self, response):
#         try:
#             if response.status != 200:
#                 logging.critical(f"Request failed with status code: {response.status}")
#                 return
            
#             total_reviews_text = response.css('#filter-info-section .a-size-base::text').get()
#             total_reviews_text = total_reviews_text.strip()
#             matches = re.search(self.total_review_re_pattern, total_reviews_text)
#             asin_number = response.request.url.split("/")[4]
#             print(asin_number)

#             if matches:
#                 total_reviews = int(matches.group(1).replace(',', ''))
#             else:
#                 total_reviews = total_reviews_text.split(",")[1].split(" ")[1]
#             num_pages = math.ceil(total_reviews / 10)
            
#             if num_pages > self.max_page_limit:
#                 num_pages = 10

#             for page_number in range(2, num_pages + 2):
#                 page_urls = self.get_url(page_number, asin=self.asin, rating=True if num_pages>9 else False)
#                 for page_url in page_urls:
#                     if scraperAPI:
#                         yield scrapy.Request(client.scrapyGet(url=page_url), callback=self.parse_next_pages, errback=self.handle_error)
#                     else:
#                         yield scrapy.Request(url=page_url, callback=self.parse_next_pages, errback=self.handle_error)
            
#             reviews = response.css('[data-hook="review"]')

#             for single_r in reviews:
#                 item_obj = AmazonProItem()
#                 # title = single_r.css('.a-text-bold span::text')[1].get()
#                 # rating = single_r.css('.a-text-bold span::text')[0].get()
#                 title_elements = single_r.css('.a-text-bold span::text')
#                 if len(title_elements) >= 2:
#                     title = title_elements[1].get()
#                 else:
#                     title = ""

#                 if title_elements:
#                     rating = title_elements[0].get()
#                 else:
#                     rating = ""
#                 username = single_r.css('.a-profile-name::text').get()
#                 description = single_r.css('.review-text-content span::text').getall()
#                 date = single_r.css('.review-date::text').get()
#                 image_url = single_r.css('.review-image-tile::attr(src)').getall()
#                 product_url = response.request.url

#                 item_obj['title'] = title
#                 item_obj['rating'] = rating
#                 item_obj['username'] = username
#                 item_obj['description'] = description
#                 item_obj['date'] = date
#                 item_obj['asin_number'] =asin_number
#                 item_obj['image_urls'] = image_url
#                 item_obj['product_url'] = product_url

#                 yield item_obj
#         except Exception as e:
#             logging.critical(f"An error occurred in parsing: {str(e)}")

#     def get_url(self, asin=None,page_number=1, rating=False):
#         if rating:
#             number_words = ["two", "three", "four", "five"]
#             urls = []
#             for star in range(1, 5):  # Change range to include 5 stars
#                 star_word = number_words[star - 1]
#                 url = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?pageNumber={page_number}&filterByStar={star_word}_star"
#                 urls.append(url)
#             return urls
#         else:
#             return [f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?pageNumber={page_number}"]

#     def parse_next_pages(self, response):
#         try:
#             if response.status != 200:
#                 logging.critical(f"Request failed with status code: {response.status}")
#                 return
#             reviews = response.css('[data-hook="review"]')


#             for single_r in reviews:    
#                 item_obj = AmazonProItem()
#                 # title = single_r.css('.a-text-bold span::text')[1].get()
#                 # rating = single_r.css('.a-text-bold span::text')[0].get()
#                 title_elements = single_r.css('.a-text-bold span::text')
#                 if len(title_elements) >= 2:
#                     title = title_elements[1].get()
#                 else:
#                     title = ""

#                 if title_elements:
#                     rating = title_elements[0].get()
#                 else:
#                     rating = ""

#                 username = single_r.css('.a-profile-name::text').get()
#                 description = single_r.css('.review-text-content span::text').getall()
#                 date = single_r.css('.review-date::text').get()
#                 asin_number = response.request.url.split("/")[4]
#                 image_url = single_r.css('.review-image-tile::attr(src)').getall()
#                 product_url = response.request.url

#                 item_obj['title'] = title
#                 item_obj['rating'] = rating
#                 item_obj['username'] = username
#                 item_obj['description'] = description
#                 item_obj['date'] = date
#                 item_obj['asin_number'] =asin_number
#                 item_obj['image_urls'] = image_url
#                 item_obj['product_url'] = product_url

#                 yield item_obj
#         except Exception as e:
#             logging.error(f"An error occurred in parsing reviews: {str(e)}") 
        
#     def handle_error(self, failure):
#         request = failure.request
#         logging.critical(f"Request failed: {request.url}, Error: {failure.value}")



import scrapy
from scraper_api import ScraperAPIClient
from amazon_pro.items import AmazonProItem
import math
import re
import logging
from urllib import parse

client = ScraperAPIClient('b90c4dcc61e317892bb64c328c931de7')
scraperAPI = True
scraperDo = False
logging.basicConfig(filename='scraper_amazom_new.log', level=logging.ERROR)
# logging.basicConfig(filename='scraper_amazom_critical.log', level=logging.CRITICAL)

class ReviewSpider(scrapy.Spider):
    name = 'review'
    max_page_limit = 10 
    total_review_re_pattern = r', (\d+(?:,\d+)*) with reviews'

    def __init__(self, asin=None, *args, **kwargs):
        super(ReviewSpider, self).__init__(*args, **kwargs)
        self.asin =asin

    def start_requests(self):
        # asin_list = ['B00AM1Z67O', 'B00DJ4FMK2']
        # for asin_number in asin_list:
        print(self.asin)
        # import pdb;pdb.set_trace
        url = self.get_url()[0]
        print(url)
        if scraperAPI:
            yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse, errback=self.handle_error)
        elif scraperDo:
            target_url = parse.quote(url)
            new_url = f"http://api.scrape.do?token=9c69a1e877664a8791388922be4d0356e1d27cbae84&url={target_url}"
            yield scrapy.Request(url=new_url, callback=self.parse, errback=self.handle_error)
        else:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)

    def parse(self, response):
        try:
            if response.status != 200:
                logging.critical(f"Request failed with status code: {response.status}")
                return
            
            total_reviews_text = response.css('#filter-info-section .a-size-base::text').get()
            total_reviews_text = total_reviews_text.strip()
            matches = re.search(self.total_review_re_pattern, total_reviews_text)
            # asin_number = response.request.url.split("/")[4]
            # print(asin_number)

            if matches:
                total_reviews = int(matches.group(1).replace(',', ''))
            else:
                total_reviews = total_reviews_text.split(",")[1].split(" ")[1]
            num_pages = math.ceil(total_reviews / 10)
            
            if num_pages > self.max_page_limit:
                num_pages = 10

            for page_number in range(2, num_pages + 2):
                page_urls = self.get_url(page_number, rating=True if num_pages>9 else False)
                for page_url in page_urls:
                    if scraperAPI:
                        yield scrapy.Request(client.scrapyGet(url=page_url), callback=self.parse_next_pages, errback=self.handle_error)
                    elif scraperDo:
                        target_url = parse.quote(page_url)
                        new_url = f"http://api.scrape.do?token=9c69a1e877664a8791388922be4d0356e1d27cbae84&url={target_url}"
                        yield scrapy.Request(url=new_url, callback=self.parse, errback=self.handle_error)
                    else:
                        yield scrapy.Request(url=page_url, callback=self.parse_next_pages, errback=self.handle_error)
            
            reviews = response.css('[data-hook="review"]')

            for single_r in reviews:
                item_obj = AmazonProItem()
                # title = single_r.css('.a-text-bold span::text')[1].get()
                # rating = single_r.css('.a-text-bold span::text')[0].get()
                # title_elements = single_r.css('.a-text-bold span::text')
                # if len(title_elements) >= 2:
                #     title = title_elements[1].get()
                # else:
                #     title = ""

                # if title_elements:
                #     rating = title_elements[0].get()
                # else:
                #     rating = ""
                title = single_r.css('[data-hook="review-title"] > span::text').get()
                rating = single_r.css('.review-rating > span::text').get()
                username = single_r.css('.a-profile-name::text').get()
                description = single_r.css('.review-text-content span::text').getall()
                date = single_r.css('.review-date::text').get()
                image_url = single_r.css('.review-image-tile::attr(src)').getall()
                product_url = response.request.url

                item_obj['title'] = title
                item_obj['rating'] = rating
                item_obj['username'] = username
                item_obj['description'] = description
                item_obj['date'] = date
                item_obj['asin_number'] =self.asin
                item_obj['image_urls'] = image_url
                item_obj['product_url'] = product_url

                yield item_obj
        except Exception as e:
            logging.critical(f"An error occurred in parsing: {str(e)}")

    def get_url(self,page_number=1, rating=False):
        if rating:
            number_words = ["one","two", "three", "four", "five"]
            urls = []
            for star in range(1, 6):  # Change range to include 5 stars
                star_word = number_words[star - 1]
                url = f"https://www.amazon.com/product-reviews/{self.asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?pageNumber={page_number}&filterByStar={star_word}_star"
                urls.append(url)
            return urls
        else:
            return [f"https://www.amazon.com/product-reviews/{self.asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?pageNumber={page_number}"]

    def parse_next_pages(self, response):
        try:
            if response.status != 200:
                logging.critical(f"Request failed with status code: {response.status}")
                return
            reviews = response.css('[data-hook="review"]')


            for single_r in reviews:    
                item_obj = AmazonProItem()
                # title = single_r.css('.a-text-bold span::text')[1].get()
                # rating = single_r.css('.a-text-bold span::text')[0].get()
                # title_elements = single_r.css('.a-text-bold span::text')
                # if len(title_elements) >= 2:
                #     title = title_elements[1].get()
                # else:
                #     title = ""

                # if title_elements:
                #     rating = title_elements[0].get()
                # else:
                #     rating = ""
                title = single_r.css('[data-hook="review-title"] > span::text').get()
                rating = single_r.css('.review-rating > span::text').get()
                username = single_r.css('.a-profile-name::text').get()
                description = single_r.css('.review-text-content span::text').getall()
                date = single_r.css('.review-date::text').get()
                # asin_number = response.request.url.split("/")[4]
                image_url = single_r.css('.review-image-tile::attr(src)').getall()
                product_url = response.request.url

                item_obj['title'] = title
                item_obj['rating'] = rating
                item_obj['username'] = username
                item_obj['description'] = description
                item_obj['date'] = date
                item_obj['asin_number'] =self.asin
                item_obj['image_urls'] = image_url
                item_obj['product_url'] = product_url

                yield item_obj
        except Exception as e:
            logging.error(f"An error occurred in parsing reviews: {str(e)}") 
        
    def handle_error(self, failure):
        request = failure.request
        logging.critical(f"Request failed: {request.url}, Error: {failure.value}")
