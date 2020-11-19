import random
import re
from time import sleep
import requests
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver

"""
    create a browser object
"""


def get_browser():
    driver_path = r'chromedriver/chromedriver-bac'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/79.0.3945.88 Safari/537.36 "
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=%s' % user_agent)
    # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_argument('--headless')
    try:
        browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
        return browser
    except:
        print("browser 启动失败")
        exit()


def get_address_detail_by_job_url(browser, url):
    browser.get(url)
    # print('gz' in browser.current_url)
    # exit()
    content = browser.page_source
    # print(content)
    soup = BeautifulSoup(content, "html.parser")
    try:
        address = soup.find('div', class_='pos-area').get_text()[0:-5]
    except:
        address = soup.find('div', class_='pos_base_condition').get_text()[0:-5]
    detail = soup.find('div', class_='shiji').get_text()
    return {'address': address, 'detail': detail}


def get_address_detail_by_com_url(url):
    # browser = get_browser()
    # url = "https://entdict.58.com/enterpriselibrary/index/detail/1?qid=6392587996&uid=21379177318407&from=2"
    # browser.get(url)
    # content = browser.page_source
    # soup = BeautifulSoup(content, "html.parser")
    # print(content)
    # print(soup.find('div', id='fullText').get_text())
    # exit()
    response = get_url_response(url)
    text = response.text
    # print(text)
    content = re.findall(r'var __REACT_SSR_ = {[\s\S]*}]}} ;', text)
    # print(content)
    if len(content) == 0:
        return False
    resp = re.findall(r'regLocation\"\:\"([\s\S]*])', content[0])
    address = re.sub(r'","re([\s\S]*])', '', resp[0])
    # address = re.sub(r'","regStatus"([\s\S]*])', '', resp[0])

    print(address)

    content2 = re.findall(r'class="introduction_box"><p class=""><span>[\s\S]*]', text)
    if len(content2) == 0:
        return False
    resp2 = re.sub(r'class="introduction_box"><p class=""><span>', '', content2[0])
    detail = re.sub(r'<br/></span></p></div></div><div class="album">[\s\S]*]', '', resp2)

    print(detail)

    # exit()
    # soup = BeautifulSoup(content, "html.parser")
    # address = soup.find('p', class_="a_address").get_text()
    # detail = soup.find('div', class_="introduction_box").get_text()
    return {'address': address, 'detail': detail}


"""
    do requests
"""


def get_url_response(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print("获取链接资源失败...")
        exit()
    return resp


def get_page_size(browser):
    page = 1
    url = "https://gz.58.com/baiyun/job/pn" + str(page) + "/?key=%E5%A4%96%E8%B4%B8&classpolicy=job_B," \
                                                          "uuid_a3c816cdb61a451696026e7bc890bc7a,displocalid_1659,from_9224," \
                                                          "to_jump&final=1&PGTID=0d302408-0067-b08b-7ba6-118981d08514&ClickID=3 "
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, "html.parser")
    page_size = soup.find('i', class_="total_page").get_text()
    return page_size


def get_page_data(browser, page):
    url = "https://gz.58.com/baiyun/job/pn" + str(page) + "/?key=%E5%A4%96%E8%B4%B8&classpolicy=job_B," \
                                                          "uuid_a3c816cdb61a451696026e7bc890bc7a,displocalid_1659,from_9224," \
                                                          "to_jump&final=1&PGTID=0d302408-0067-b08b-7ba6-118981d08514&ClickID=3 "
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, "html.parser")
    job_name = soup.find_all("div", class_="job_name")
    comp_name = soup.find_all("div", class_="comp_name")
    data = []
    for i in range(len(job_name)):
        data.append(
            {
                "job_name": job_name[i].find('a').get_text().replace(" ", ""),
                "comp_name": comp_name[i].find('a').get_text().replace(" ", ""),
                "job_url": job_name[i].find('a').get("href"),
                "comp_url": comp_name[i].find('a').get("href"),
            }
        )
    return data


def main():
    browser = get_browser()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('白云区-外贸')
    xls_name = 'test.' + str(random.randint(0, 9)) + '.xls'
    page_size = int(get_page_size(browser))
    num = 0
    for i in range(page_size):
        data = get_page_data(browser, i + 1)
        for j in range(len(data)):
            try:
                worksheet.write(num, 0, label=data[j]['job_name'])
                worksheet.write(num, 1, label=data[j]['comp_name'])
                if bool(data[j]['job_url']):
                    res = get_address_detail_by_job_url(browser, data[j]['job_url'])
                    worksheet.write(num, 2, label=res['address'])
                    worksheet.write(num, 3, label=res['detail'])
            except:
                workbook.save(xls_name)
            # worksheet.write(num, 2, label=data[j]['job_url'])
            # worksheet.write(num, 3, label=data[j]['comp_url'])
            sleep(3)
            num += 1
            print(num)
            print(data[j]['job_name'])
        print(i + 1)
    workbook.save(xls_name)


if __name__ == '__main__':
    main()
