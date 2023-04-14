import scrapy


class ChessonlineyouthSpider(scrapy.Spider):
    name = "chessonlineyouth"
    allowed_domains = ["chess.com"]
    start_urls = ["https://www.chess.com/ratings/u20"]

    def parse(self, response):
        rows = response.css("table.table-component tbody tr")
        for row in rows:
            player_url: str = row.css("td")[1].css("div a").attrib["href"]
            yield {
                "player_url": player_url,
            }

        next_page = response.xpath(
            '//*[@id="view-master-players"]/div/div[2]/div/nav/a[6]'
        ).attrib["href"]
        if next_page != response.url:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
            )
        else:
            print(f"Reached the last page: {next_page}")
