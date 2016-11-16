#encoding:utf-8

import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers=headers)
# print (start_html.text)
Soup = BeautifulSoup(start_html.text, 'lxml') #ʹ��BeautifulSoup���������ǻ�ȡ������ҳ����lxml����ָ���Ľ����� ������ο��ٷ��ĵ�Ŷ��

'''
li_list = Soup.find_all('li')
for li in li_list:
    print(li)
'''
#��˼���Ȳ��� classΪ all ��div��ǩ��Ȼ��������е�<a>��ǩ
all_a = Soup.find('div', class_='all').find_all('a')
for a in all_a:
    # print a
    title = a.get_text()    #ȡ��a��ǩ���ı�
    path = str(title).strip()  #ȥ���ո�
    os.makedirs(os.path.join("D:\mzitu", path))   #����һ����ͼ�ļ���
    os.chdir("D:\mzitu\\" + path) #�л����ļ���
    href = a['href']        #ȡ��a��ǩ��href ����
    html = requests.get(href, headers=headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find_all('span')[10].get_text()    #�������е�<span>��ǩ��ȡ��ʮ����<span>��ǩ�е��ı�Ҳ�������һ��ҳ����
    for page in range(1, int(max_span)+1):
        page_url = href + '/' + str(page)
        # print page_url
        img_html = requests.get(page_url, headers=headers)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url  = img_Soup.find('div', class_='main-image').find('img')['src']
        # print img_url
        name = img_url[-9:-4]
        img = requests.get(img_url, headers=headers)
        f = open(name + '.jpg', 'ab')   #д���ý���ļ�����Ҫb�������
        f.write(img.content)
        f.close()