## Get the fastest China IP address from multiple websites
## 从网上爬取中国ip，选取速度最快的

#### 需求性：中国大陆境外使用国内的音乐软件（网易云、虾米、QQ等）因为海外地区没有版权无法播放
#### 根属性：不在中国大陆境内
#### 解决力：翻墙回国内 || 网上找代理服务器
#### 损益比：两个方法都能解决问题，但是市面上的选择太多且不知道网速如何要逐个去试，麻烦
<br>

瞎逼逼完了就随便讲一下这几行垃圾代码能干嘛吧：<br>
首先，有一个小爬虫从三个网站爬了N个ip和对应的端口（N可以自己改），<br>
其次，逐个ping这些ip，用正则获得丢包率，<br>
然后，选出丢包率为0的ip，用requests模块测试这个代理地址的响应时间，<br>
最后，比较出响应时间最少的ip并print它的ip、端口<br>

<br>
下面是我自己的输出结果（实际输出因应当时的网络环境和爬到的ip而有所不同）<br>
    

Requesting http://cn-proxy.com/<br>
Requesting http://free-proxy.cz/zh/proxylist/country/CN/all/ping/all<br>
Requesting https://www.kuaidaili.com/free/intr/<br>
Requesting http://www.xicidaili.com/nt/<br>
Got 0 IPs from cn-proxy.com<br>
Got 0 IPs from free-proxy.cz<br>
Got 200 IPs from xicidaili.com<br>
Got 30 IPs from kuaidaili.com<br>
<br>
Pinging total 230 IPs...<br>
<br>
Finding the best from 20 qualified IPs<br>
<br>
The best ip address is: <br>
218.108.7.98<br>
Its port number is: <br>
3128<br>
Its response time is: <br>
0.231226 seconds<br>
This is for backup: 120.26.110.59:8080<br>
It takes 74 seconds<br>
(/*^o^/*)

