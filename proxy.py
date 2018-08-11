#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests                 # 读取网页
from bs4 import BeautifulSoup   # 解析网页
import random                   # 随机选择代理Ip

_urlip = 'http://www.xicidaili.com/nt/'         # 提供代理IP的网站
_headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

#--获得代理IP列表
def get_ip_list(urlip=_urlip, headers=_headers):
    web_data = requests.get(urlip, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for k in range(1, len(ips)):
        ip_info = ips[k]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

#-从代理IP列表里面随机选择一个
def get_random_proxies(ip_list=get_ip_list()):
    proxy_ip = random.choice(ip_list)
    proxies = {'http': 'http://' + proxy_ip}
    print(proxies)
    return proxies

if __name__=='__main__':
    print(get_random_proxies())