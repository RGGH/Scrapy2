import scrapy
from items import ImdbItem
from scrapy.crawler import CrawlerProcess

class ImdbSpider(scrapy.Spider):
	name = 'imdbspider'
	allowed_domains = ['imdb.com']
	start_urls = ['http://www.imdb.com/chart/top']

	custom_settings = {'FEED_FORMAT':'csv','FEED_URI':'IMDB.csv'}

	### def start_requests(self):
    	### The default implementation generates Request(url, dont_filter=True) for each url in start_urls 

	def parse(self,response):
		for href in response.css("td.titleColumn a::attr(href)").getall():
			yield response.follow(url=href,callback=self.parse_movie)

	def parse_movie(self, response):
		item = ImdbItem()
		item['title'] = [ x.replace('\xa0', '')  for x in response.css(".title_wrapper h1::text").getall()][0]
		item['directors'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Director")]/following-sibling::a/text()').getall()
		item['writers'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Writers")]/following-sibling::a/text()').getall()
		item['stars'] = response.xpath('//div[@class="credit_summary_item"]/h4[contains(., "Stars")]/following-sibling::a/text()').getall()
		item['popularity'] = response.css(".titleReviewBarSubItem span.subText::text")[2].re('([0-9]+)')
		item['rating'] = response.css(".ratingValue span::text").get()
		return item

# Code to make script run like normal Python script 
process = CrawlerProcess()
process.crawl(ImdbSpider)
process.start() # the script will block here untill the crawling is finished

