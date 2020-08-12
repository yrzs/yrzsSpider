# -*- coding-8 -*-
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from pynput.mouse import Button, Controller as c1
from bs4 import BeautifulSoup
import xlwt


# 构造滑动轨迹
def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


# 滑动划块（会被识别）
def do_actions(action, sli_ele):
    # 在滑块处按住鼠标左键
    action.click_and_hold(sli_ele)
    track = get_track(318)
    for i in track:
        # 相对鼠标当前位置进行移动
        action.move_by_offset(xoffset=i, yoffset=0).perform()
        # 释放鼠标
        action.reset_actions()
    # 执行动作
    action.perform()


def dy(username, password):
    url = "https://dy.feigua.cn/Rank/Area?period=month&province=11&city=121"
    driver_path = r'chromedriver/chromedriver'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/79.0.3945.88 Safari/537.36 "
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=%s' % user_agent)
    # 不加载图片,加快访问速度
    # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 设置为开发者模式，防止被识别出来使用了Selenium
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    '''------无界面模式------'''
    # options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    # options.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
    # options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # options.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
    # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
    # options.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败

    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    # 浏览器最大窗口（报错）
    browser.maximize_window()
    wait = WebDriverWait(browser, 10)
    browser.get(url)
    sleep(3)
    browser.find_element_by_class_name("js-show-phone").click()
    browser.find_element_by_name("tel").clear()
    browser.find_element_by_name("tel").send_keys(username)
    browser.find_element_by_name("pwd").clear()
    browser.find_element_by_name("pwd").send_keys(password)
    browser.find_element_by_class_name("js-account-logon").click()
    sleep(1)
    '''------划块验证------'''
    mouse = c1()
    trace = get_track(318)
    while True:
        sleep(1 + random.random())
        mouse.position = (810, 456)
        print(mouse.position)
        mouse.press(Button.left)
        sleep(1 + random.random())
        for d in trace:
            mouse.move(d, 0)
            sleep(random.random() / 10)
        sleep(1)
        mouse.release(Button.left)
        sleep(1)
        try:
            browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span/b[contains(text(),"验证通过")]')
            print('验证通过')
            break
        except:
            continue

    # # 选择拖动滑块的节点
    # sli_ele = browser.find_element_by_id('nc_1_n1z')
    # # ------------鼠标滑动操作------------
    # action = ActionChains(browser)
    # sli_ele.click()
    # do_actions(action, sli_ele)

    # 点击登录按钮
    browser.find_element_by_class_name("btn-login").click()

    browser.get(url)
    # 点击博主查找
    browser.find_element_by_xpath('//div[@id="mCSB_1_container"]/ul/li[3]').click()
    sleep(1)
    # 点击博主排行榜
    browser.find_element_by_xpath('//div[@id="mCSB_1_container"]/ul/li[3]/ul/li[3]').click()
    # 点击地区排行榜
    # browser.find_element_by_xpath('//div[@class="videos"]/div/ul/li[4]').click()
    # 点击月榜
    # browser.find_element_by_xpath('//div[@class="v-rank-content"]/div/div/div/button[3]').click()

    browser.get("https://dy.feigua.cn/Member#/Rank/Area?period=month&province=11&city=125&datecode=202007")

    for i in range(12):
        mouse.scroll(0, -50)
        sleep(3)

    # browser.refresh()

    '''------处理结果------'''
    # content = browser.page_source
    # print(content)
    # sleep(3)
    # browser.get("https://dy.feigua.cn/Member#/Rank/Area?period=week&province=11&city=123&datecode=20200803-20200809&page=2")
    content = browser.page_source
    # print(content)
    # ''.join(doc) 将list doc 转换成字符串
    soup = BeautifulSoup(''.join(content), "html.parser")
    tbody = soup.find("tbody", id="js-blogger-container")
    tr = tbody.findAll("tr")
    # print(len(tr))
    # rank_data = []
    # print(rank_data)
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('温州')
    for i in range(len(tr)):
        td = tr[i].findAll("td")
        [s.extract() for s in td[0]('em')]
        # 排名
        rank = td[0].get_text().strip()
        # 名称
        name = td[1].get_text().strip()
        # 飞瓜数据
        fg_data = td[2].get_text().strip()
        # 粉丝
        fans = td[3].get_text()
        # 平均点赞
        avg_likes = td[4].get_text().strip()
        # 平均评论
        avg_comment = td[5].get_text().strip()
        # 平均转发
        avg_relay = td[6].get_text().strip()
        # 详情链接
        link = "https://dy.feigua.cn/Member" + td[7].find("a").get('href')
        browser.get(link)
        sleep(6)
        detail = browser.page_source
        detailSoup = BeautifulSoup(''.join(detail), "html.parser")
        info = detailSoup.find('div', class_='info')
        # 抖音号
        dy_account = info.select("ul")[0].findAll("li")[0].get_text()
        data = {
            "排名": rank,
            "名称": name,
            "飞瓜数据": fg_data,
            "粉丝": fans,
            "平均点赞": avg_likes,
            "平均评论": avg_comment,
            "平均转发": avg_relay,
            "抖音号": dy_account,
        }
        # 写入excel
        # 参数对应 行, 列, 值
        worksheet.write(i, 0, label=data["排名"])
        worksheet.write(i, 1, label=data["名称"])
        worksheet.write(i, 2, label=data["飞瓜数据"])
        worksheet.write(i, 3, label=data["粉丝"])
        worksheet.write(i, 4, label=data["平均点赞"])
        worksheet.write(i, 5, label=data["平均评论"])
        worksheet.write(i, 6, label=data["平均转发"])
        worksheet.write(i, 7, label=data["抖音号"][4:])
        if i % 20 == 0:
            sleep(10)
    # 保存
    workbook.save('Excel_test.xls')
    #     if i > 2:
    #         break
    # print(rank_data)
    sleep(300)
    # browser.close()


if __name__ == "__main__":
    username = "your username"
    password = "your password"
    dy(username, password)
