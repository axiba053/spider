#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 16:18
# @Author  : lxq
# @Email   :liuqiang053@126.com
# 豆瓣读书 大冰 乖摸摸头 评论 爬取

import requests
from lxml import etree
import pandas as pd
from collections import defaultdict
import time
import random
from fake_useragent import UserAgent

ua = UserAgent() #使用fake-Agent随机生成User-Agent，添加到headers
def get_douban_comments(number,page): #加书的编号number为参数
    head = {'User-Agent': ua.random}
    all = defaultdict(lambda :[]) # 新建字典，保存结果
    urls = ['https://book.douban.com/subject/'+ number +'/comments/hot?p={}'.format(str(i)) for i in range(1, page)]
    n = 0
    for url in urls:
        n += 1
        r = requests.get(url, headers=head).text
        s = etree.HTML(r)
        # tol_num = s.xpath('//*[@id="total-comments"]/text()')#总评论数
        comment = s.xpath('//*[@id="comments"]/ul/li/div[2]/p/span/text()') #评论内容
        people = s.xpath('//*[@id="comments"]/ul/li/div[2]/h3/span[2]/a/text()') # 评论者
        lianjie = s.xpath('//*[@id="comments"]/ul/li/div[2]/h3/span[2]/a/@href')  #评论者知乎主页
        # score = s.xpath('//*[@id="comments"]/ul/li[1]/div[2]/h3/span[2]/span[1]/@title')#评分有缺值，列表长度与其他不一致，得到的字典无法正确保存
        score1 = [s.xpath('//*[@id="comments"]/ul/li[{}]/div[2]/h3/span[2]/span[1]/@title'.format(str(i))) for i in range(1,len(people)+1)]
        score2 = [''.join(i) for i in score1] #评分（有的没有给出评分，故需单个依次提取）
        date = s.xpath('//*[@id="comments"]/ul/li/div[2]/h3/span[2]/span/text()') #评论日期
        agree = s.xpath('//*[@class="vote-count"]/text()') #多少人认为该条评论有用
        all['people'].extend(people)
        all['lianjie'].extend(lianjie)
        all['comment'].extend(comment)
        all['score'].extend(score2)
        all['agree'].extend([int(i) for i in agree])
        all['date'].extend(date)
        time.sleep(random.randint(5, 7)) #爬取间隔时间
        print('第%s页已完成' % str(n))
        # print(all)
    df = pd.DataFrame(all)
    df.to_excel('guaimomotou.xlsx')


if __name__ == '__main__':
    get_douban_comments('25984204', 788)