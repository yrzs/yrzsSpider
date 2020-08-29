# -*- coding-8 -*-
import json
from time import *
import requests
from bs4 import BeautifulSoup
from lxml import etree
import threading


"""
    知乎热榜
"""


def zhihu_hot():
    url = 'https://www.zhihu.com/billboard'
    headers = {
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36',
        'cookie': ''
    }
    zh_response = requests.get(url, headers=headers)
    if zh_response.status_code != 200:
        print("网页获取失败...")
    zh_response.encoding = 'utf-8'
    content = zh_response.text
    html = etree.HTML(content)
    result = html.xpath('//*[@id="root"]/div/main//a')
    zh_hot = []
    for li in result:
        try:
            num = li.xpath('./div[1]/div[1]/text()')[0]
            title = li.xpath('./div[2]/div[1]/text()')[0]
            hot = li.xpath('./div[2]/div[2]/text()')[0]
            zh_hot.append({int(num): title + "(" + hot + ")"})
        except Exception as e:
            print(e)
    return zh_hot


"""
    微博热搜
"""


def weibo_hot():
    url = 'https://s.weibo.com/top/summary'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36',
        'cookie': 'SINAGLOBAL=8853236457116.986.1595403593153; '
                  'SCF=AsQCgAHfXJr-mGJSxOeFpMMiVPEaj5p0IOh9_TtP7ztxiJCdPDITokXPbw0HaRnDSkO-LLSBiUN7p0IP56Ok3Lw.; '
                  'SUHB=0S7SQ8DfpxmdnG; _s_tentry=login.sina.com.cn; Apache=6339454521373.924.1596077193951; '
                  'ULV=1596077194033:3:3:1:6339454521373.924.1596077193951:1595466858956; UOR=www.baidu.com,'
                  's.weibo.com,www.baidu.com; WBStorage=42212210b087ca50|undefined; '
                  'webim_unReadCount=%7B%22time%22%3A1596093482480%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22'
                  '%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D; '
                  'SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh0nNmeIVGd5oLA3N9ffUe3; '
                  'SUB=_2AkMofvscdcNxrARQnvAUy27mboRH-jybq5LqAn7uJhMyAxh87n0wqSVutBF-XHL-23MvrAEqwgO5lX9m9UngfUwc; '
                  'login_sid_t=6dd746293e1a207e2ef3ba7d194519b3; cross_origin_proto=SSL '
    }
    wb_response = requests.get(url, headers=headers)
    if wb_response.status_code != 200:
        print("网页获取失败...")
    content = wb_response.text
    soup = BeautifulSoup(content, "html.parser")
    index_list = soup.find_all("td", class_="td-01")
    title_list = soup.find_all("td", class_="td-02")
    wb_hot = []
    for i in range(len(index_list)):
        item_index = index_list[i].get_text(strip=True)
        if item_index == "":
            item_index = "0"
        item_title = title_list[i].a.get_text(strip=True)
        if item_index != '0':  # 置顶不要了
            wb_hot.append({int(item_index): item_title})
    return wb_hot


"""
    抖音热点榜
"""


def douyin_hot():
    url = 'https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36',
        'cookie': ''
    }
    dy_response = requests.get(url, headers=headers)
    if dy_response.status_code != 200:
        print("请求失败")

    content = json.loads(dy_response.text)
    dy_hot = []
    for i in range(len(content["word_list"])):
        dy_hot.append({i + 1: content["word_list"][i]['word']})
    return dy_hot


"""
    百度热点榜
"""


def baidu_hot():
    url = 'http://top.baidu.com/buzz?b=1&fr=topindex'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36',
        'cookie': ''
    }
    bd_response = requests.get(url, headers=headers)
    if bd_response.status_code != 200:
        print("请求失败")
    bd_response.encoding = 'gbk'  # gbk编码
    content = bd_response.text
    soup = BeautifulSoup(content, "html.parser")
    index_list_top = soup.find_all("span", class_="num-top")
    index_list_normal = soup.find_all("span", class_="num-normal")
    index_list = index_list_top + index_list_normal
    index_title = soup.find_all("a", class_="list-title")
    bd_hot = []
    for i in range(len(index_list)):
        bd_hot.append({i + 1: index_title[i].get_text()})
    return bd_hot


"""
    今日头条热榜（APP）
"""


