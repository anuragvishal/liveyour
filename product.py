import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://www.liveyoursport.com/heart-rate-monitors-1/',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=2',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=3',
        'https://www.liveyoursport.com/heart-rate-monitors-1/?page=4',
    ]

    def parse(self, response):
        for product in response.css('ul.ProductList li'):
            desc_url = product.css('div.ProductDetails a::attr(href)').extract_first();
            yield {
                'product_name': product.css('div.ProductDetails a::text').extract_first(),
                'price': product.css('em::text').extract_first(),
                'product_url': product.css('div.ProductImage a::attr(href)').extract(),
                'description': response.follow(desc_url, callback=self.parseDescription)

            }

    def parseDescription(self, response):
        #print response
        item = response.css('span::text').extract()
        yield item
