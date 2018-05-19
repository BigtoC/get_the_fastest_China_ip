import analyzeIP
import time

urls = ['http://cn-proxy.com/',
        'http://free-proxy.cz/zh/proxylist/country/CN/all/speed/level3/1',
        # 'https://www.kuaidaili.com/free/intr/'  # 快代理的ip虽然快，但是在网易云测试过都不能用，this website sucks
        ]
good_ip = []


def compare_ips():
    good_ip.sort(key=lambda x: (x["speed"]), reverse=True)


def print_result():
    compare_ips()  # TODO why do you write a line function...
    if good_ip[0]["ip"] and good_ip[0]["speed"] and good_ip[0]["port"] != -1:
        print('The best ip address is: \n{}'.format(good_ip[0]["ip"]))
        time.sleep(0.5)
        print('Its port number is: \n{}'.format(good_ip[0]["port"]))
        time.sleep(0.5)
        print('Its response time is: \n{}ms'.format(good_ip[0]["speed"]))
        time.sleep(0.5)
        print('(*^o^*)')
    else:
        # TODO exceptions instead of print string.
        print("Error T_T")


if __name__ == '__main__':

    for url in urls:
        # start = time.clock()
        analyzeIP.analyze_ip(url)
        selected_ip = analyzeIP.return_ip()
        good_ip.append(selected_ip)
        # end = time.clock()
        # print(end - start)

    print_result()

    print()  # TODO redundant
