import scrapy
from scraper_api import ScraperAPIClient
from amazon_pro.items import AmazonProItem
import math
import re
import logging

client = ScraperAPIClient('b90c4dcc61e317892bb64c328c931de7')
scraperAPI = False
logging.basicConfig(filename='scraper_amazom.log', level=logging.ERROR)
# logging.basicConfig(filename='scraper_amazom_critical.log', level=logging.CRITICAL)

class ReviewSpider(scrapy.Spider):
    name = 'review'
    max_page_limit = 10 
    total_review_re_pattern = r', (\d+(?:,\d+)*) with reviews'

    def start_requests(self):
        asin_list = ['B00AM1Z67O', 'B00DJ4FMK2']
        for asin_number in asin_list:
            print(asin_number)
            # import pdb;pdb.set_trace
            url = self.get_url(asin=asin_number)[0]
            print(url)
            if scraperAPI:
                yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse, errback=self.handle_error)
            else:
                yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error, meta={'asin': asin_number})

    def parse(self, response):
        try:
            if response.status != 200:
                logging.critical(f"Request failed with status code: {response.status}")
                return
            
            total_reviews_text = response.css('#filter-info-section .a-size-base::text').get()
            total_reviews_text = total_reviews_text.strip()
            matches = re.search(self.total_review_re_pattern, total_reviews_text)
            asin_number = response.request.url.split("/")[4]
            print(asin_number)

            if matches:
                total_reviews = int(matches.group(1).replace(',', ''))
            else:
                total_reviews = total_reviews_text.split(",")[1].split(" ")[1]
            num_pages = math.ceil(total_reviews / 10)
            
            if num_pages > self.max_page_limit:
                num_pages = 10

            for page_number in range(2, num_pages + 2):
                page_urls = self.get_url(page_number, asin=asin_number, rating=True if num_pages>9 else False)
                for page_url in page_urls:
                    if scraperAPI:
                        yield scrapy.Request(client.scrapyGet(url=page_url), callback=self.parse_next_pages, errback=self.handle_error)
                    else:
                        yield scrapy.Request(url=page_url, callback=self.parse_next_pages, errback=self.handle_error, meta={'asin': asin_number, 'page_number': page_number})
            
            reviews = response.css('[data-hook="review"]')

            for single_r in reviews:
                item_obj = AmazonProItem()
                # title = single_r.css('.a-text-bold span::text')[1].get()
                # rating = single_r.css('.a-text-bold span::text')[0].get()
                title_elements = single_r.css('.a-text-bold span::text')
                if len(title_elements) >= 2:
                    title = title_elements[1].get()
                else:
                    title = ""

                if title_elements:
                    rating = title_elements[0].get()
                else:
                    rating = ""
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
                item_obj['asin_number'] =asin_number
                item_obj['image_urls'] = image_url
                item_obj['product_url'] = product_url

                yield item_obj
        except Exception as e:
            logging.critical(f"An error occurred in parsing: {str(e)}")

    def get_url(self, asin=None,page_number=1, rating=False):
        if rating:
            number_words = ["two", "three", "four", "five"]
            urls = []
            for star in range(1, 5):  # Change range to include 5 stars
                star_word = number_words[star - 1]
                url = f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?pageNumber={page_number}&filterByStar={star_word}_star"
                urls.append(url)
            return urls
        else:
            return [f"https://www.amazon.in/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?pageNumber={page_number}"]

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
                title_elements = single_r.css('.a-text-bold span::text')
                if len(title_elements) >= 2:
                    title = title_elements[1].get()
                else:
                    title = ""

                if title_elements:
                    rating = title_elements[0].get()
                else:
                    rating = ""

                username = single_r.css('.a-profile-name::text').get()
                description = single_r.css('.review-text-content span::text').getall()
                date = single_r.css('.review-date::text').get()
                asin_number = response.request.url.split("/")[4]
                image_url = single_r.css('.review-image-tile::attr(src)').getall()
                product_url = response.request.url

                item_obj['title'] = title
                item_obj['rating'] = rating
                item_obj['username'] = username
                item_obj['description'] = description
                item_obj['date'] = date
                item_obj['asin_number'] =asin_number
                item_obj['image_urls'] = image_url
                item_obj['product_url'] = product_url

                yield item_obj
        except Exception as e:
            logging.error(f"An error occurred in parsing reviews: {str(e)}") 
        
    def handle_error(self, failure):
        request = failure.request
        logging.critical(f"Request failed: {request.url}, Error: {failure.value}")
