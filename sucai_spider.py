# -*- coding: utf-8 -*-

"""方法1：Spider"""
import scrapy
import pymongo

class SuCaiSpider(scrapy.Spider):
    name = 'doooorsucai'
    allowed_domains = ['www.doooor.com']
    start_urls = ['https://www.doooor.com/sucai1.html']

    # 通过scrapy.Request传递headers
    # headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    #     }
    # page_url = 'https://www.doooor.com/sucai{}.html'
    # def start_requests(self):
    #     for i in range(1,11):
    #         yield scrapy.Request(url=self.page_url.format(str(i)), callback=self.parse)

    # 通过custom_settings传递headers等配置参数
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        },
        'FEED_EXPORT_ENCODING': 'UTF-8',
        # 'LOG_LEVEL': 'DEBUG',
        # 'LOG_FILE': './log.log'
    }
    # 配置数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client['doooor']
    sucai = db['sucai']


    def parse(self, response):
        # 验证配置参数是否配置成功
        # print(response.request.headers.getlist('User-Agent'))

        # 用css正则解决'#shoucang li'匹配问题
        for li in response.css('li[id^="qqy_list"]'):
            data = {
                'category': li.css('.itemfoot > a::text').extract_first().strip(),
                'title': li.css('a.simgtitle::text').extract_first(),
                'url': li.css('a.simgtitle::attr(href)').extract_first(),
                'cover': li.css('a.simage > img::attr(src)').extract_first()
            }
            self.sucai.update_one({'url':data['url']}, {'$set':data}, True)
            yield data

        next = response.css('.pg a.nxt::attr(href)').extract_first()
        # next_url = 'https://www.doooor.com/' + next
        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse)


""""方法2：CrawlSpider"""
# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# import pymongo

# class SuCaiSpider(CrawlSpider):
#     name = 'doooorsucai'
#     allowed_domains = ['www.doooor.com']
#     start_urls = ['https://www.doooor.com/sucai1.html']
#     rules = (
#         Rule(LinkExtractor(allow=(r'.*sucai\d+\.html',)), callback='parse_item', follow=True),
#     )
#     custom_settings = {
#         'DOWNLOAD_DELAY': 1,
#         'DEFAULT_REQUEST_HEADERS': {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
#         },
#         'FEED_EXPORT_ENCODING': 'UTF-8'
#     }
#     client = pymongo.MongoClient('localhost', 27017)
#     db = client['doooor']
#     sucai_c = db['sucai_c']



#     def parse_item(self, response):
#         # self.logger.info('Hi, this is an item page! %s', response.url)

#         for li in response.xpath('//li[starts-with(@id,"qqy_list")]'):
#             data = {
#                 'category': li.xpath('.//div[@class="itemfoot"]/a/text()').get().strip(),
#                 'title': li.xpath('.//a[@class="simgtitle"]/text()').get(),
#                 'url': li.xpath('.//a[@class="simgtitle"]/@href').get(),
#                 'cover': li.xpath('.//a[@class="simage"]/img/@src').get()
#             }
#             self.sucai_c.update_one({'url':data['url']}, {'$set':data}, True)
#             yield data

