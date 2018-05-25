import analyzeIP
import time


urls = ['http://cn-proxy.com/',
        'http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all',
        #  'https://www.kuaidaili.com/free/intr/',  # 快代理的ip虽然快，但是在网易云测试过都不能用，this website sucks
        'http://www.xicidaili.com/nt/'
        ]


def print_result(selected):
    print()
    if selected[0].ip and selected[0].port and selected[0].speed != -1:
        print('The best ip address is: \n{}'.format(selected[0].ip))
        time.sleep(0.5)
        print('Its port number is: \n{}'.format(selected[0].port))
        time.sleep(0.5)
        print('Its response time is: \n{}ms'.format(selected[0].speed))
        time.sleep(0.5)
        print('This is for backup: {}:{}'.format(selected[1].ip, selected[1].port))

    else:
        print("Error T_T")


if __name__ == '__main__':

    start = time.clock()

    analyzeIP.thread_get_ip(urls)  # First get all IPs and ports

    analyzeIP.thread_analyze()  # Then multi thread ping

    selected_ip = analyzeIP.return_ip()  # Get the selected IP's info

    end = time.clock()

    print_result(selected_ip)
    print('It takes {} seconds'.format(int(end - start)))
    print('(*^o^*)')
    input()
