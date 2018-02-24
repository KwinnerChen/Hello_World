#! usr/bin/evn python
# -*- coding:utf-8 -*-
import requests, re
import threading


def htmldown(url):
	'''
	接受一个链接，并返回一个HTML文件对象，如果链接解析失败，则返回None。
	'''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(url + ' 下载完成！')
        return r.text
    except:
        print(url + '下载失败！')
        return None 

def htmlparser(url, html):
	'''接受页面链接及该页面HTML文件，解析得到需要内容，并返回一个二元组列表。没有内容返回空列表。
	'''
    try:
        titles = re.findall(r'"title":"([\w\d\s]*)"', html)
        prices = re.findall(r'"price":"([\d\.]*)"', html)
        infolist = zip(titles, prices)
        print(url + '解析完成！')
        return infolist
    except:
        print(url + '此页没有信息')
        infolist = list()
        return infolist

def dataoutput(url, infolist):
	'''接受链接及相应信息列表。符合条件存储
	'''
    plt = '{0:4}\t{1:10}\t{2:20}\n'
    count = 1
    if infolist:
        try:
            with open('淘宝手机信息.txt', 'a') as f:
                f.write(plt.format('序号', '价格', '手机简介'))
                for element in infolist:
                    f.write(plt.format(str(count), element[1], element[0]))
                    count += 1
        except:
            print('存储出现了错误，请检查文件夹及代码')
    else:
        print(url + '没有任何信息输出！')

def urlmaker():
	'''url生成器，“下一页”由js生成，根据链接规则生成相应链接，链接失效需要改变
	'''
    num = 0
    baseurl = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&p4ppushleft=5%2C48&s={0}'
    while True:
        yield baseurl.format(num)
        num += 48

def main(url, mylock):
	'''接受必要参数，及线程锁，避免数据输出出现错误
	'''
    html = htmldown(url)
    infolist = htmlparser(url, html)
    mylock.acquire()
    dataoutput(url, infolist)
    mylock.release()

if __name__ == '__main__':
    mylock = threading.RLock()
    flag = 0
    for url in urlmaker():
        spiderThread = threading.Thread(target=main, args=(url,mylock,), name='thread'+url.split('=')[-1])
        flag += 1
        spiderThread.start()
        spiderThread.join()
        if flag == 3:
            print('已提取设置的%s页，停止。' % flag)
            break