def toutiao_hot():
    url = 'https://api3-normal-c-lq.snssdk.com/api/news/feed/v88/?version_code=7.8.1&tma_jssdk_version=1.72.0.1&app_name=news_article&vid=F30FC7AD-EFFD-4D80-93F2-88C1D03C7002&device_id=37543420443&channel=App Store&resolution=750*1334&aid=13&ab_feature=794526,1538698,1662483&ab_version=668779,1863122,660830,662176,1859936,1417597,662099,1403339,668774,1870643,1853622,668775,1874958,1529255,1335891,1874925,1844807,1469498,1419049,1899475,1157750,1413879,1898624,1593455,1419598,1851965&ab_group=794526,1538698,1662483&openudid=495796b28e252f145f0bb253539f4dddc8e0a899&pos=5pe9vb/88Pzt3vTp5L+9p72/ewAweCoDeCUfv7GXvb2//vTp5L+9p72/ewAweCoDeCUfv7GXvb2/8fLz+vTp6Pn4v72nvayvrbOtpaisqaqtr6ukraSqr7GXvb2/8fzp9Ono+fi/vae9rq2zr6Wtqa+sr6qlr6yspa2psZe9vb/88Pzt0fzp9Ono+fi/vae9rq2zr6Wtqa+sr6qlr6yspa2psZe9vb/88Pzt0fLz+vTp6Pn4v72nvayvrbOtpaisqaqtr6ukraSqr7GXvb2/8fL+/PHC8fzp+O7pwu3y7r+9p73ml729vb2/6fTw+O7p/PDtv72nvayopKusra2tqq2zpK2orq2ppLGXvb29vb/t7/Lr9PP++L+9p72/eygEeywCegEcv7GXvb29vb/+9Onkv72nvb97ADB4KgN4JR+/sZe9vb29v/7y8u/59PP86fjL/PHo+O6/vae95pe9vb29vb2/8fLz+vTp6Pn4v72nvayvrbOtpaisqaqtr6ukraSqr7GXvb29vb29v/H86fTp6Pn4v72nva6ts6+lramvrK+qpa+srKWtqZe9vb294LGXvb29vb/8+fnv+O7uv72nvb97KAR7LAJ6ARx7ADB4KgN4JR91OCJ7JAt4ESd1DxZ7AAx1PAp0HA51OCJ7Jzd4BiB4Myt7JCJ4AS14GDF4BjB1OCJ7Jzd4BiB4Myt7JCJ4AS14GDF4BjB5JQF4ESe/l7294Jfg&cdid=3FEA617F-0641-4112-9105-95A24D25E68C&update_version_code=78112&idfv=F30FC7AD-EFFD-4D80-93F2-88C1D03C7002&ac=WIFI&os_version=13.5.1&ssmix=a&device_platform=iphone&iid=3324520118356047&ab_client=a1,f2,f7,e1&device_type=iPhone 7&idfa=524737FE-1186-4B1A-992A-0851F0057427&language=zh-Hans-CN&support_rn=4&image=1&list_count=7&count=20&tt_from=pull&latitude=30.2804212782118&category=news_hotspot&city=杭州市&last_refresh_sub_entrance_interval=817&loc_time=1596100070&refer=1&ad_ui_style={"van_package":130000042,"is_crowd_generalization_style":true}&refresh_reason=1&concern_id=&longitude=120.0851470269097&st_time=212&session_refresh_idx=3&strict=0&LBS_status=authroize&rerank=0&detail=1&client_extra_params={"lynx_version_json":"{\"ugc_common_lynx\":76400,\"ugc_lynx_native_hotboard_card\":74201,\"ugc_personal_page\":77400,\"ugc_lynx_wenda\":74600,\"lynx_city_channel\":76500,\"ugc_lynx_hotboard\":75502,\"ugc_lynx_survey\":76400,\"attach_post_card\":76800,\"new_local_forum_cell\":76200,\"learning_lynx_profile\":77700,\"new_local_stick_cell\":76300,\"tt_lynx_hotboard\":76903}","last_ad_position":-1,"playparam":"codec_type:1","sort_offset":"0"}&min_behot_time=1596100033&loc_mode=1&cp=59Fd202f8eEA5q1'
    headers = {
        'User-Agent': 'News 7.8.1 rv:7.8.1.12 (iPhone; iOS 13.5.1; zh_CN) Cronet',
        'cookie': 'history=alrvlFic6pJZXJCTWBmSmZt6KV6petpSz5LU3OKuy3H%2FreLeNTAxX2LnYHC4HC80M9K%2BgYn7EqsbiKc4wetQAxPvJf5LDAGX45Xi9t5yYOK%2BxNzC4HA57up1hb0MjNyXGBg4GC7HK%2BlzCB9qYr7E4wfSp3CsbYnDOfZLXD0cBy7HK04PqTnAxHOJTwBkiiRzDXcrE88ljlMglQy3tx4H2c54iMEBAAAA%2F%2F8%3D; odin_tt=8065e91725923a24c855ed0fd0c2df2b98df91b5b5515af9acb8864fb343ae571cb5b2052e8d9aab05a89e4f6909bfbd; install_id=3324520118356047; ttreq=1$b48c06afc027d15945793de1bdd17341427722ff; PIXIEL_RATIO=2; WIN_WH=375_590; SLARDAR_WEB_ID=cc53e21c-a3f3-4fa7-8f64-a8a0ba044af8'
    }
    tt_response = requests.get(url, headers=headers)
    if tt_response.status_code != 200:
        print("请求失败")
    content = json.loads(tt_response.text)
    content1 = json.loads(content['data'][1]['content'])
    hot_board_items = content1['raw_data']['hot_board_items']
    """今天头条本地的十条热点"""
    # local_items = content1['raw_data']['local_items']
    # local_tt_hot = []
    # for i in range(len(local_items)):
    #     local_tt_hot.append({i+1: local_items[i]['Title']})
    # print(local_tt_hot)
    tt_hot = []
    for i in range(len(hot_board_items)):
        tt_hot.append({i + 1: hot_board_items[i]['title']})
    return tt_hot


