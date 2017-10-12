import csv
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from datetime import datetime

class CookieSpider():
    def __init__(self):
        csvfile = open('cookies.csv', 'w', newline='')
        self.writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
        self.driver = webdriver.PhantomJS(os.path.join(os.path.dirname(__file__), 'bin/phantomjs'))
        self.driver.set_page_load_timeout(10)

    def scrape(self, urls):
        for url in urls:
            print('Processing: ' + url)
            try:
                result = {}
                self.driver.delete_all_cookies()
                self.driver.get(url)
                cookies = self.driver.get_cookies()
                if cookies:
                    for cookie in cookies:
                        result[cookie['name']] = cookie['value']
                self.writer.writerow([str(datetime.now()), url, result])
            except TimeoutException:
                print('- - Timeout exception at ' + url)

if __name__ == '__main__':
    import os
    if len(sys.argv) != 2:
        print('Please, specify path to file with urls')
        exit()
    urlsfile = sys.argv[1]
    if not os.path.exists(urlsfile):
        print('File not exists')
        exit()
    with open(urlsfile, newline='') as csvfile:
        reader = csv.reader(csvfile)
        urls = [row[-1] for row in reader]
        spider = CookieSpider()
        print('Scraping cookies started at: ' + str(datetime.now()))
        spider.scrape(urls)
        print('Scraping cookies finished at: ' + str(datetime.now()))
