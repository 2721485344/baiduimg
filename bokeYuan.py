#_*_coding:utf-8_*_
"""
需求分析
获取博客园每一篇帖子标题和内容
源码分析
入口："https://www.cnb.com/"
  1、获取标题的url   //a[@class='titlelnk']
  2、通过URL访问每一篇帖子的详细内容，获取标题和内容

  //a[@id='cb_post_title_url']/text()
  String(div[@id='cnblogs_post_body'])
  第二页的url
  https://www.cnblogs.com/#p2
"""
import numpy as np
import pandas as pd
import requests
from  bs4 import BeautifulSoup
from lxml import etree
requestUrl="https://www.cns.com/"
headers={
'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}
page=1 #页数
num=1  #帖子的数量
while True:
       html=requests.get(requestUrl,headers=headers)
       html=etree.HTML(html.text)
       # https: // www.cnb.com / sitehome / p / 190
       urllist=html.xpath("//a[@class='titlelnk']/@href")#文章列表
       for url in urllist:
            print("第{0}页,第{1}条".format(page,num))
            htm2=requests.get(url,headers=headers)
            htm2 = etree.HTML(htm2.text)
            htm2title=htm2.xpath("//a[@id='cb_post_title_url']/text()")
            print(htm2title)
            htm2content=htm2.xpath("string(//div[@id='cnblogs_post_body'])")
            print("*"*50+ "\n")
            print(htm2content)
            with open('bokeyuan.txt','a+',encoding='utf-8') as file:
                file.write(str(htm2title)+"\n")
                file.write(str(htm2content) + "\n")
                file.write("*"*50+ "\n")
            num+=1
       aLast = html.xpath("//div[@class='pager']/a[last()]")  # 分页的url
       requestUrl = "https://www.cn.com" + str(aLast[0].xpath('@href')[0])
       if(aLast[0].xpath('text()')[0]=="Next >"):
           page+=1
           num=1
           print(requestUrl)
       else:
           break
