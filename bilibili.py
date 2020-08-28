from threading import Thread, Lock
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from you_get import common


class DownloadBiliVideo(Thread):
    def __init__(self, url):
        super().__init__()
        self._url = url
        self._lock = Lock()

    def run(self):
        self._lock.acquire()
        common.any_download(url=self._url, info_only=False, output_dir=r'video', merge=True)
        self._lock.release()


def main():
    url = "https://space.bilibili.com/16539048/video?tid=0&keyword=&order=pubdate"
    driver_path = r'chromedriver/chromedriver'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/79.0.3945.88 Safari/537.36 "
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=%s' % user_agent)
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    browser.get(url + "&page=1")
    sleep(2)
    content = browser.page_source
    soup = BeautifulSoup(''.join(content), "html.parser")
    v_list = soup.find('ul', class_='cube-list')
    # print(v_list)
    v_url = v_list.findAll('li')
    urls = []
    for v in v_url:
        v_u = v.find("a").get("href")
        if v_u[0:2] == '//':
            v_u = 'https:' + v_u
        urls.append(v_u)

    threads = []
    for u in urls:
        t = DownloadBiliVideo(u)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
