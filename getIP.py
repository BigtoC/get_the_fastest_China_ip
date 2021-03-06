import re
from bs4 import BeautifulSoup
from selenium import webdriver
import platform


class Tmp:
    def __init__(self):
        self.ip = -1
        self.port = -1


ip_regex = re.compile(r'\d+\.\d+\.\d+\.\d+')

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Cookie': '_ga=GA1.2.1328575144.1520154766; _gid=GA1.2.1755846933.1526619066',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch, base64',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    }


def get_html(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = None
    if 'Windows' in platform.system():
        driver = webdriver.Chrome(executable_path='venv\chromedriver.exe', chrome_options=chrome_options)
    elif 'Linux' in platform.system():
        driver = webdriver.Chrome(executable_path='venv\chromedriver_linux64', chrome_options=chrome_options)
    elif 'mac' in platform.system():
        driver = webdriver.Chrome(executable_path='venv\chromedriver_mac64', chrome_options=chrome_options)

    driver.get(url)
    source = BeautifulSoup(driver.page_source, 'lxml').prettify()
    driver.close()

    return source


def dispatch(url):
    dic = {}
    if 'cn-proxy' in url:
        dic = c_get_ip(url)
    if 'free-proxy' in url:
        dic = f_get_ip(url)
    if 'kuaidaili' in url:
        dic = k_get_ip(url)
    if 'xicidaili' in url:
        dic = x_get_ip(url)

    # dic['118.114.77.47'] = 8080
    # dic['39.134.68.23'] = 80
    return dic


def c_get_ip(url):
    html = get_html(url)

    ip_port = []

    port_regex = re.compile(r'<td>\n\s*\d+\n\s*</td>')

    all_ip = re.findall(ip_regex, html)
    tmp_port = re.findall(port_regex, html)

    all_port = []
    for p in tmp_port:
        p = re.sub(r'\D', '', p)
        all_port.append(p)

    for i in range(len(all_ip)):
        t = Tmp()
        t.ip = all_ip[i]
        t.port = all_port[i]
        ip_port.append(t)

    # for i in range(100):
    #     t = Tmp()
    #     t.ip = '39.137.77.66'
    #     t.port = '8080'
    #     ip_port.append(t)

    print(f'Got {len(ip_port)} IPs from cn-proxy.com')
    return ip_port


def f_get_ip(url):
    html = get_html(url)
    ip_port = []

    port_regex = re.compile(r'<span class="fport" style="">\n\s*\d+\n\s*</span>')
    tmp_ip = re.findall(re.compile(r'</script>\n\s*\d+\.\d+\.\d+\.\d+\n\s*</td>|'
                                   r'</script>\n\s*\d+\.\d+\.\d+\.\d+\n\s*</abbr>'), html)  # MDZZ
    tmp_port = re.findall(port_regex, html)

    all_ip = []
    all_port = []

    for i in tmp_ip:
        i = re.findall(r'\d+\.\d+\.\d+\.\d+', i)
        all_ip.append(i)

    for p in tmp_port:
        p = re.sub(r'\D', '', p)
        all_port.append(p)

    for i in range(len(all_ip)):
        t = Tmp()
        t.ip = all_ip[i][0]
        t.port = all_port[i]
        ip_port.append(t)

    print(f'Got {len(ip_port)} IPs from free-proxy.cz')
    return ip_port


def k_get_ip(url):  # Abandoned! Ignore this!
    ip_port = []
    page_num = 2  # change the number if you want get more ip addresses
    for i in range(page_num):
        url = 'https://www.kuaidaili.com/free/intr/{}/'.format(i+1)
        html = get_html(url)

        port_regex = re.compile(r'<td data-title="PORT">\n\s*\d+\n\s*</td>')
        all_ip = re.findall(ip_regex, html)
        tmp_port = re.findall(port_regex, html)

        all_port = []

        for p in tmp_port:
            p = re.sub(r'\D', '', p)
            all_port.append(p)

        for j in range(len(all_ip)):
            t = Tmp()
            t.ip = all_ip[j]
            t.port = all_port[j]
            ip_port.append(t)

    print(f'Got {len(ip_port)} IPs from kuaidaili.com')
    return ip_port


def x_get_ip(url):
    ip_port = []
    page_num = 2
    port_regex = re.compile(r'\s*<td>\n\s*\d+\n\s*</td>')

    for i in range(page_num):
        u = url + str(i+1)
        html = get_html(u)

        all_ip = re.findall(ip_regex, html)
        tmp_port = re.findall(port_regex, html)

        all_port = []
        for p in tmp_port:
            p = re.sub(r'\D', '', p)
            all_port.append(p)

        for j in range(len(all_ip)):
            t = Tmp()
            t.ip = all_ip[j]
            t.port = all_port[j]
            ip_port.append(t)

    print(f'Got {len(ip_port)} IPs from xicidaili.com')
    return ip_port


# if __name__ == '__main__':
#     url = 'http://www.xicidaili.com/nn/'
#     d = dispatch(url)
#     print(len(d))
#     print(d)

    # html = get_html(url)
    # file = open("2.html", "w", encoding='utf-8')
    # file.write(html)
    # file.close()
    # print(html)
    #
    # ip_port = f_get_ip(url)
    # print(ip_port)
    # print(len(ip_port))
    # r = requests.get('https://1.1.1.1', proxies={"http": "http://222.33.192.238:8118"})
    # print(r.status_code)