"""
    快手热榜（APP）
"""


def kuaishou_hot():
    url = 'https://apissl.gifshow.com/rest/n/search/home/hot?kcv=193&kpf=IPHONE&net=%E4%B8%AD%E5%9B%BD%E8%81%94%E9%80%9A_5&appver=7.6.30.2436&kpn=KUAISHOU&c=a&mod=iPhone9%2C1&sys=ios13.5.1&sh=1334&ver=7.6&isp=CUCC&did=1601D04B-2D14-4E5E-97D4-4F2ABC8FFE09&darkMode=false&browseType=1&sw=750&egid=DFPE39A11F53760E6EC2953F1EB8CCC7D0180FE35E554E3A28DE814C305BE535'
    data = '__NS_sig3=2196747298da28994371cef24c26b0b3cdbab3876f&client_key=56c3713c&country_code=cn&cs=false&global_id=DFPE39A11F53760E6EC2953F1EB8CCC7D0180FE35E554E3A28DE814C305BE535&kuaishou.api_st=&language=zh-Hans-CN%3Bq%3D1%2C%20en-CN%3Bq%3D0.9%2C%20zh-Hant-CN%3Bq%3D0.8%2C%20io-CN%3Bq%3D0.7&sig=9e6f8331537c0cc646a6286611af7612&startSessionId=344A43BE-E1BE-45B2-9E01-5AC82DF00D54&token='
    headers = {
        'Host': 'apis1.gifshow.com',
        'Accept': 'application/json',
        'User-Agent': 'kwai-ios',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'X-REQUESTID': '159617684530850617',
        'Cookie': 'region_ticket=RT_7B0DC62FA97143BFED480EFFA027516B8984FF553003A508F6187CDA7C49E',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8, io-CN;q=0.7',
        'Content-Length': '381',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    ks_response = requests.post(url, data=data, headers=headers, timeout=5)
    if ks_response.status_code != 200:
        print("请求失败")
    content = ks_response.json()
    ks_hot = []
    for i in range(len(content['hots'])):
        ks_hot.append({i + 1: content['hots'][i]['keyword'] + " (热度：" + str(content['hots'][i]['hotValue']) + ")"})
    return ks_hot


"""
    天涯热帖
"""


def tianya_hot():
    url = 'https://bbs.tianya.cn/api?method=bbs.ice.getHotArticleList&params.pageSize=40&params.pageNum=1&var=apiData' \
          '&_r=0.9757292205705086&_=' + str(int(time())) + '000'
    headers = {
        'User-Agent': 'News 7.8.1 rv:7.8.1.12 (iPhone; iOS 13.5.1; zh_CN) Cronet',
        'cookie': 'ASL=18474,0000l,73c7b142; tianya1=12980,1596165034,1,86400; __cid=CN; ADVC=38b50952a0f5d4; '
                  'ADVS=38b50952a0f5d4; __asc=46381b20173a2d9937a491a612f; __auc=46381b20173a2d9937a491a612f; '
                  '__guid=1272401424; __guid2=1272401424; __ptime=1596165319547; '
                  'Hm_lvt_bc5755e0609123f78d0e816bf7dee255=1596165047,1596165050,1596165252,1596165320; '
                  'Hm_lpvt_bc5755e0609123f78d0e816bf7dee255=1596165320; time=ct=' + str(int(time())) + '.000'
    }
    ty_response = requests.get(url, headers=headers)
    if ty_response.status_code != 200:
        print("请求失败")
    content = ty_response.text.strip("var apiData = ")
    content = json.loads(content)
    row = content['data']['rows']
    ty_hot = []
    for i in range(len(row)):
        ty_hot.append({i + 1: row[i]['title']})
    return ty_hot


"""
    贴吧热议
"""


def tieba_hot():
    url = 'https://tieba.baidu.com/hottopic/browse/topicList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'cookie': 'PSTM=1595399629; BAIDUID=C96A7585E9B3E13A5D5CCE177C421D99:FG=1; '
                  'BIDUPSID=FDAB1B2BA70B4D41DEB70D4B18AF06AD; TIEBA_USERTYPE=2c5edaeff23e6b87289fde5c; '
                  'bdshare_firstime=1595493230416; MCITY=-179%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; '
                  'yjs_js_security_passport=20db979abf46575baa454b645c6d3218a1ed93ba_1596094764_js; delPer=0; '
                  'PSINO=5; H_PS_PSSID=32294_1452_32362_32328_32046_32393_32429_32115_32092_26350_32434_32261; '
                  'TIEBAUID=cb23caae14130a0d384a57f1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1595493231,1595921290,'
                  '1596173058; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1596173058; '
                  'st_data=1f11b1f6869840be68962bf2bef2201104df1427916375f1151a75461b93f8fa370f0e4f88cc817c76be91f973a81f11aa466b33d783535afa31fe343f22972e4419022340d6f90d2005221e725071daeee5028a4393825b112f1674b4caa68b501e636c50c04dad11601deb5ff4ea7d2246869a82c60724d84ab0518c0b1595; st_key_id=17; st_sign=b37c2602 '
    }
    tb_response = requests.get(url, headers=headers)
    if tb_response.status_code != 200:
        print("请求失败")
    content = tb_response.json()
    topic_list = content['data']['bang_topic']['topic_list']
    tb_hot = []
    for i in range(len(topic_list)):
        tb_hot.append({i + 1: topic_list[i]['topic_name']})
    return tb_hot


