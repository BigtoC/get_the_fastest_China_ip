# coding = utf-8

import os
import re
import socket
from getIP import dispatch, headers
import requests
import threading
import queue
import urllib3

urllib3.disable_warnings()


class IP:
    def __init__(self):
        self.ip = -1
        self.port = -1
        self.speed = -1


ready_to_ping = []
selected = []
counter = 0

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
    threads = []

    for r in ready_to_ping:
        qa.put(r)

    for i in range(len(ready_to_ping)):
        ta = threading.Thread(target=analyze_ip, args=(qa,))
        ta.daemon = True
        threads.append(ta)

    for th in threads:
        th.start()

    qa.join()


def analyze_ip(qa):

    while True:
        try:
            tmp = qa.get(True, 1)
        except queue.Empty:
            break
        # tmp = qa.get()
        ip = tmp.ip
        port = tmp.port
        global selected

        global counter
        counter += 1
        c = counter
        # print('{} Pinging {}'.format(counter, ip))

        timeout = '30'  # For filtering the IPs that the response time more that this time unit
        result = os.popen('ping -n 3 -w {} {}'.format(timeout, ip)).read()

        lost = re.search(lost_regex, result).group(0)

        if lost == '0%':

            # 用网易云的歌来测试ip和端口能不能用，歌曲：BINGBIAN病变 (女声版) 鞠文娴
            url_for_testing = 'http://music.163.com/song?id=543607345&userid=74549500'
            # QQ音乐，僕が死のうと思ったのは - 中島美嘉 (なかしま みか)
            backup_url = 'https://y.qq.com/n/yqq/song/00259rMK3PfBLS.html'
            # 虾米，The Blower's Daughter - Damien Rice
            backup_url_2 = 'https://www.xiami.com/mv/K6YXRW?spm=a1z1s.3521865.23309997.3.Vc8kEs'
            test_url = [url_for_testing, backup_url]
            r = requests.session()
            r.keep_alive = False

            try:
                status = r.get(url=test_url[counter % 2],
                               headers=headers,
                               proxies={"http": str(ip) + ':' + str(port)},
                               timeout=5)
            except requests.exceptions.ChunkedEncodingError:
                status = r.get(url=backup_url_2,
                               headers=headers,
                               proxies={"http": str(ip) + ':' + str(port)},
                               timeout=5)
            except requests.exceptions.RequestException:
                status = -1

            # print('{} requested {}:{}'.format(counter, ip, status))

            if type(status) is not int:
                if status.status_code == 200:
                    if c == len(ready_to_ping) - 1:
                        print()
                    # tmp_ip = re.search(ip_regex, result).group(0)
                    # average = re.search(average_rex, result)
                    # tmp_speed = str(re.sub('\D', '', str(average)))
                    speed = status.elapsed.total_seconds()

                    info = IP()
                    info.ip = ip
                    info.port = port
                    info.speed = speed
                    # print('{}:{} is good'.format(c, ip))
                    selected.append(info)

        qa.task_done()


def return_ip():
    for_return = []
    selected.sort(key=lambda x: x.speed)
    print('Finding the best from {} qualified IPs'.format(len(selected)))

    selected_ip = selected[0]
    for_return.append(selected_ip)

    if len(selected) > 1:
        backup_ip = selected[1]
        for_return.append(backup_ip)

    return for_return

# os.system('ping -n 4 {}'.format(ip))
