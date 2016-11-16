#encoding:utf-8

import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers=headers)
# print (start_html.text)
Soup = BeautifulSoup(start_html.text, 'lxml') #使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）

'''
li_list = Soup.find_all('li')
for li in li_list:
    print(li)
'''
#意思是先查找 class为 all 的div标签，然后查找所有的<a>标签
all_a = Soup.find('div', class_='all').find_all('a')
for a in all_a:
    # print a
    title = a.get_text()    #取出a标签的文本
    path = str(title).strip()  #去掉空格
    os.makedirs(os.path.join("D:\mzitu", path))   #创建一个存图文件夹
    os.chdir("D:\mzitu\\" + path) #切换到文件夹
    href = a['href']        #取出a标签的href 属性
    html = requests.get(href, headers=headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find_all('span')[10].get_text()    #查找所有的<span>标签获取第十个的<span>标签中的文本也就是最后一个页面了
    for page in range(1, int(max_span)+1):
        page_url = href + '/' + str(page)
        # print page_url
        img_html = requests.get(page_url, headers=headers)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url  = img_Soup.find('div', class_='main-image').find('img')['src']
        # print img_url
        name = img_url[-9:-4]
        img = requests.get(img_url, headers=headers)
        f = open(name + '.jpg', 'ab')   #写入多媒体文件必须要b这个参数
        f.write(img.content)
        f.close()