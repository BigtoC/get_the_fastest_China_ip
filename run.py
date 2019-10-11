import analyzeIP
import time


urls = ['http://cn-proxy.com/',
        'http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all',
        'https://www.kuaidaili.com/free/intr/',  # 快代理的ip虽然快，但是在网易云测试过都不能用，this website sucks
        'http://www.xicidaili.com/nt/'
        ]


def print_result(selected):
    print()
    if selected[0].ip and selected[0].port and selected[0].speed != -1:
        print(f'The best ip address is: \n{selected[0].ip}')

        print(f'Its port number is: \n{selected[0].port}')

        print(f'Its response time is: \n{selected[0].speed} seconds')

        if selected[1] is not None:
            print(f'This is for backup: {selected[1].ip}:{selected[1].port}')

    else:
        print("Error T_T")


if __name__ == '__main__':

    start = time.process_time()

    analyzeIP.thread_get_ip(urls)  # First get all IPs and ports

    analyzeIP.thread_analyze()  # Then multi thread ping

    selected_ip = analyzeIP.return_ip()  # Get the selected IP's info

    end = time.process_time()

    print_result(selected_ip)
    print(f'It takes {int(end - start)} seconds')
    print(f'(*^o^*)')
    input(f'Press <enter> to exit...')
