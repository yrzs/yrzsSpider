# -*- coding-8 -*-
import json
import re
import time

import requests


def baidu_comp(keyword):

    params = {
        "q": keyword,
        "t": 0,
        "fl": 1,
        "castk": "LTE=",
        "v": int(round(time.time() * 1000))
    }
    sorted(params.items(), key=lambda d: d[0])

    url = "https://xin.baidu.com/s"
    headers = {
        "host": "xin.baidu.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36",
        "connection": "keep-alive",
        "cache-control": "max-age=0",
        "accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp," \
                  "image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "referer": "https://xin.baidu.com/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookies": "PSTM=1577629593; BAIDUID=55EC303297CE963163FDF0C1C2D5AC50:FG=1; "
                   "BIDUPSID=64138704602910CD649295EB714F77C1; log_guid=9f731cb9f883b10f9a6eb6fc0194b1b4; "
                   "BDPPN=547ab1857917129c9717cd05d6270448; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; "
                   "ZX_UNIQ_UID=c289a047d2069df54efeafb9257415bf; "
                   "ZX_HISTORY=%5B%7B%22visittime%22%3A%222020-07-06+18%3A49%3A57%22%2C%22pid%22%3A%22xlTM"
                   "-TogKuTwzdnPNz73ab0CbAr6Hf8Yugmd%22%7D%2C%7B%22visittime%22%3A%222020-06-18+12%3A54%3A27%22"
                   "%2C%22pid%22%3A%22xlTM-TogKuTwWt3heVemPOjiWG3zQwkk7wmd%22%7D%5D; "
                   "Hm_lvt_baca6fe3dceaf818f5f835b0ae97e4cc=1592456018,1593394426,1594031629,1594032598; "
                   "delPer=0; PSINO=5; BCLID=13048482020587173326; "
                   "BDSFRCVID=UhKOJeC62C4yjDcr0FsvhwS2PQ1aqmOTH6f3qok8GP5Dow02T4BoEG0PSf8g0Ku"
                   "-OLyYogKKKgOTHICF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; "
                   "H_BDCLCKID_SF=JJIHVC_yf-bJKROg-DTjh6PAM-R9BtQmJJrm_PT_3nOKhhQR547b0TDr0HQKb4r9Qg"
                   "-q0DOhabkWsUtGQ-nbD5D7j-5y0x-jLN7hVn0MW-KV8pRwWtnJyUPUbPnnBUcm3H8HL4nv2JcJbM5m3x6qLTKkQN3T"
                   "-PKO5bRh_CcJ-J8XMD863D; H_PS_PSSID=32100_1457_31669_32139_31254_32046_32231_31709_32111; "
                   "Hm_lpvt_baca6fe3dceaf818f5f835b0ae97e4cc=1594088511",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.116 Safari/537.36",
    }
    request = requests.get(url=url, params=params, headers=headers)
    if request.status_code != 200:
        return False
    content = re.findall(r'window.pageData\s*=\s*\{(.*?)\};', request.text)
    if len(content) == 0:
        return False
    resp = re.sub(r'(<(\\/)?em>|-)', '', content[0])
    resp = json.loads("{%s}" % resp)
    companys = resp.get("result", {}).get('resultList', [])
    if len(companys) == 0:
        return False
    return companys[0]


res = baidu_comp("百度")
print(res)
