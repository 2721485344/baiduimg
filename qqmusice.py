#_*_coding:utf-8_*_
"""
  需求：爬取所有qq音乐
  入口：获取分类歌单 https://y.p.com/portal/playlist.html
         获取分类歌单列表 https://y.p.com/n/yqq/playsquare/2054035442.html#stat=y_new.playlist.pic_click
         获取每首歌曲详情
         http://dl.stream.pmusic.p.com/C4000037HlEP0subhS.m4a?vkey=9ADBCF5B41C3C81F2B626C7C6D5E85CE5459783FBF33EE885D247B0DBB9CF3DCAE86E53C9A7EB89B91B5E4E35857F87CDE391E5993C87A5D&guid=2438110866&uin=0&fromtag=66
  代码分析：xpath
"""
import  requests
from  bs4 import BeautifulSoup
from lxml import etree
import json

# 获取分类歌单
# 获取分类歌单列表
# 获取每首歌曲详情
# 保存获取每首歌曲详情
def get_classification_list(url,headers):
    r=requests.get(url,headers=headers).content.decode('utf-8')
    print(r)
    html=etree.HTML(r)
    mulislist1=html.xpath("//span[@class='playlist__title_txt']/a")
    print(mulislist)
    mulislist=html.xpath("//span[@class='playlist__title_txt']/a[@class='js_playlist']/@href")
    print(mulislist1)
    return mulislist
if __name__=="__main__":
    heads = {
        'referer':'https://y.p.com/portal/playlist.html',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
    url='https://c.py.p.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.34692207151847465&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin={0}&ein={1}'
    sin=0
    ein=29
    page=1 #页码数
    while True:
        html=requests.get(url.format(sin,ein),headers=heads).text
        dissidList=json.loads(html.strip('getPlaylist()'))#第一页获取歌曲列表
        classmusie=1
        for list in dissidList['data']['list']:
            dissid=list['dissid'] #获取歌单id
            dissname=list['dissname']#获取歌单名称
            songmidurl='https://p.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid={0}&format=jsonp&g_tk=5381&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
            heads['referer']='https://p.pq.com/n/yqq/playsquare/2054035442.html'
            html = requests.get(songmidurl.format(dissid), headers=heads).text
            song_dic=json.loads(html.strip('playlistinfoCallback()'))
            k=1# 歌曲
            for songmids in song_dic['cdlist'][0]['songlist']:
                songmid=songmids['songmid']#获取songmid
                songname=songmids['songname']#获取songmid
                filename='C400{0}.m4a'.format(songmid)
                vkeyurl='https://c.pq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&' \
                        'jsonpCallback = MusicJsonCallback' \
                        '&loginUin=0&hostUin=0&format=json&inCharset=utf8' \
                        '&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0' \
                        '&cid=205361747&callback=MusicJsonCallback' \
                        '&uin=0&songmid={0}&' \
                        'filename={1}&guid=1093240106'
                heads['referer'] = 'https://y.p.com/portal/playlist.html'
                vkhtml = requests.get(vkeyurl.format(songmid,filename), headers=heads).text
                vkdict=json.loads(vkhtml.strip('MusicJsonCallback()'))
                vkey=vkdict['data']['items'][0]['vkey'] #提取vkey
                #通过vkey下载音乐
                musicurl='http://dl.stream.p.pp.com/C400{0}.m4a?vkey={1}&guid=1093240106&uin=0&fromtag=66'
                heads['Host']='dl.stream.qqmusic.qq.com'
                del heads['referer']
                musicurhtml=requests.get(musicurl.format(songmid,vkey),headers=heads,stream=True)
                try:
                    with open("music/music{0}.mp3".format(songname),'wb') as file:
                        for i in musicurhtml.iter_content(1024*10): #每次读取1024
                            file.write(i) #每次写1024
                except OSError:
                    continue
                print("第{0}页，分类{1},第{2}首歌{3}".format(page,classmusie,k,songname))
                k+=1
            classmusie+=1
        #下一页
        sin+=30
        ein+=30
        page+=1
        if sin<6075:
            break

