"""
Scraper to collect player ranking data from chess.com
"""
import scrapy


class ChessonlineSpider(scrapy.Spider):
    name = "chessonline"
    allowed_domains = ["chess.com"]
    start_urls = ["https://www.chess.com/ratings"]

    def parse(self, response):
        rows = response.css("table.table-component tbody tr")
        for row in rows:
            # Handle ranking column that either contains just the ranking
            # or if it indicates whether the player has gone up or down in rank
            if row.css("td")[0].xpath(".//div/div") == []:
                ranking = row.css("td")[0].xpath(".//div").css("::text").get().strip()
                ranking_change = 0
            else:
                ranking_div = row.css("td")[0].xpath(".//div").get()
                ranking = ranking_div[ranking_div.index("#"):].split("\n")[0]
                # TODO: the type conversion below should be handled in a safer way
                ranking_change = int(
                    row.xpath(".//td[1]/div/div/text()")[1].get().strip()
                )
                if "trend-down" in row.xpath(".//td[1]/div/div").attrib["class"]:
                    ranking_change = ranking_change * -1

            # Parse player image URL
            image_url = ""
            if "data-src" in row.css("td")[1].css("div img").attrib:
                image_url = (
                    row.css("td")[1]
                    .css("div img")
                    .attrib["data-src"]
                    .replace("v1/", "")
                )

            # Handle country column for the Ukraine flag link
            if row.css("td")[1].xpath(".//div/a[2]") == []:
                country = row.css("td")[1].css("div div")[1].attrib["v-tooltip"].strip()
            else:
                country = (
                    row.css("td")[1]
                    .xpath(".//div/a[2]")
                    .attrib["v-tooltip"]
                    .split()[-1]
                )

            yield {
                "ranking": ranking,
                "ranking_change": ranking_change,
                "image_url": image_url,
                "ranking_name": row.css("td")[1].css("div div")[0].attrib["v-tooltip"],
                "ranking_acronym": row.css("td")[1].css("div div")[0].css("span::text").get(),
                "player_url": row.css("td")[1].css("div a").attrib["href"],
                "player_name": row.css("td")[1].css("div a::text").get().strip(),
                "country": country,
                "classical_rating": row.css("td")[3].css("div::text").get().strip(),
                "rapid_rating": row.css("td")[4].css("div::text").get().strip(),
                "blitz_rating": row.css("td")[5].css("div::text").get().strip(),
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
