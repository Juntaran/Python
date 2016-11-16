# -*- coding:utf-8 -*-
'''
Created on 2016-5-2
获取  教务系统 信息
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
    # 模拟登陆研究生教务系统
    def __init__(self):
        self.baseURL = ""
        self.enable = True
        self.charaterset = "gb2312"
        string = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2438.3 Safari/537.36"
        self.headers = {'User-Agent' : string}
        self.cookie = cookielib.CookieJar()
        self.hander = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.hander)

    # 验证码处理
    def getCheckCode(self):
        # 验证码连接
        # checkcode_url = "http://yjs.ustc.edu.cn/checkcode.asp"
        checkcode_url = "http://jw.hrbeu.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS"
        request = urllib2.Request(checkcode_url, headers=self.headers)
        picture = self.opener.open(request).read()
        # 将验证码写入本地
        local = open("checkcode.jpg", "wb")
        local.write(picture)
        local.close()
        # 调用系统默认的图片查看程序查看图片
        os.system("checkcode.jpg")
        # 手工识别验证码
        txt_check = raw_input(str("请输入验证码").encode(self.charaterset))
        return txt_check

    # 模拟登陆
    def login(self, userid, userpwd):
        # 获取验证码
        txt_check = self.getCheckCode()
        postData = {"userid":userid, "userpwd":userpwd, "txt_check":txt_check}
        data = urllib.urlencode(postData)

        # request_url = "http://yjs.ustc.edu.cn/default.asp"
        request_url = "http://jw.hrbeu.edu.cn/ACTIONLOGON.APPPROCESS"
        request_new = urllib2.Request(request_url, headers=self.headers)
        response = self.opener.open(request_new, data)

    # 抓取网页
    def getHtml(self, url):
        try:
            request_score = urllib2.Request(url, headers=self.headers)
            response_score = self.opener.open(request_score)
            print('claw page')
            return response_score.read().decode("gb2312", 'ignore').encode("utf8")
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                string = "连接bbs 失败, 原因" +  str(e.reason)
                print string.encode(self.charaterset)
                return None

    # 获取成绩信息
    def getScore(self):
        # get score
        # score_url = "http://yjs.ustc.edu.cn/score/m_score.asp"
        score_url = "http://jw.hrbeu.edu.cn/ACTIONQUERYSTUDENTSCORE.APPPROCESS"
        content = self.getHtml(score_url)
        if not content:
            print "获取成绩失败"
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
            #record = unicode("课程名称:%40s\t成绩:%5s\t学分:%5s" % (item[0].strip(), item[1].strip(), item[2].strip()), "utf8")
            #print item[0].encode("utf8"), item[1], item[2]
            #print record
        return [class_name, class_grade, class_credit]

    # 科大的gpa 转化公式， 不全， 我们只写了自己成绩中对应的部分
    def convert2GPA(self, grade):
        if grade == "通过":
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


    # 成绩显示
    def display(self):
        result = self.getScore()
        name = result[0]
        grade = result[1]
        credit = result[2]
        sum = 0
        count = 0
        for i in range(len(name)):
            record = unicode("课程名称:%40s\t成绩:%5s\t学分:%5s" % (name[i], grade[i], credit[i]), "utf8")
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
    # 这里改成自己的账号和密码信息
    userpwd = "13684502706"
    yjs = YJSSpider()
    yjs.login(userid, userpwd)
    # yjs.display()
    os.system("pause")
