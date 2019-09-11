# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
#from scrapy.pipelines.files import FilesPipeline
from nhbook.settings import IMAGES_STORE as images_store
import scrapy,os,copy

class NhbookPipeline(object):

	def create_dir(self, path):
		# 去除首位空格
		path = path.strip()
		# 去除尾部 \ 符号
		path = path.rstrip("\\")
		# 判断路径是否存在
		isExists = os.path.exists(path)
		# 判断结果
		if not isExists:
			# 如果不存在则创建目录
			# 创建目录操作函数
			os.makedirs(path)
			#print(path + ' 创建成功')
			return True
		else:
			# 如果目录存在则不创建，并提示目录已存在
			#print(path + ' 目录已存在')
			return False

	def process_item(self, item, spider):
		#将不同的book保存成不同的文件夹
		# replacedStr = re.sub("\d+", "222", inputStr)
		book_name = item["bookname"]
		#bookname = re.sub('[\/:*?"<>|]', '', book_name)
		path = images_store + book_name
		self.create_dir(path)
		#print(path)
		return item
class NhbookImgPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		# 这里meta={'item': item},目的事件item传递到file_path中
		img_url = item['imgurl']
		yield scrapy.Request(img_url,meta = {'item':copy.deepcopy(item)})

	def file_path(self, request, response=None, info=None):
		item = request.meta['item']
		book_name = item['bookname']
		#folder_strip = folder.strip()
		#image_guid = request.url.split('/')[-1]
		img_name = item['imgname']
		filename = book_name+"/"+img_name+".jpg"
		return filename

	#def item_completed(self, results, item, info):
		#book_name = item["bookname"]
		#img_name = item["imgname"]
		#print(img_name)
		#image_path = [x["path"] for ok, x in results if ok]
		#print(image_path)
		#print(image_path)
		#IMAGES_STORE = "F:/pyData/douyu/"
		# print(image_path)
		# newpath = book_name +'/'+img_name+'.jpg'
		# print(newpath)
		# print(newpath)
		# 更改文件名
		#os.rename(images_store + image_path[0],images_store + newpath)
		#return item
	
	#def file_path(self, request, response=None, info=None):

	#	book_name = request.meta.item['bookname']
	#	img_name = request.meta.item['imgname']
	#	newpath = book_name +'/'+img_name+'.jpg'
	#	print("newpath")
	#	#return newpath
