# -*- coding:gb2312 -*-
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from dirbot.items import Website
import sys
import string
sys.stdout=open('output.txt','w') #����ӡ��Ϣ�������Ӧ��λ����


add = 0
class DmozSpider(CrawlSpider):

    name = "huhu"
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/huhuuu",
    ]

    
    rules = (
        # ��ȡƥ�� huhuuu/default.html\?page\=([\w]+) �����Ӳ���������(û��callback��ζ��followĬ��ΪTrue)
        Rule(SgmlLinkExtractor(allow=('huhuuu/default.html\?page\=([\w]+)', ),)),

        # ��ȡƥ�� 'huhuuu/p/' �����Ӳ�ʹ��spider��parse_item�������з���
        Rule(SgmlLinkExtractor(allow=('huhuuu/p/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        global add #����ͳ�Ʋ��ĵ�����
        
        print  add
        add+=1
        
        sel = Selector(response)
        items = []

        item = Website()
        item['headTitle'] = sel.xpath('/html/head/title/text()').extract()#�۲���ҳ��Ӧ��htmlԴ��
        item['url'] = response
        print item
        items.append(item)
        return items