# -*- coding-8 -*-
import requests


def py123(offNum):
    params = {
        "sort": '''{"update_at": -1}''',
        "filter": '''{}''',
        "paging": '''{"offset": ''' + str(offNum) + ''', "limit": 20}'''
    }
    sorted(params.items(), key=lambda d: d[0])

    url = "https://www.python123.io/api/v1/turtles"
    headers = {
        "Host": "www.python123.io",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "connection": "keep-alive",
        "cache-control": "max-age=0",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookies": "Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1596531940,1596596410; Hm_lpvt_6f63cfeea8c9a84040e2c4389f01bb91=1596596699",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36",
    }
    request = requests.get(url=url, params=params, headers=headers)
    if request.status_code != 200:
        print("请求失败")
    content = request.json()
    if content['code'] == 200:
        data = content['data']
        order = offNum + 1
        fo = open("a.txt", "a")
        for i in range(len(data)):
            fo.write(str(order) + ":" + data[i]['title'] + "  ： \n")
            fo.write(data[i]['code'] + "\n\n\n")
            # fo.close()
            order += 1
        print("完成第", offNum + 1, "-", offNum + 20, "条数据抓取")
    else:
        print("获取数据失败")


if __name__ == '__main__':
    offNum = 0
    num = 1520 * 20
    while offNum < num:
        py123(offNum)
        offNum += 20
