# -*- coding-8 -*-
import requests
from bs4 import BeautifulSoup


def tyc_comp(keyword):

    params = {
        "key": keyword,
    }
    sorted(params.items(), key=lambda d: d[0])

    url = "https://www.tianyancha.com/search"
    headers = {
        "Host": "www.tianyancha.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36",
        "connection": "keep-alive",
        "cache-control": "max-age=0",
        "accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookies": "aliyungf_tc=AQAAAAOlzRubXgcA1LKft1/wU4VIaYp/; csrfToken=EHWavLwR-zn0P-jxwoRyzCPB; jsid=SEM-BAIDU-PZ0703-VIP-000001; TYCID=2a0bfc60c28c11ea80895553db3bdc5e; undefined=2a0bfc60c28c11ea80895553db3bdc5e; ssuid=4945590262; bannerFlag=false; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1594371786; _ga=GA1.2.812266930.1594371787; _gid=GA1.2.902258854.1594371787; relatedHumanSearchGraphId=2336231932; relatedHumanSearchGraphId.sig=IjFchBaMMTSRS4rEVo655Qy0yz81-BAifdEk_Pq_lvk; refresh_page=0; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1594372360; _gat_gtag_UA_123487620_1=1",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.88 Safari/537.36",
    }
    request = requests.get(url=url, params=params, headers=headers)
    if request.status_code != 200:
        print("搜索请求失败")

    # print(request.text)
    # exit()

    # ''.join(doc) 将list doc 转换成字符串
    soup = BeautifulSoup(''.join(request.text), "html.parser")
    try:
        subUrl = soup.find('div', class_='result-list').select(".content")[0].select(".header")[0].find('a').get('href')
    except:
        print("cookie失效")
        exit()
    if subUrl == '':
        print("没有找到：" + keyword)
        exit()
    detailReq = requests.get(url=subUrl, params=params, headers=headers)
    if detailReq.status_code != 200:
        print("内容请求失败")
        exit()
    detailSoup = BeautifulSoup(''.join(detailReq.text), "html.parser")
    detailTable = detailSoup.find('div', id='_container_baseInfo').findAll('table')[1]
    # 注册资金
    registeredCapital = detailTable.findAll('tr')[0].findAll('td')[1].find('div').get_text()
    # 成立日期
    registeredTime = detailTable.findAll('tr')[1].findAll('td')[1].find('div').get_text()
    # 统一社会信用代码
    registeredCode = detailTable.findAll('tr')[2].findAll('td')[1].get_text()
    # 工商注册号
    businessRegistrationCode = detailTable.findAll('tr')[2].findAll('td')[3].get_text()
    # 纳税人识别号
    taxpayerIdentificationCode = detailTable.findAll('tr')[3].findAll('td')[1].get_text()
    # 组织机构代码
    organizationCode = detailTable.findAll('tr')[3].findAll('td')[3].get_text()
    # 公司类型
    companyType = detailTable.findAll('tr')[4].findAll('td')[1].get_text()
    # 行业
    industry = detailTable.findAll('tr')[4].findAll('td')[3].get_text()
    # 注册地址
    registeredAddress = detailTable.findAll('tr')[9].findAll('td')[1].get_text()
    # 经营范围
    businessScope = detailTable.findAll('tr')[10].findAll('td')[1].get_text()
    detail = {
        "注册资金": registeredCapital,
        "成立日期": registeredTime,
        "统一社会信用代码": registeredCode,
        "工商注册号": businessRegistrationCode,
        "纳税人识别号": taxpayerIdentificationCode,
        "组织机构代码": organizationCode,
        "公司类型": companyType,
        "行业": industry,
        "注册地址": registeredAddress,
        "经营范围": businessScope,
    }
    print(detail)
    exit()


tyc_comp("百度")
