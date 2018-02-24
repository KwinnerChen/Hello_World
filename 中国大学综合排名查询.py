from bs4 import BeautifulSoup
import bs4, requests

def gethtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return None

def htmlparser(html):
    if html:
        soup = BeautifulSoup(html, 'lxml')
        for tr in soup.find('tbody').children:
            if isinstance(tr, bs4.element.Tag):
                tds = tr.find_all('td')
                yield tds[0].string, tds[1].string, tds[3].string

def printinfo(iterable, num=None):
    splt = '%10s\t%10s\t%10s'
    print(splt % ('排名', '学校', '总分'))
    #splt = '{0:^10}\t{1:{3}^10}\t{2:^10}'
    #print(splt.format('排名', '学校', '总分', chr(12288)))
    flag = 0
    for td in iterable:
        if flag == num or num == 0:
            break
        elif num == None or num:
            print(splt % td)
            #print(splt.format(td[0], td[1], td[2], chr(12288)))
        flag += 1

def main(url,num):
    html = gethtml(url)
    printinfo(htmlparser(html),num)

if __name__ == '__main__':
    temp = input('想知道前几位？：')
    main('http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html',num=int(temp))
