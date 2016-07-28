# -*- coding: utf-8 -*-
"""
Created on Sun 4/14 12:49:26 2016

@author: 龙
"""

import urllib.request
from bs4 import BeautifulSoup
import re
import http.cookiejar,urllib.parse
from collections import deque
from html.parser import  HTMLParser
from tkinter import *
import tkinter.messagebox

class spider(object):
    i = 0  
    num = 0
    j = 0
    dict = {}
    proxy = {1:'http://xx.xx.xx.xx:xx',2:'http://xx.xx.xx.xx:xx'}
    webUrl = set()
    queue = deque()    
    
    def __init__(self):
        pass
    
    def getNum(self):
        j = j+1
        return j;
    
    def getHTML(self,url):
        try:#伪装成浏览器+cookie的处理
            cj = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(\
            urllib.request.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-Agent',
            'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit\
            /537.36 (KHTML, like Gecko) Chrome/41.0.2272.101\
            Safari/537.36'),
            ('Cookie','4564564564564564565646540')]
            urllib.request.install_opener(opener)
            html_bytes=''
            try:
                html_bytes = urllib.request.urlopen(url).read()
                html_bytes = html_bytes.decode('utf-8')
            except:
                html_bytes = urllib.request.urlopen(url).read()
        except:#使用代理服务器
            try:
                urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler(self.proxy[1]),urllib.request.HTTPHandler))
            except:
                urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler(self.proxy[2]),urllib.request.HTTPHandler))
            html_bytes = urllib.request.urlopen(url).read().decode('utf-8')
        finally:
            return html_bytes
        
    def subMessage(self,message):
        p = re.compile(r'[(<.*> | \s | \\ | \/ | \= | {.*} | & | : | ; | \" | \' | # | \-) | (a-zA-Z)*]')
        length = len(message)
        for link in range(length):
            print('message-->{}\n'.format(p.sub('',str(message[link].contents))))
    
    def deepFind(self,websiteTest,keyword):#关键词搜索
        html_doc = self.getHTML(websiteTest)
        soup = BeautifulSoup(
                            html_doc,
                            'html.parser',#解析器
                            from_encoding='utf-8'
                            )
        some = soup.find_all(re.compile(r'[a | p]'),text=re.compile(r'[^\w]*'+keyword+r'[\w$]*'))
        self.subMessage(some)
        return some
    
    def urlJudge(self,url):#运用字典去重
        if url not in self.dict.keys():
            self.dict[url] = 1
            return True
        else:
            return False
    
    def urlSet(self,site):#集合去重,与字典去重任选一种
        if site not in self.webUrl:
            self.webUrl |= {site}
            return True
        else:
            return False
        
    def saveFile(self,web):
        file = open('TEST'+str(self.i)+'.txt','wb')
        url = urllib.request.urlopen(web)
        buf = url.read()
        file.write(buf)
        file.close()
        self.i += 1
        
    def theSameMessage(self,web,keyword):
        if self.urlJudge(web):
            self.queue.append(web)
            print('加入队列---->',web)
            self.PrintMessage(self.deepFind(web,keyword),web,keyword)

    def PrintMessage(self,lines,website,keyword):
        #self.saveFile(website)
        if website[0:5]!='http:' or website[0:2]=='//':
            ws = 'http://'+website
        else:
            ws = website
        for link in lines:
            if 'href'in link.attrs:#判断能否进行深度搜索
                if link['href']=='/' or link['href']=='#':
                    if self.urlJudge(website):
                        self.queue.append(website)
                        print('加入队列---->',website)
                elif link['href']!='/' and link['href']!='#':
                    website = link['href']
                    if link['href'][0:5]=='http:' and website != ws:
                        self.theSameMessage(website,keyword)
                    elif link['href'][0:2]=='//':
                        website = 'http:'+website
                        if website != ws:
                            self.theSameMessage(website,keyword)
                    else:   
                        if website not in ws:
                            if ws[-2:-1]!='/':
                                website = ws + '/' + website
                            else:
                                website = ws + website
                            self.theSameMessage(website,keyword)  
                         
class Application(Frame,spider):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        spider.__init__(self)
        self.grid()
        self.createWidgets()
 
    def createWidgets(self):
        Label(self, text='网址:').grid(row=0)
        Label(self, text='内容:').grid(row=1)
        self.website_ = Entry(self)
        self.website_.grid(row=0,column=1)
        self.keyword_ = Entry(self)
        self.keyword_.grid(row=1,column=1)
        self.alertButton = Button(self, text='查询', command=self.do_findMessage)
        self.alertButton.  grid(row=2,column=1)            
    
    def do_findMessage(self):
        website_w = self.website_.get()
        keyword_w = self.keyword_.get()
        info = self.deepFind('http://'+website_w,keyword_w)
        self.PrintMessage(info,'http://'+website_w,keyword_w)
            
if __name__ == '__main__':  
    app = Application()
    app.master.title('爬虫之深度搜索')
    app.mainloop()
    #sp = spider()
    #website = input('请输入网址:')    
    #keyword = input('请输入查询关键字：')   
    #website = "www.baidu.com"
    #keyword = "百度"
    #info = sp.deepFind('http://'+website,keyword) 
    #sp.PrintMessage(info,'http://'+website,keyword)
    