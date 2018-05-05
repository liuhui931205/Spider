# coding=utf-8
import requests
from lxml import etree
# from queue import Queue
# import threading
from multiprocessing import Process
from multiprocessing import JoinableQueue as Queue
import time

class QiuBai:
    def __init__(self):
        self.temp_url = "http://www.qiushibaike.com/8hr/page/{}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_list_queue = Queue()
        self.proxies = {"http":"http://58.247.179.94:8060"}

    def get_url_list(self):
        # return [self.temp_url.format(i) for i in range(1,14)]
        for i in range(1,14):
            self.url_queue.put(self.temp_url.format(i))

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url,headers=self.headers,proxies=self.proxies)
            print(response)

            if response.status_code != 200:
                self.url_queue.put(url)
            else:
                self.html_queue.put(response.content.decode())
            self.url_queue.task_done()  #让队列的计数-1

    def get_content_list(self):#提取数据
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            div_list = html.xpath("//div[@id='content-left']/div")
            content_list = []
            for div in div_list:
                item = {}
                item["user_name"] = div.xpath(".//h2/text()")[0].strip()
                item["content"] = [i.strip() for i in div.xpath(".//div[@class='content']/span/text()")]
                content_list.append(item)
            self.content_list_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self): #保存
        while True:
            content_list = self.content_list_queue.get()
            for content in content_list:
                # print(content)
                pass
            self.content_list_queue.task_done()

    def run(self):#实现做主要逻辑
        thread_list = []
        #1. 准备url列表
        t_url = Process(target=self.get_url_list)
        thread_list.append(t_url)
        #2. 遍历发送请求，获取响应
        for i in range(13):
            t_parse = Process(target=self.parse_url)
            thread_list.append(t_parse)
        #3. 提取数据
        t_content = Process(target=self.get_content_list)
        thread_list.append(t_content)
        #4. 保存
        t_save = Process(target=self.save_content_list)
        thread_list.append(t_save)

        for process in thread_list:
            process.daemon = True #把子线程设置为守护线程
            process.start()

        for q in [self.url_queue,self.html_queue,self.content_list_queue]:
            q.join() #让主线程阻塞，等待队列计数为0


if __name__ == '__main__':
    t1 = time.time()
    qiubai = QiuBai()
    qiubai.run()
    print("total cost:",time.time()-t1)