# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class AmazonProPipeline:
#     def process_item(self, item, spider):
#         return item

import csv

class AmazonCSVExportPipeline:
    def open_spider(self, spider):
        self.csv_files = {}  # To store CSV file handlers

    def close_spider(self, spider):
        for asin, csv_file in self.csv_files.items():
            csv_file.close()

    def process_item(self, item, spider):
        asin = item['asin_number'] 
        if asin not in self.csv_files:
            filename = f"{asin}.csv"
            csv_file = open(filename, 'w', newline='', encoding='utf-8')
            fieldnames = ['title', 'rating', 'username', 'description', 'date', 'image_urls', 'asin_number']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            self.csv_files[asin] = (csv_file, writer)

        csv_file, writer = self.csv_files[asin]
        writer.writerow({
            'title': item['title'],
            'rating': item['rating'],
            'username': item['username'],
            'description': '\n'.join(item['description']),
            'date': item['date'],
            'image_urls': '\n'.join(item['image_urls']),
        })
        
        return item

