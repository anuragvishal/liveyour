import scrapy
from scrapy.selector import Selector
# from scrapy.http.request import Request

class ProductsSpider(scrapy.Spider):
    name = "productsspider"
    start_urls = [
        'https://www.liveyoursport.com/heart-rate-monitors-1/',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=2',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=3',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=4',
    ]

    def parse(self, response):
        for product in response.css('ul.ProductList li'):
            desc_url = product.css('div.ProductDetails a::attr(href)').extract_first()

            data = {
                'product_name': product.css('div.ProductDetails a::text').extract_first(),
                'price': product.css('em::text').extract_first(),
                'product_url': product.css('div.ProductImage a::attr(href)').extract()
                }
            request = scrapy.Request(desc_url, callback=self.parseDescription,)
            request.meta['item']= data
            yield request

    def parseDescription(self, response):
        description = response.css('span.prod-descr::text').extract_first()
        data = response.meta['item']
        data['description']=description
        yield data
