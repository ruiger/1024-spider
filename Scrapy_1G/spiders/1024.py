import os

import scrapy
from scrapy import Selector
from scrapy import Spider
from scrapy.loader import Identity, ItemLoader
from scrapy.utils.project import get_project_settings

from Scrapy_1G.items import ImageItem


class XiaoHaiSpider(Spider):
    name = "xiaohai"
    allowed_domains = ["http://xiaohai.ga/"]
    start_urls = [

    ]
    set = get_project_settings()

    def start_requests(self):
        pages = []
        print(self.set['BASE_URL'])
        for i in range(1, 2):
            url = self.set['BASE_URL'] + 'thread0806.php?fid=16&search=&page=' + str(i)
            page = scrapy.Request(url)
            pages.append(page)
        return pages

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        sel = Selector(response)
        url_list_one = sel.xpath("//a[contains(@href,'htm_data')]")
        open_url = []
        for u in url_list_one:
            href = u.xpath("@href").extract_first()
            open_url.append(self.set['BASE_URL'] + href)
        for pageUrl in open_url:
            try:
                print('正在下载地址' + pageUrl)
                filePath = pageUrl[-12:-5]
                # if not os.path.isdir(filePath):
                #     os.mkdir(filePath)
                request = scrapy.Request(url=pageUrl, callback=self.parse_item, dont_filter=True)
                request.meta['item'] = filePath
                yield request
                # image_item = ImageItem()
                # image_item['image_urls'] = filePath
                # yield image_item
            except:
                print("地址：" + pageUrl + '下载失败')

    def parse_item(self, response):
        # sel2 = Selector(response)
        # link = sel2.xpath("//img/@src").extract()
        # image_item = ImageItem()
        # image_item['image_urls'] = link
        # yield image_item
        l = ItemLoader(item=ImageItem(), response=response)
        l.add_xpath('image_urls', "//input[@type='image']/@src", Identity())
        filePath = response.meta['item']
        l.add_value('url', response.url)
        l.add_value('filePath', filePath)
        return l.load_item()
