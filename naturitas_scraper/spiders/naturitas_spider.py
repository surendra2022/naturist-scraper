import scrapy


class NaturitasSpiderSpider(scrapy.Spider):
    name = 'naturitas_spider'
    allowed_domains = ['naturitas.es']
    start_urls = ['https://www.naturitas.es/c/suplementos]

    def parse(self, response):
        product_links = response.css('a.product-item-link::attr(href)').extract()

        for product_link in product_links:
            yield scrapy.Request(product_link, callback=self.parse_product)
        load_more = response.css('a#load-more-product-link::attr(href)').extract_first()
        if load_more:
            original_url = response.meta.get('original_url', response.url)
            page_number = response.meta.get('page_number', 1)
            page_number += 1
            url = original_url+ f'?&p={page_number}'
            yield scrapy.Request(url, callback=self.parse, meta={'page_number': page_number, 'original_url': original_url}, dont_filter=True)
    
    def parse_product(self, response):
        product_name = response.css('h1 span::text').extract_first()
        product_link = response.url
        product_brand = response.css('div.product-brand a::text').extract_first().strip() if response.css('div.product-brand a::text').extract_first() else ''
        product_format = response.css('div.product__presentation::text').extract_first().strip()
        product_rating = response.css('div.product-reviews-summary-rating::attr(title)').extract_first()
        product_summary = response.css('a.product-reviews-summary-link::text').extract_first().strip() if response.css('a.product-reviews-summary-link::text').extract_first() else ''
        
        yield {
            'product_name': product_name,
            'product_link': product_link,
            'product_brand': product_brand,
            'product_format': product_format,
            'product_rating': product_rating,
            'product_summary': product_summary
        }
       
