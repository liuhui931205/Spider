# coding=utf-8
import requests
from lxml import etree

class TieBaSpider:
    def __init__(self,tieba_name):
        #1. start_url
        self.start_url= "http://tieba.baidu.com/mo/q---C9E0BC1BC80AA0A7CE472600CDE9E9E3%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1525330549279_782/m?kw={}&lp=6024".format(tieba_name)
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36"}
        self.part_url = "http://tieba.baidu.com/mo/q---C9E0BC1BC80AA0A7CE472600CDE9E9E3%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1525330549279_782"
    def parse_url(self,url): #发送请求，获取响应
        response = requests.get(url,headers=self.headers)
        return response.content

    def get_content_list(self,html_str): #3. 提取数据
        html = etree.HTML(html_str)
        div_list = html.xpath("//body/div/div[contains(@class,'i')]")
        content_list = []
        for div in div_list:
            item = {}
            item["href"] = self.part_url+div.xpath("./a/@href")[0]
            item["title"] = div.xpath("./a/text()")[0]
            content_list.append(item)

        #提取下一页的url地址
        next_url = html.xpath("//a[text()='下一页']/@href")
        next_url =self.part_url+ next_url[0] if len(next_url)>0 else None
        return content_list,next_url

    def save_content_list(self,content_list):#保存数据
        for content in content_list:
            print(content)

    def run(self): #实现主要逻辑
        next_url = self.start_url
        while next_url is not None:
            #1. start_url
            #2. 发送请求，获取响应
            html_str = self.parse_url(next_url)
            #3. 提取数据
            content_list,next_url = self.get_content_list(html_str)
            #4。保存
            self.save_content_list(content_list)
            #5.获取next_url，循环2-5

if __name__ == '__main__':
    tieba = TieBaSpider("传智播客")
    tieba.run()

