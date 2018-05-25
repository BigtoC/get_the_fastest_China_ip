# coding = utf-8

import os
import re
from getIP import dispatch, headers
import requests
import threading
import queue


class IP:
    def __init__(self):
        self.ip = -1
        self.port = -1
        self.speed = -1


ready_to_ping = []
selected = []
# counter = 0

lost_regex = r'\w+%'
# ip_regex = r'\d+\.\d+\.\d+\.\d+'
average_rex = 'Average = \d+ms|平均 = \d+ms'


def thread_get_ip(urls):
    qg = queue.Queue()
    for u in urls:
        qg.put(u)

    for url in urls:
        print('Requesting {}'.format(url))
        tg = threading.Thread(target=get_all_ip, args=(qg, ))
        tg.daemon = True
        tg.start()

    qg.join()


def get_all_ip(qg):
    while True:
        try:
            url = qg.get(True, 1)
        except queue.Empty:
            break

        global ready_to_ping
        ip_port = dispatch(url)
        for item in ip_port:
            ready_to_ping.append(item)
        qg.task_done()


def thread_analyze():
    global selected
    print('\nPinging total {} IPs...\n'.format(len(ready_to_ping)))
    qa = queue.Queue()

    for r in ready_to_ping:
        qa.put(r)

    for i in range(len(ready_to_ping)):
        ta = threading.Thread(target=analyze_ip, args=(qa,))
        ta.daemon = True
        ta.start()

    qa.join()


def analyze_ip(qa):

    while True:
        try:
            tmp = qa.get(True, 1)
        except queue.Empty:
            break

        ip = tmp.ip
        port = tmp.port
        global selected

        # global counter
        # counter += 1
        # print('{} Pinging {}'.format(counter, ip))

        timeout = 50  # For filtering the IPs that the response time more that this time unit
        result = os.popen('ping -n 3 {} -w {}'.format(ip, timeout)).read()

        # 用网易云的歌来测试ip和端口能不能用，歌曲：BINGBIAN病变 (女声版) 鞠文娴
        url_for_testing = 'http://music.163.com/song?id=543607345&userid=74549500'
        # QQ音乐，僕が死のうと思ったのは 中島美嘉 (なかしま みか)
        backup_url = 'https://y.qq.com/n/yqq/song/00259rMK3PfBLS.html'

        try:
            status = requests.get(url=url_for_testing,
                                  headers=headers,
                                  proxies={"http": str(ip) + ':' + str(port)}).status_code
        except requests.exceptions.ChunkedEncodingError:
            status = requests.get(url=backup_url,
                                  headers=headers,
                                  proxies={"http": str(ip) + ':' + str(port)}).status_code
        except requests.exceptions.ProxyError:
            status = -1

        lost = re.search(lost_regex, result).group(0)

        if lost == '0%' and status == 200:
            # tmp_ip = re.search(ip_regex, result).group(0)
            average = re.search(average_rex, result)
            tmp_speed = int(re.sub('\D', '', average.group()))

            info = IP()
            info.ip = ip
            info.port = port
            info.speed = tmp_speed
            # print('{} is good'.format(ip))
            selected.append(info)
        qa.task_done()


def return_ip():
    for_return = []
    selected.sort(key=lambda x: x.speed)
    print('Finding the best from {} qualified IPs'.format(len(selected)))

    selected_ip = selected[0]
    backup_ip = selected[1]

    for_return.append(selected_ip)
    for_return.append(backup_ip)

    return for_return

# os.system('ping -n 4 {}'.format(ip))
