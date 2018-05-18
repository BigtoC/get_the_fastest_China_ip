# coding = utf-8

import os
import re
from getIP import dispatch

myip = {"ip": -1, "speed": -1, "port": -1}


def analyze_ip(url):

    ip_port = dispatch(url)

    print('Pinging ip...\n')
    # os.system('ping -n 4 {}'.format(ip))

    lost_regex = r'\w+%'
    ip_regex = r'\d+\.\d+\.\d+\.\d+'
    average_rex = u'Average = \d+ms|平均 = \d+ms'

    for key in ip_port:
        result = os.popen('ping -n 3 {}'.format(key)).read()

        lost = re.search(lost_regex, result).group(0)

        if lost == '0%':
            tmp_ip = re.search(ip_regex, result).group(0)
            average = re.search(average_rex, result)
            tmp_speed = int(re.sub('\D', '', average.group()))

            if myip["ip"] and myip["speed"] and myip["port"] == -1:
                myip["ip"] = tmp_ip
                myip["speed"] = int(tmp_speed)
                myip["port"] = ip_port[tmp_ip]

            elif tmp_speed < myip["speed"]:
                myip["ip"] = tmp_ip
                myip["speed"] = int(tmp_speed)
                myip["port"] = ip_port[tmp_ip]

            else:
                pass
        else:
            pass


def return_ip():
    return myip



