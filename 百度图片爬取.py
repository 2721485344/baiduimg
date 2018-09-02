#_*_coding:utf-8_*_
"""
需求：输入关键字即可获取对应的百度图片
分析：找到获取图片的Url(战斗机)
      http://img2.imgtn.bdimg.com/it/u=86738536,1961393008&fm=27&gp=0.jpg
      有鼠标滚轮事件
      https://image.baidu.com/search/acjson?
      tn=resultjson_com&ipn=rj&ct=201326592
      &is=&fp=result&queryWord=战斗机图片
      &cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1
      &z=&ic=0&word=战斗机图片&s=&se=&tab=&width=&height=&face=0
      &istype=2&qc=&nc=1&fr=&pn=30&rn=30&gsm=1e&1524010904022=
      加载参数
      gsm:1e   =str(hex(pn))[-2:]16 进制
      pn: 30  120  150
      int(time.time()*1000)
"""


import requests
from xml import etree
import time
import json
headers={
'Host':'tupian.baidu.com',
'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59'
}
url='https://image.baidu.com/search/acjson?' \
    'tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&' \
    'queryWord={0}&cl=2&lm=-1&ie=utf-8&oe=utf-8&' \
    'adpicid=&st=-1&z=&ic=0&word={0}&s=&se=&tab=&' \
    'width=&height=&face=0&istype=2&qc=&nc=1&fr=&' \
    'pn={1}&rn=30&gsm={2}&{3}='
word=input("请输入要爬取的图片名称")
pn=0
gsm=str(hex(pn))[-2:]
times=int(time.time()*1000)
page=1
proxies = {
                "http": "http://110.190.77.104:8080",
                "https":"https://119.28.152.208:80",
            }
while True:
    imgJson=requests.get(url.format(word,pn,gsm,times),proxies=proxies,headers=headers).content.decode("utf-8")
    imgJson=json.loads(imgJson)
    print(imgJson)
    # imgJson=imgJson.json()
    num=1
    for midURl in imgJson['data']:
        if midURl:
            imgUrl=midURl['middleURL']# 每个图片的url
            print("*"*50)
            print(imgUrl)
            imgName=midURl['fromPageTitleEnc']#每个图的名字
            print(imgName)
            headers['Host']='ss2.bdstatic.com'
            headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
            proxies = {
                "http": "http://110.190.77.104:8080",
                "https":"https://119.28.152.208:80",
            }
            img=requests.get(imgUrl,headers=headers,proxies=proxies,stream=True).raw.read()#获取每张图片的套接字
            #保存图片
            with open('img\img{0}.jpg'.format(imgName),'wb') as file:
                # for i in img.iter_content(1024 * 10):  # 每次读取1024
                #     file.write(i)  # 每次写1024
                file.write(img)
            print('第{0}页，第{1}张图片'.format(page,num))
            time.sleep(5)
            num+=1
    if imgJson['displayNum']>pn:
        pn+=30
        page+=1
        gsm=str(hex(pn))[-2]
