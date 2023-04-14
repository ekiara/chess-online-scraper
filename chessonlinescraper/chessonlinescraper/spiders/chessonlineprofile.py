import scrapy


class ChessonlineprofileSpider(scrapy.Spider):
    """
    This spider is only intended to scrape one profile at a time, and
    the sample URL list in `start_urls` should be ignored,
    this spider should be invoked with the following:
    `scrapy crawl chessonlineprofile -a start_urls=url_01,url_02,url_03`

    """

    name = "chessonlineprofile"
    allowed_domains = ["chess.com"]
    start_urls = [
        "https://www.chess.com/players/ding-liren",
        "https://www.chess.com/players/alireza-firouzja",
        "https://www.chess.com/players/hikaru-nakamura",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        designation: str = response.xpath(
            '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[1]/h1/span[contains(@class, "master-players-chess-title")]/text()'
        ).get()
        full_name: str = (
            response.xpath(
                '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[1]/h1/span[contains(@class, "master-players-full-name")]/text()'
            )
            .get()
            .strip()
        )
        name: str = (
            response.xpath(
                '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[3]/div[1]/div[contains(@class, "master-players-value")]/text()'
            )
            .get()
            .strip()
        )
        dob_string: str = (
            response.xpath(
                '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[3]/div[2]/div[contains(@class, "master-players-value")]/text()'
            )
            .get()
            .strip()
        )
        place_of_birth: str = (
            response.xpath(
                '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[3]/div[3]/div[contains(@class, "master-players-value")]/text()'
            )
            .get()
            .strip()
        )
        federation: str = (
            response.xpath(
                '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[3]/div[4]/div[contains(@class, "master-players-value")]/text()'
            )
            .get()
            .strip()
        )
        profile_links = []
        for profile_link in response.xpath(
            '//*[@id="view-master-players"]/div[3]/div/article/div[1]/div[3]/div[5]/div[2]/a'
        ):
            profile_links.append(profile_link.attrib["href"])

        yield {
            "designation": designation,
            "full_name": full_name,
            "name": name,
            "dob_string": dob_string,
            "place_of_birth": place_of_birth,
            "federation": federation,
            "profile_links": profile_links,
        }
