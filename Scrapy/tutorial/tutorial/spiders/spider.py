# -*- coding:gb2312 -*-
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dirbot.items import Website
import sys
import string
sys.stdout=open('output.txt','w') #将打印信息输出在相应的位置下


add = 0
class DmozSpider(CrawlSpider):

    name = "huhu"
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/huhuuu",
    ]

    
    rules = (
        # 提取匹配 huhuuu/default.html\?page\=([\w]+) 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(SgmlLinkExtractor(allow=('huhuuu/default.html\?page\=([\w]+)', ),)),

        # 提取匹配 'huhuuu/p/' 的链接并使用spider的parse_item方法进行分析
        Rule(SgmlLinkExtractor(allow=('huhuuu/p/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        global add #用于统计博文的数量
        
        print  add
        add+=1
        
        sel = Selector(response)
        items = []

        item = Website()
        item['headTitle'] = sel.xpath('/html/head/title/text()').extract()#观察网页对应得html源码
        item['url'] = response
        print item
        items.append(item)
        return items