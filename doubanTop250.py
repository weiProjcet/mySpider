import csv
import time

import requests
from bs4 import BeautifulSoup
import re

"""
    获取豆瓣网页信息，
"""
def getHtml(url):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        print(r.status_code)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


"""
    解析网页，定位相关电影信息
    电影名，评分，评论人数，发行年份，地区，类型，人员，名句
"""


def getDatas(html):
    soup = BeautifulSoup(html, 'html.parser')
    movie_list = soup.find_all('div', class_='item')
    for movie in movie_list:
        try:
            # 电影名
            title = movie.find('span', class_='title').text
            all = movie.find('div', class_='bd')
            content = all.p
            # 人员
            person = content.find('br').previous_sibling.strip().split()
            person = ' '.join(person)
            # 年数，地区，类型
            other = content.find('br').next_sibling.split('/')
            if len(other) == 3:
                year = other[0].strip()
                area = other[1].strip()
                types = other[2].strip()
            else:
                year = ''.join(other[0:-2]).strip()
                area = other[-2].strip()
                types = other[-1].strip()
            # 评分
            score = all.find('span', class_='rating_num').text
            # 评论人数
            number_of_comment = re.findall(r'\d+', all.div.text.split()[1])[0]
            # 名句
            if all.find('p', class_='quote'):
                quote = all.find('p', class_='quote').text.strip()
            else:
                quote = ""
            data = [title, score, number_of_comment, year, area, types, person, quote]
            saveToCSV(data)  # 存入CSV文件
            time.spleet(1)  # 防止爬取太快
        except:
            pass

"""
    将信息存入CSV文件
"""
def saveToCSV(data):
    with open('temp.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def main():
    saveToCSV(['电影名','评分','评论人数','发行年份','地区','类型','人员','名句'])
    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        html = getHtml(url)
        getDatas(html)
        print(i)


if __name__ == '__main__':
    main()
