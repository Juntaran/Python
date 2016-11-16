# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import scrapy

from scrapy.item import Item, Field

class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

	import scrapy  
  
class DmozItem(scrapy.Item):  
    title = scrapy.Field()  
    link = scrapy.Field()  
    desc = scrapy.Field()  
	
class Website(Item):

    headTitle = Field()
    description = Field()
    url = Field()