# -*- coding: utf-8 -*-
import scrapy,re
from nhbook.items import NhbookItem

class NhbookSpider(scrapy.Spider):
	name = 'nhBook'
	allowed_domains = ['nhentai.net']
	# 爬取某指定搜索词下的book
	# key = "lolicon+chinese"
	# baseURL = "https://nhentai.net/search/?q="
	# 爬取开始url,搜索类爬虫
	# start_urls = ['https://nhentai.net/search/?q=+chinese+lolicon&page=22']
	
	#爬取每一天内更新的所有本子
	start_urls = ["https://nhentai.net/"]
	baseURL = "https://nhentai.net/?page="
	# offset = ""
	
	server = "https://nhentai.net"

	def parse(self, response):
		book_urls = response.xpath("//a[@class='cover']/@href").extract()
		for index,url in enumerate(book_urls):
			book_url = self.server + url
			#print(book_url)
			# yield scrapy.Request(book_url,callback = self.parse_pages,meta={'book_url': book_url})
			yield scrapy.Request(book_url,callback = self.parse_date,meta={'book_url': book_url})
			
		#搜索结果页数循环迭代
		# for i in range(33,255):
		# 	offset = "&page="+str(i)
		# 	next_url = self.baseURL + self.key +offset
		# 	#print(next_url)
		# 	yield scrapy.Request(next_url,callback = self.parse)
		
		#迭代首页最新几页
		for i in range(2,5):
			next_url = self.baseURL + str(i)
			#print(next_url)
			yield scrapy.Request(next_url,callback = self.parse)
	# 判断书的跟新url是否符合标准，爬取某一天内更新的所有书
	def parse_date(self,response):
		date = response.xpath("//div[@id = 'info']//time/@datetime").extract()[0]
		keydate = "2019-03-31"
		if(date[0:10] == keydate):
			# print("这个是2019-03-17更新的")
			item = NhbookItem()
			book_url = response.meta['book_url']
			# print(book_url)
			book_page_num = response.xpath("//div[@class = 'thumb-container']").extract()
			n = len(book_page_num)
			try:
				book_name = response.xpath("//div[@id = 'info']/h2/text()").extract()[0]
			except IndexError:
				book_name = response.xpath("//div[@id = 'info']/h1/text()").extract()[0]
			cover_url = response.xpath("//div[@id = 'cover']/a/img/@data-src").extract()[0]
			item['bookname'] = book_name
			# print(cover_url)
			book_id = re.findall(".*/(.*)/.*",cover_url)[0]
			# print(book_id)
			# 用页数循环传入图片url
			for i in range(1,n+1):
				page_url = "https://i.nhentai.net/galleries/"+book_id+"/"+str(i)+".jpg" 
				#print(page_url)
			#	#print(str(i))
				item['imgname'] = str(i)
				item['imgurl'] = page_url
				#print(item['imgname'])
				yield item
		else:
			print("这个不是2019-03-31更新的")


	# 爬取每本书名和页数，传入item
	def parse_pages(self, response):
		item = NhbookItem()
		book_url = response.meta['book_url']
		#print(book_url)
		book_page_num = response.xpath("//div[@class = 'thumb-container']").extract()
		n = len(book_page_num)
		try:
			book_name = response.xpath("//div[@id = 'info']/h2/text()").extract()[0]
		except IndexError:
			book_name = response.xpath("//div[@id = 'info']/h1/text()").extract()[0]
		cover_url = response.xpath("//div[@id = 'cover']/a/img/@data-src").extract()[0]
		item['bookname'] = book_name
		# print(cover_url)
		book_id = re.findall(".*/(.*)/.*",cover_url)[0]
		# print(book_id)
		# 用页数循环传入图片url
		for i in range(1,n+1):
			page_url = "https://i.nhentai.net/galleries/"+book_id+"/"+str(i)+".jpg" 
			#print(page_url)
		#	#print(str(i))
			item['imgname'] = str(i)
			item['imgurl'] = page_url
			#print(item['imgname'])
			yield item
		#	cover = https://t.nhentai.net/galleries/1326248/cover.jpg
		#	page = https://i.nhentai.net/galleries/1326248/63.jpg

		#while()
		#print(book_name+"有"+str(book_page_num)+"本书！")
		#page_urls = response.xpath("//div[@class = 'gallerythumb']/@href").extract()
		#for()