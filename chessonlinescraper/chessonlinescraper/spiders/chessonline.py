import scrapy


class ChessonlineSpider(scrapy.Spider):
    name = "chessonline"
    allowed_domains = ["chess.com"]
    start_urls = ["http://chess.com/"]

    def parse(self, response):
        pass
