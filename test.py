import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.selector import Selector

class ErrbackSpider(scrapy.Spider):
    name = "errback_example"
    start_urls = [

        'https://www.liveyoursport.com/heart-rate-monitors-1/',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=2',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=3',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=4',
        # "http://www.httpbin.org/",              # HTTP 200 expected
        # "http://www.httpbin.org/status/404",    # Not found error
        # "http://www.httpbin.org/status/500",    # server issue
        # "http://www.httpbin.org:12345/",        # non-responding host, timeout expected
        # "http://www.httphttpbinbin.org/",       # DNS error expected
    ]

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin,
                                    )

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))

        a=Selector(response).xpath('//em/text()').extract()
        yield {'a':a}
        # do something useful here...
