import scrapy

from scrapy.loader import ItemLoader

from ..items import RaiffeisenhuItem
from itemloaders.processors import TakeFirst

base = 'https://www.raiffeisen.hu/hasznos/hirek?p_p_id=1_WAR_wtjournalcontentdisplayportlet_INSTANCE_GDEKUmSJfYT4&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=pagination&p_p_cacheability=cacheLevelPage&p_p_col_id=column-3&p_p_col_pos=2&p_p_col_count=3&_1_WAR_wtjournalcontentdisplayportlet_INSTANCE_GDEKUmSJfYT4_entryEnd=10000&_1_WAR_wtjournalcontentdisplayportlet_INSTANCE_GDEKUmSJfYT4_entryStart=0&p_p_id=1_WAR_wtjournalcontentdisplayportlet_INSTANCE_GDEKUmSJfYT4&p_p_lifecycle=0&ajax=1'


class RaiffeisenhuSpider(scrapy.Spider):
	name = 'raiffeisenhu'
	start_urls = [base]

	def parse(self, response):
		post_links = response.xpath('//article')
		for post in post_links:
			url = post.xpath('./a/@href').get()
			date = post.xpath('.//time/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//article/h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=RaiffeisenhuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
