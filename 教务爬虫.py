# -*- coding:utf-8 -*-
'''
Created on 2016-5-2
��ȡ  ����ϵͳ ��Ϣ
@author: ThinkPad User
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import re
import cookielib
import sys
import os
import string

class YJSSpider:
    # ģ���½�о�������ϵͳ
    def __init__(self):
        self.baseURL = ""
        self.enable = True
        self.charaterset = "gb2312"
        string = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2438.3 Safari/537.36"
        self.headers = {'User-Agent' : string}
        self.cookie = cookielib.CookieJar()
        self.hander = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.hander)

    # ��֤�봦��
    def getCheckCode(self):
        # ��֤������
        # checkcode_url = "http://yjs.ustc.edu.cn/checkcode.asp"
        checkcode_url = "http://jw.hrbeu.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS"
        request = urllib2.Request(checkcode_url, headers=self.headers)
        picture = self.opener.open(request).read()
        # ����֤��д�뱾��
        local = open("checkcode.jpg", "wb")
        local.write(picture)
        local.close()
        # ����ϵͳĬ�ϵ�ͼƬ�鿴����鿴ͼƬ
        os.system("checkcode.jpg")
        # �ֹ�ʶ����֤��
        txt_check = raw_input(str("��������֤��").encode(self.charaterset))
        return txt_check

    # ģ���½
    def login(self, userid, userpwd):
        # ��ȡ��֤��
        txt_check = self.getCheckCode()
        postData = {"userid":userid, "userpwd":userpwd, "txt_check":txt_check}
        data = urllib.urlencode(postData)

        # request_url = "http://yjs.ustc.edu.cn/default.asp"
        request_url = "http://jw.hrbeu.edu.cn/ACTIONLOGON.APPPROCESS"
        request_new = urllib2.Request(request_url, headers=self.headers)
        response = self.opener.open(request_new, data)

    # ץȡ��ҳ
    def getHtml(self, url):
        try:
            request_score = urllib2.Request(url, headers=self.headers)
            response_score = self.opener.open(request_score)
            print('claw page')
            return response_score.read().decode("gb2312", 'ignore').encode("utf8")
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                string = "����bbs ʧ��, ԭ��" +  str(e.reason)
                print string.encode(self.charaterset)
                return None

    # ��ȡ�ɼ���Ϣ
    def getScore(self):
        # get score
        # score_url = "http://yjs.ustc.edu.cn/score/m_score.asp"
        score_url = "http://jw.hrbeu.edu.cn/ACTIONQUERYSTUDENTSCORE.APPPROCESS"
        content = self.getHtml(score_url)
        if not content:
            print "��ȡ�ɼ�ʧ��"
            return

        string = r'<td class.*?"bt06".*?>.*?<td.*?"bt06".*?>.*?<td.*?"bt06".*?>.*?<td.*?"bt06".*?>(.*?)</td.*?td.*?"bt06".*?>(.*?)</td.*?"bt06".*?>(.*?)</td.*?td.*?"bt06".*?>.*?<td.*?"bt06".*?>.*?<td.*?"bt06".*?>.*?<td.*?"bt06".*?>.*?</td>'
        pattern = re.compile(string, re.S)
        res = re.findall(pattern, content)
        class_name = []
        class_grade = []
        class_credit = []
        for item in res:
            class_name.append(item[0])
            class_grade.append(item[1])
            class_credit.append(item[2])
            #record = unicode("�γ�����:%40s\t�ɼ�:%5s\tѧ��:%5s" % (item[0].strip(), item[1].strip(), item[2].strip()), "utf8")
            #print item[0].encode("utf8"), item[1], item[2]
            #print record
        return [class_name, class_grade, class_credit]

    # �ƴ��gpa ת����ʽ�� ��ȫ�� ����ֻд���Լ��ɼ��ж�Ӧ�Ĳ���
    def convert2GPA(self, grade):
        if grade == "ͨ��":
            return None
        if grade == "A-":
            return 3.7

        try:
            grade_int = int(grade)
            if grade_int >= 95:
                return 4.3
            if grade_int >= 90:
                return 4.0
            if grade_int >= 85:
                return 3.7
            if grade_int >= 82:
                return 3.4
            if grade_int >= 78:
                return 3.1
            return None
        except:
            return None


    # �ɼ���ʾ
    def display(self):
        result = self.getScore()
        name = result[0]
        grade = result[1]
        credit = result[2]
        sum = 0
        count = 0
        for i in range(len(name)):
            record = unicode("�γ�����:%40s\t�ɼ�:%5s\tѧ��:%5s" % (name[i], grade[i], credit[i]), "utf8")
            print record.encode(self.charaterset)
            gpa = self.convert2GPA(grade[i])
            if not gpa:
                continue
            sum += gpa * string.atof(credit[i])
            count += string.atof(credit[i])
        avg = sum / count
        print str("avg gpa : %f" % avg).encode(self.charaterset)

if "__main__" == __name__:
    # userid = "SA14009048"
    userid = "2011201130"
    # ����ĳ��Լ����˺ź�������Ϣ
    userpwd = "13684502706"
    yjs = YJSSpider()
    yjs.login(userid, userpwd)
    # yjs.display()
    os.system("pause")
