import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform


ip_regex = re.compile(r'\d+\.\d+\.\d+\.\d+')


def get_html(url):
    print('Requesting {}'.format(url))
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    headers = {
        'User-agent': user_agent,
        'Cookie': '_ga=GA1.2.1328575144.1520154766; _gid=GA1.2.1755846933.1526619066',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }

    chrome_options = Options()
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

    # dic['118.114.77.47'] = 8080
    # dic['39.134.68.23'] = 80

    return dic


def c_get_ip(url):
    html = get_html(url)

    ip_port = {}

    port_regex = re.compile(r'<td>\n             \d+\n            </td>')
    print('Getting IP addresses from cn-proxy.com...')

    all_ip = re.findall(ip_regex, html)
    tmp_port = re.findall(port_regex, html)

    all_port = []
    for p in tmp_port:
        p = re.sub(r'\D', '', p)
        all_port.append(p)

    for i in range(len(all_ip)):
        ip_port[all_ip[i]] = all_port[i]

    return ip_port


def f_get_ip(url):
    html = get_html(url)
    ip_port = {}

    print('Getting IP addresses from free-proxy.cz...')

    port_regex = re.compile(r'<span class="fport" style="">\n         \d+\n        <\/span>')
    tmp_ip = re.findall(re.compile(r'</script>\n        \d+\.\d+\.\d+\.\d+\n       <\/td>|'
                                   r'</script>\n         \d+\.\d+\.\d+\.\d+\n        </abbr>'), html)  # MDZZ
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
        ip_port[all_ip[i][0]] = all_port[i]

    return ip_port


def k_get_ip(url):  # Abandoned! Ignore this!
    ip_port = {}
    page_num = 3  # change the number if you want get more ip addresses
    for i in range(page_num):
        url = 'https://www.kuaidaili.com/free/intr/{}/'.format(i+1)
        html = get_html(url)

        print('Getting IP addresses from kuaidaili.com...')

        port_regex = re.compile(r'<td data-title="PORT">\n           \d+\n          </td>')
        all_ip = re.findall(ip_regex, html)
        tmp_port = re.findall(port_regex, html)

        all_port = []

        for p in tmp_port:
            p = re.sub(r'\D', '', p)
            all_port.append(p)

        for i in range(len(all_ip)):
            ip_port[all_ip[i]] = all_port[i]

    return ip_port


# if __name__ == '__main__':
#     url = 'http://free-proxy.cz/zh/proxylist/country/CN/all/speed/level3'
#     html = get_html(url)
#     file = open("2.html", "w", encoding='utf-8')
#     file.write(html)
#     file.close()
#     print(html)
#
#     ip_port = f_get_ip(url)
#     print(ip_port)
#     print(len(ip_port))

