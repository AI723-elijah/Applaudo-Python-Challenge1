# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ApplaudoNikeSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ApplaudoNikeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from selenium import webdriver
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from scrapy.http import HtmlResponse
from logging import getLogger
class SeleniumDownloaderMiddleware(object):
    def __init__(self, timeout=None, chrome_options=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        options = Options()
        
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_driver_binary = r"C:\Program Files\chromedriver.exe"
        
        for o in chrome_options or ():
            options.add_argument(o)
        self.browser = webdriver.Chrome(chrome_options=options , executable_path=chrome_driver_binary)
        self.browser.set_window_size(1920, 1080)
        self.browser.set_page_load_timeout(timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.actions = ActionChains(self.browser)

    def __del__(self):
        self.browser.quit()

    def process_request(self, request, spider):
        if request.url.endswith('jpg'):
            return None
        self.logger.debug('Chrome is starting')
        self.browser.get(request.url)
        self.actions.send_keys(Keys.END)
        self.actions.send_keys(Keys.END)
        self.actions.perform()
        time.sleep(1)
        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, status=200, encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
            chrome_options=crawler.settings.get('CHROME_OPTIONS'),
        )
