import requests
from bs4 import BeautifulSoup
import bs4
"""
这是一个爬取中国最好大学排名的爬虫
缺陷：只爬取一页，只有30个大学
"""
def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivRank(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds=tr('td')
            temp=[]
            for td in tds:
                s=td.text.strip()
                cleaned_str = ' '.join(s.split())
                temp.append(cleaned_str)
            ulist.append(temp)


def printUnivRank(ulist,num):
    print("{:^5}{:^100}{:^10}{:^10}{:^10}{:^10}".format("排名", "学校名称/级别", "省市", "类型", "总分", "办学层次"))
    for i in range(num):
        u=ulist[i]
        print("{:^5}{:^100}{:^10}{:^10}{:^10}{:^10}".format(u[0], u[1], u[2], u[3], u[4], u[5]))

def main():
    uinfo=[]
    url="https://www.shanghairanking.cn/rankings/bcur/2024"
    html=getHTMLText(url)
    fillUnivRank(uinfo,html)
    printUnivRank(uinfo,20)

if __name__ == '__main__':
    main()