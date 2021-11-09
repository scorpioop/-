import scrapy
import json

class BookSpider(scrapy.Spider):
    name = 'book'
    # allowed_domains = ['jd.com']
    start_urls = ['https://pjapi.jd.com/book/sort?source=bookSort']
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'LOG_FILE': 'tool.txt',  # 配置的日志boo
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            "referer":"https://book.jd.com/"
        },
    }

    def parse(self, response):
        # big_node_list=response.xpath('//dt/a/text()').extract()
        # print(big_node_list)
        category = json.loads(response.text)['data']
        print(category)
        for item in category:
            big_category = item["categoryName"]
            big_category_link = "https://channel.jd.com/%d-%d.html"%(int(item["fatherCategoryId"]),int(item["categoryId"]))
            for item1 in item["sonList"]:
                temp={}
                small_category = item1["categoryName"]
                small_category_link = "https://list.jd.com/list.html?cat=%d,%d,%d"%(int(item["fatherCategoryId"]),int(item["categoryId"]),int(item1["categoryId"]))
                temp["big_category"] = big_category
                temp["big_category_link"] = big_category_link
                temp["small_category"] = small_category
                temp["small_category_link"] = small_category_link
                yield scrapy.Request(
                    url = small_category_link,
                    callback= self.parse_book_list,
                    meta = temp
                )
                break
            break
    def parse_book_list(self,response):
        print(response.meta)
        book_list = response.xpath('//*[@id="J_goodsList"]/ul/li/div')
        print(book_list)
        for book in book_list:
            link = "https:"+book.xpath('./div[3]/a/@href').extract_first()
            print(link)
            bookname = book.xpath('./div[3]/a/em/text()').extract_first()
            print(bookname)
            author = book.xpath('./div[4]/span[1]/a/text()').extract()
            author=(',').join(author)
            print(author)