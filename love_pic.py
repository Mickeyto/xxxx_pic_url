#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import getopt
import time
import re
import hashlib
from urllib.parse import parse_qs
from multiprocessing.pool import Pool
import requests

headers = {'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
           'Accept': 'image/webp,*/*', 'TE': 'Trailers', 'Cache-Control': 'no-cache',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}
error_page = []
save_file_path = './Images'


def match_title_url(url):
    s_index = url.rfind('&itemName')
    new_url = url[:s_index]
    title = parse_qs(url)['itemName'][0]

    return {"title": title, "url": new_url}


def get_pic_url_list(page):
    s_url = 'http://sex8.cc/forum-158-' + str(page) + '.html'
    print('Url', s_url)

    r = requests.get(f'{s_url}', headers=headers).text

    ru = '<a href="thread-(\d+)-1-' + str(page) + '.html"\s*[style]*[^>]*\s*onclick="atarget\(this\)"'
    matches = re.findall(ru, r)

    id_list = []
    pic_urls = []
    id_list = list(set(matches))

    list_len = len(id_list)
    print(list_len)

    if list_len == 0:
        error_page.append(page)
    else:
        for i in id_list:
            urls = get_pics(i, page)
            pic_urls += urls

    return pic_urls


def get_pics(pid, page):
    url_list = []

    if pid == '11876815':
        return []

    s_url = 'http://sex8.cc/thread-' + str(pid) + '-1-' + str(page) + '.html'

    print("pic_url:", s_url)

    # if s_url != 'http://sex8.cc/thread-8971031-1-311.html':
    r = requests.get(f'{s_url}', headers=headers).text

    matches_list = re.findall('\s+file="(.*?)"', r)
    match_ti = re.findall('<span\sid="thread_subject">(.*)</span>', r)
    if len(match_ti) < 1:
        match_ti = re.findall('<h1 class="ph z">(.*)</h1>', r)

    title = match_ti[0]

    url_arr = []
    url_list = list(set(matches_list))

    for i in range(len(url_list)):
        ti = url_list[i] + "&itemName=" + title
        url_arr += [ti]

    return url_arr


def write_urlfile(url):
    with open(f'./ch_sexual_love_urls.txt', 'a+') as f:
        f.write(url + "\n")
        f.close()


def download_pic(url):
    pic_info = match_title_url(url)

    print('Downloading：', pic_info['url'])

    # write url
    write_urlfile(pic_info['url'])

    s = requests.get(pic_info['url'], headers=headers, stream=True)
    # 下载图片的保存路径
    image_path = "./ch_sexual_love/Images/" + pic_info['title'] + '/'

    if not os.path.isdir(image_path):
        os.makedirs(image_path)

    file_name = hashlib.md5(url.encode('utf-8')).hexdigest()

    with open(f'{image_path}/{file_name}.jpg', 'wb') as f:
        # for data in s.iter_content(128):
        f.write(s.content)


def write_page_file(start_page, end_page):
    content = (str(start_page) + '-' + str(end_page)).encode('utf-8')
    with open(f'./page_love_history.txt', 'wb') as f:
        # for data in s.iter_content(128):
        f.write(content)


if __name__ == '__main__':
    print('开始获取图片地址')

    start_page = 0
    end_page = 1
    opts, args = getopt.getopt(sys.argv[1:], "hs:e:")

    for cmd, arg in opts:
        if cmd in ("-s"):
            start_page = int(arg)
        if cmd in ("-e"):
            end_page = int(arg) + 1

    print("start_page", start_page)
    print("end_page", end_page)

    write_page_file(start_page, end_page)

    pic_list = []
    for i in range(start_page, end_page):
        pic_list += get_pic_url_list(i)

    print('获取完毕，开始下载图片...')

    start_time = time.time()
    pool = Pool(10)
    pool.map_async(download_pic, pic_list)
    pool.close()
    pool.join()

    print(error_page)
    print(f'Down done\n 耗时：{time.time() - start_time}秒')
