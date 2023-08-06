# coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/8/25.
# ---------------------------------
from utils.queue import PriorityQueue as Queue
from threading import Thread
import urllib2
import time
import datetime
from utils.encrypt import md5
import  urlparse
from pybloom import  BloomFilter,ScalableBloomFilter


_queue = Queue()
_size = 0


def spider_init(pool_size):
    '''初始化爬虫
    pool_size 线程池的大小
    '''
    print datetime.datetime.now(), "[Spider]:init...."
    global _size, _queue, _url_max_num, _proxy_list
    if _size == 0:
        _size = pool_size

        def run():
            def work():
                while 1:
                    fun = _queue.get().obj
                    if fun:
                        fun()
                    _queue.task_done()

            for i in range(0, _size):
                thread = Thread(target=work)
                thread.setDaemon(True)
                thread.start()

        run()


def spider_join():
    '''
    等待爬虫执行完成
    '''
    global _queue
    _queue.join()







class Spider(object):
    _url_buff = None

    def __init__(self, url, charset=None, data=None, headers=None, response_handle=None, timeout=3, retry_times=30,
                 retry_delta=3, http_proxy_url=None, force=False,priority=0):
        '''
            url   目标url
            charset   编码
            data   post的数据,字符串
            headers  自定义请求头,dict
            response_handle 采集结果处理函数
            timeout  超时时间,int,  比如:3
            retry_times 重试次数,int,比如3
            retry_delta   重试间隔,int
            http_proxy_url         代理ip,  "http://192.168.1.1:80"
            force         强制爬取,而不管有没有爬取过.
            priority      优先级,默认为0, 高优先级的会被优先爬取
        '''
        self.url = url
        self.data = data
        self.timeout = timeout
        self.retry_times = retry_times
        self.retry_delta = retry_delta
        self.response_handle = response_handle
        self.charset = charset
        self.headers = headers
        self.proxy = http_proxy_url
        self.priority = priority
        if not Spider._url_buff:
            Spider._url_buff = [BloomFilter(1000000)]
        global _queue
        if data:
            _hash = md5(url) + md5(data)
        else:
            _hash = md5(url)
        if not force:
            try:
                for bloomfilter in Spider._url_buff:
                    assert  _hash not in bloomfilter
            except:
                pass
            else:
                try:
                    Spider._url_buff[-1].add(_hash)
                except:
                    Spider._url_buff.append(BloomFilter(Spider._url_buff[-1].capacity+1000000))
                    Spider._url_buff[-1].add(_hash)
                _queue.put_priority(self._go,priority)
        else:
            _queue.put_priority(self._go,priority)

    def _go(self):
        def urllib2_get_httpproxy(ip, port):
            proxy = urllib2.ProxyHandler({'http': 'http://%s:%s' % (ip, port)})
            opener = urllib2.build_opener(proxy)
            return opener, "http", ip, port
        retry_times = self.retry_times
        url = self.url
        postdata = self.data
        timeout = self.timeout
        retry_delta = self.retry_delta
        for i in range(0, retry_times):
            try:
                if self.proxy:
                    proxy_info = urlparse.urlparse(self.proxy)
                    proxy_hostname = proxy_info.hostname
                    proxy = urllib2_get_httpproxy(proxy_hostname,80)
                    urllib2.install_opener(proxy)
                request = urllib2.Request(url)
                if self.headers:
                    request.headers = self.headers
                else:
                    request.headers = {"User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36\
(KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'}
                if self.charset:
                    response = urllib2.urlopen(request, data=postdata, timeout=timeout)
                    data = response.read().decode(self.charset, errors="ignore")
                    headers = response.info().dict
                else:
                    response = urllib2.urlopen(request, data=postdata, timeout=timeout)
                    data = response.read()
                    headers = response.info().dict
                if self.response_handle:
                    self.response_handle(data)
            except Exception as e:
                print datetime.datetime.now(), "[Spider]:%s Exception:%s" % (url, e)
                time.sleep(retry_delta)
            else:
                print datetime.datetime.now(), "[Spider]:%s Success!" % url
                break
