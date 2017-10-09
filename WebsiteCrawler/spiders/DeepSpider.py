import sys
import datetime
import scrapy
import csv
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess

if len(sys.argv) != 3:
    print('Please, specify filename with PROJECT NAME and URL as first parameter and MAX DEPTH as second parameter')
    exit()

class DeepSpider(scrapy.Spider):
    name = 'spider'
    dumper = csv.writer(open('result.csv', 'a'))

    custom_settings = {
        'DEPTH_LIMIT': int(sys.argv[2])
    }

    found_urls = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.urls = [self.MAIN_URL]
        self.domain = urlparse(self.urls[0]).netloc
        self.linkExtractor = LinkExtractor(allow_domains=self.domain, unique=True)
        self.dumper.writerow([self.PROJECT_NAME, datetime.datetime.now(), self.urls[0]])
        print(self.urls[0] + '------------------------')


    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse,
                                 dont_filter=True)


    def parse(self, response):
        if(response.status != 200):
            return
        new_urls = []
        for link in self.linkExtractor.extract_links(response):
            if link.url not in self.found_urls:
                new_urls.append(link.url)
                self.write(link.url)
        self.found_urls += new_urls
        print('New urls: ' + str(len(new_urls)))
        for url in new_urls:
            yield scrapy.Request(url, callback=self.parse)


    def write(self, url):
        self.dumper.writerow([self.PROJECT_NAME, datetime.datetime.now(), url])


def main():
    import os

    if os.path.exists(sys.argv[1]):
        filename = sys.argv[1]
        PROJECT_NAME, MAIN_URL  = open(filename, 'r').read().split(',')
        PROJECT_NAME, MAIN_URL = PROJECT_NAME.strip(), MAIN_URL.strip()
        DEPTH_LIMIT = int(sys.argv[2])

        print('Your url: ' + MAIN_URL)
        print('Your project name: ' + PROJECT_NAME)
        print('Your depth: ' + str(DEPTH_LIMIT))

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        })

        process.crawl(DeepSpider, MAIN_URL = MAIN_URL, PROJECT_NAME = PROJECT_NAME)
        process.start()

if __name__ == '__main__':
    main()