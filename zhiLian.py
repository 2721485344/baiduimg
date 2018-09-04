#_*_coding:utf-8_*_
"""
需求分析：
    获取职位名称等。。。。
入口：
    http://sou.*.com/
    //div[@id='search_right_demo']/div/div/a/@href   获取职位列表url
    //td[@class='zwmc']/div/a[1]      获取详细职位列表url
    //a[@class='next-page']           下一页
    //div[@class='inner-left fl']/h1   获取标题
    //div[@class='inner-left fl']/h2   公司名称
    //div[@class='welfare-tab-box']     公司福利   返回文本，text()返回列表
    //ul[@class='terminal-ul clearfix']/li  获取职位信息 8 个

    代码
"""
# import requests
# from lxml import etree
# headers={
# 'Referer': 'http://sou.#.com/',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
# }
# requestsURL='http://sou.#.com/'
# zhlian=requests.get(requestsURL,headers=headers)
# html=etree.HTML(zhlian.text)
# print(html)
# urlList=html.xpath("//div[@id='search_right_demo']/div/div/a/@href")
# print(urlList)
# for url in urlList:
#     zhlian2 = requests.get(requestsURL+url, headers=headers)
#     html2=etree.HTML(zhlian2.text)
#     urlList2=html2.xpath("//td[@class='zwmc']/div/a[1]/@href")
#     print(urlList2)
#     for url2 in urlList2:
#         zhlian3=requests.get(requestsURL + url, headers=headers)
#         html3 = etree.HTML(zhlian3.text)
#         title=html2.xpath("//div[@class='inner-left fl']/h1")
#         gsmc=html2.xpath("//div[@class='inner-left fl']/h2")
#         print("*"*50)
#         print(title)
# 1,获取所有职位分类列表
import requests
from lxml import etree
import re
def get_job_cat_list(url,headers):
    r=requests.get(url, headers=headers).content.decode('utf-8')
    html=etree.HTML(r)
    job_cat_list=html.xpath("//div[@id='search_right_demo']/div/div/a/@href")
    pattern=re.compile('jl=\d+&')
    job_cat_list=[url[:-1]+str(pattern.sub('jl=489',i)) for i in job_cat_list]
    return  job_cat_list
# 2,获取所有职位列表(返回页码和列表)
def get_job_list(url,headers):#url 跳转列表url
    r = requests.get(url, headers=headers).content.decode('utf-8')
    html = etree.HTML(r)
    zwxqlist=html.xpath("//td[@class='zwmc']/div/a[1]/@href")#页面的url
    next_page=html.xpath("//a[@class='next-page']/@href")
    if len(next_page):
        return zwxqlist ,next_page[0]
    else:
        return zwxqlist, next_page
    # zwxqlist = html.xpath("//td[@class='zwmc']/div/a[1]")  # 页面的url
    # zwxqlist = html.xpath("//a[@class='next-page nopress2']")  # 最后一页的url
    pass
# 3,获取职位详细信息
def get_job_info(url,headers):
    r = requests.get(url, headers=headers).content.decode('utf-8')
    html = etree.HTML(r)
    job_dic={}
    job_dic['zwmc']=html.xpath("string(//div[@class='inner-left fl'or @class='fl']/h1)")
    job_dic['gsmc']=html.xpath("string(//div[@class='inner-left fl'or @class='fl']/h1)")
    job_dic['gsfl']=html.xpath("//div[@class='inner-left fl']/div/span/text()")
    job_dic['zwyx']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[1]/strong)")
    job_dic['gzdd']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[3]/strong)")
    job_dic['fbrq']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[3]/strong)")
    job_dic['gzxz']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[4]/strong)")
    job_dic['gzjy']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[5]/strong)")
    job_dic['zdxl']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[6]/strong)")
    job_dic['zprs']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[7]/strong)")
    job_dic['zwlb']=html.xpath("string(//div[@class='terminalpage-left']/ul/li[8]/strong)")
    return job_dic
# 4，保存数据
def save_data(data):
    data=','.join([str(i) for i in data.values()])
    with open('zl.txt','a+',encoding='utf-8')as file:
        file.write(data)
    pass
if __name__=='__main__':
    url="http://sou.#.com/"
    headers={
    'Referer': 'http://sou.#.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
    job_cat_list=get_job_cat_list(url,headers)

    for j in job_cat_list:
        page = 1
        job_sum_list, next_page=get_job_list(j,headers)
        print('第{0}页，第60条'.format(page))
        print(len(job_sum_list))
        while next_page:
            page += 1
            job_list, next_page = get_job_list(next_page, headers)
            print('第{0}页，第60条'.format(page))
            print(len(job_list))
            job_sum_list += job_list
        else:# 只获取第一个url中所有数据列表
            break
    print(len(job_sum_list)) #60 * 页码数量
    zhiliandatals=[]
    for i in job_list:
        print(i)
        job_dic=get_job_info(i,headers)
        with open('zl.txt', 'a+', encoding='utf-8')as file:
            file.write(str(job_dic))
        zhiliandatals.append(job_dic)
        print(job_dic)
