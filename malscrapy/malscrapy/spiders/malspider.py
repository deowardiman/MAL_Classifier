import scrapy
# from scrapy.contrib.spiders import Rule, Crawlspider
from malscrapy.items import MalscrapyItem


class MalspiderSpider(scrapy.Spider):
    name = 'malspider'
    # allowed_domains = ['https://myanimelist.net/topanime.php']
    start_urls = ['http://myanimelist.net/topanime.php/']        
    
    # for i in range (50,101,50):
    for i in range (50,11751,50):
        start_urls.append('http://myanimelist.net/topanime.php?limit='+str(i)+'')                
        
    def parse(self, response):
        for href in response.xpath('//h3[@class="hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"]/a/@href'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)         
        
    def parse_dir_contents(self,response):
        item = MalscrapyItem()
        
        item['title'] = response.xpath('//h1[@class="title-name h1_bold_none"]/strong/text()').extract()
        item['rating']= response.xpath('//div[@class="fl-l score"]/div/text()').extract()
        item['ranking']= response.xpath('//span[@class="numbers ranked"]/strong/text()').extract()
        item['season'] = response.xpath('//span[@class="information season"]/a/text()').extract()
        item['misc'] = ";".join(response.xpath('//span[@itemprop="genre"]/text()').extract()).strip()
        relative_img_urls = response.xpath('//td[@class="borderClass"]/div/div/a/img/@data-src').extract()
        item['image_urls'] = self.url_join(relative_img_urls, response)
        item['description'] = response.xpath('//p[@itemprop="description"]/text()').extract()
        yield item

    def url_join(self, urls, response):
        joined_urls = []
        for url in urls:
            joined_urls.append(response.urljoin(url))
        return joined_urls
        
        
        
        # for item in zip(title, rating, ranking):
        #     scraped_data= {
        #         'title': item[0],
        #         'rating': item[1],
        #         'ranking': item[2]}
        
        #     yield scraped_data
