import os
import json
import requests
from math import ceil
from time import sleep
from lxml import etree
from threading import Thread, Lock
from bs4 import BeautifulSoup
from selenium import webdriver
from you_get import common
from multiprocessing import Pool
from concurrent.futures.thread import ThreadPoolExecutor


def download_video(url, save_path):
    # 线程锁
    # lock = Lock()
    # lock.acquire()
    common.any_download(url=url, info_only=False, output_dir=save_path, merge=True)
    # lock.release()


class DownloadBiliVideo(Thread):
    def __init__(self, url, save_path):
        super().__init__()
        self._url = url
        self._save_path = save_path
        self._lock = Lock()

    def run(self):
        self._lock.acquire()
        common.any_download(url=self._url, info_only=False, output_dir=self._save_path, merge=True)
        self._lock.release()


def do_soup(content):
    soup = BeautifulSoup(''.join(content), "html.parser")
    v_list = soup.find('ul', class_='cube-list')
    v_url = v_list.findAll('li')
    urls = []
    for v in v_url:
        v_u = v.find("a").get("href")
        if v_u[0:2] == '//':
            v_u = 'https:' + v_u
        urls.append(v_u)
    return urls


def get_mid(browser, up_name):
    search_url = "https://search.bilibili.com/all?keyword=" + str(up_name)
    browser.get(search_url)
    sleep(2)
    # content = browser.page_source
    html = etree.HTML(browser.page_source)
    href = html.xpath('//*[@class="user-item"]/div/a/@href')[0]
    mid = href.split('?')[0].split('/')[-1]
    return mid


"""
    download videos by you-get
"""


def do_download(urls, save_path):
    """test1 单线程循环"""
    for url in urls:
        try:
            download_video(url, save_path)
            sleep(3)
        except:
            continue
    print("视频下载完成！")
    print("已下载%d个视频，视频保存在%s" % (len(urls), save_path))
    exit()
    """test2 线程池"""
    # thread_pool = ThreadPoolExecutor(max_workers=2)
    # for url in urls:
    #     future = thread_pool.submit(download_video, url, save_path)
    #     print(future.result())
    # thread_pool.shutdown(wait=True)
    """test3 多线程"""
    # threads = []
    # for u in urls:
    #     t = DownloadBiliVideo(u)
    #     t.start()
    #     threads.append(t)
    # for t in threads:
    #     t.join()
    """test4 进程池"""
    # pool =Pool(2)
    # for url in urls:
    #     pool.map(do_download, url, save_path)
    #     pool.close()
    #     pool.join()


"""
    create a browser object
"""


def get_browser():
    driver_path = r'chromedriver/chromedriver'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/79.0.3945.88 Safari/537.36 "
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=%s' % user_agent)
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    try:
        browser = webdriver.Chrome(executable_path=driver_path, options=options)
        return browser
    except:
        print("browser 启动失败")
        exit()


"""
    通过selenium获取up主视频链接
"""


def get_urls_by_selenium(mid):
    browser = get_browser()
    url = "https://space.bilibili.com/" + str(mid) + "/video?tid=0&keyword=&order=pubdate"
    urls = []
    for i in range(4):
        browser.get(url + "&page=" + str(i + 1))
        sleep(3)
        content = browser.page_source
        res = do_soup(content)
        urls.extend(res)
    return urls


"""
    do requests
"""


def get_url_response(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print("获取链接资源失败...")
        exit()
    return resp


"""
    get video urls form up's mid
"""


def get_up_video_urls(mid):
    urls = []
    info_url = "https://api.bilibili.com/x/space/arc/search?mid=" + \
               str(mid) + "&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
    resp = get_url_response(info_url)
    try:
        info = json.loads(resp.text)
        v_list = info['data']['list']['vlist']
        count = info['data']['page']['count']
        if count > 0:
            page_size = info['data']['page']['ps']
            page_num = ceil(count / page_size)
            for i in range(page_num):
                url = "https://api.bilibili.com/x/space/arc/search?mid=" + \
                      str(mid) + "&ps=30&tid=0&pn=" + str(i + 1) + "&keyword=&order=pubdate&jsonp=jsonp"
                resp = get_url_response(url)
                sleep(1.5)
                info = json.loads(resp.text)
                v_list = info['data']['list']['vlist']
                for v in v_list:
                    url = "https://www.bilibili.com/video/" + str(v['bvid'])
                    urls.append(url)
        return urls
    except:
        print("json解析失败！")
        exit()


def main(up_name, save_path):
    try:
        mkdir = lambda x: os.makedirs(x) if not os.path.exists(x) else True
        mkdir(save_path)
    except PermissionError:
        print("no permission to mkdir")
        exit()
    browser = get_browser()
    mid = get_mid(browser, up_name)
    urls = get_up_video_urls(mid)
    do_download(urls, save_path)


if __name__ == '__main__':
    main(up_name="欣小萌", save_path="xxm")
