# Defined Number of Threads -> Multiple Pages per Thread -> Multiple posts per page

from scrapy import Spider, Request
from forum.items import ForumItem

import re

class ForumSpider(Spider):
	name = "forum_spider"
	allowed_url = ['https://liberalforum.net'] 
	start_urls = ['https://liberalforum.net/viewtopic.php?t=37200']

#load start page for for each thread:
	def parse(self, response):

		numThreads = ['https://liberalforum.net/viewtopic.php?t={}'.format(x) for x in range(14493,37211)]
	# desired start = When Trump announced Presidency: 14493
		for thread in numThreads:
			yield Request(url = thread, callback = self.parse_within_thread)

#load each page of each thread:
	def parse_within_thread(self,response):

	# different xpath for when only one thread page and when thread has multiple pages...

		if response.xpath('//*[@id="page-body"]/div[1]/div[1]/div[3]/div[2]/a/strong[2]/text()').extract_first() is None:
			threadMaxPage = 1
		else:	 
			threadMaxPage = response.xpath('//*[@id="page-body"]/div[1]/div[1]/div[3]/div[2]/a/strong[2]/text()').extract_first()

		numPages =['https://liberalforum.net/viewtopic.php?t={}&start={}'.format(x,y) for x in range(14493,37211) for y in range(0,20*(int(threadMaxPage)-1),20)]
		for page in numPages:
			yield Request(url = page, callback=self.parse_posts_within_thread_page)
	
 #parse components of each post of each page in each thread
	def parse_posts_within_thread_page(self, response):
		
		posts = response.xpath('//div[@class="vtinner"]')
		
		for post in posts:
			
			threadReplies = response.xpath('//*[@id="page-body"]/div[1]/div[1]/div[6]/div/div/span[1]/text()').extract_first()
			threadTitle = response.xpath('//*[@id="page-body"]/div[1]/h2/a/span/text()').extract_first()
			userName = post.xpath('div[3]/div/span/a/text()').extract_first()
			userPosts = post.xpath('div[3]/div[2]/a/text()').extract_first()
			userPolitics = post.xpath('div[3]/div[2]/a[2]/text()').extract  # <- Issue with spacing/newline characters
			userMoney =  post.xpath('div[3]/div[2]/a[3]/span/text()').extract_first()
			postDateTime = post.xpath('./div[2]/div[2]/span/a/text()').extract_first()
			postText = post.xpath('div[4]/div[@class="content"]/text()').extract() # <- Issue with spacing/newline characters

			item = ForumItem()
			item['threadReplies'] = threadReplies
			item['threadTitle'] = threadTitle
			item['userName'] = userName
			item['userPosts'] = userPosts
			item['userPolitics'] = userPolitics
			item['userMoney'] = userMoney
			item['postDateTime'] = postDateTime
			item['postText'] = postText
		
			yield item