"""
    澎湃新闻24h最热
"""


def pengpai_24h_hot():
    url = 'https://app.thepaper.cn/clt/jsp/v6/channelContList.jsp?n=-6'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'cookie': 'JSESSIONID=54AB8156C5B64B1324B7BA786C8D5B5D; __ads_session=7pI/DnWRgwktqoQCvAA=; '
                  'SERVERID=srv-omp-ali-app8_80; route=ac205598b1fccbab08a64956374e0f11',
        'WD-UUID': '65998909-AA83-4C46-B660-D7F0C45DBA16',
    }
    pp_24h_response = requests.get(url, headers=headers)
    if pp_24h_response.status_code != 200:
        print("请求失败")
    content = pp_24h_response.json()
    contList = content['contList']
    pp_24h_hot = []
    for i in range(len(contList)):
        if 0 < i < len(contList) - 2:
            # print(contList[i]['name'])
            pp_24h_hot.append({i: contList[i]['name']})
    return pp_24h_hot


"""
    bilibili全站榜
"""


def bilibili_hot():
    url = 'https://www.bilibili.com/ranking'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'cookie': ''
    }
    bl_response = requests.get(url, headers=headers)
    content = bl_response.text
    soup = BeautifulSoup(content, "html.parser")
    index_list = soup.find_all("div", class_="num")
    index_title = soup.find_all("a", class_="title")
    bl_hot = []
    for i in range(len(index_list)):
        bl_hot.append({int(index_list[i].get_text()): index_title[i].get_text()})
    return bl_hot


"""
    参考消息(滚动新闻)
"""


def cankaoxiaoxi_hot():
    url = 'http://www.cankaoxiaoxi.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'cookie': ''
    }
    ckxx_response = requests.get(url, headers=headers)
    content = ckxx_response.text
    soup = BeautifulSoup(content, "html.parser")
    index_title = soup.find_all("li", class_="mar-r-15")
    ckxx_hot = []
    for i in range(len(index_title)):
        ckxx_hot.append({i + 1: index_title[i].find('a').get_text()})
    return ckxx_hot


class ResThread(threading.Thread):
    # 重写线程类
    def __init__(self, func, *args, **kwargs):
        super().__init__()  # 调用父类初始化方法
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        # 重写run方法, 用变量接收函数返回值
        self.result = self.func(*self.args, **self.kwargs)

    def getName(self):
        # 重写getName, 是哪个方法
        return str(self.func)[10:][0:-19]

    def getResult(self):
        # 增加获取结果函数, 待程序执行完毕之后才可获取
        if self.result:
            return self.result
        else:
            raise Exception("为执行或没有返回值...")


if __name__ == '__main__':
    begin_time = time()
    threads = [
        ResThread(zhihu_hot),
        ResThread(weibo_hot),
        ResThread(douyin_hot),
        ResThread(baidu_hot),
        ResThread(toutiao_hot),
        ResThread(kuaishou_hot),
        ResThread(tianya_hot),
        ResThread(tieba_hot),
        ResThread(pengpai_24h_hot),
        ResThread(bilibili_hot),
        ResThread(cankaoxiaoxi_hot),
    ]
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
    for i in range(len(threads)):
        print(threads[i].getName())
        print(threads[i].getResult())
    end_time = time()
    run_time = end_time - begin_time
    print('本次耗时：', round(run_time, 2), end='s')

