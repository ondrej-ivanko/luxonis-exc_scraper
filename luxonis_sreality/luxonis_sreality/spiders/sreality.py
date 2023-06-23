from math import ceil

import scrapy
from luxonis_sreality.items import LuxonisSrealityItem
from scrapy.spiders import CrawlSpider
from scrapy_playwright.page import PageMethod


class SrealitySpider(CrawlSpider):
    name = "sreality"
    allowed_domains = ["sreality.cz"]
    detail_anchors_sel = (
        "div.property:nth-child(1) > div:nth-child(2) > div:nth-child(1) "
        "> span:nth-child(1) > h2:nth-child(1) > a:nth-child(1) "
        "> span:nth-child(1)"
    )
    ITEMS_GOAL = 500
    follow_count = None

    def start_requests(self):
        yield scrapy.Request(
            "https://www.sreality.cz/hledani/prodej/byty",
            self.parse_items,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", self.detail_anchors_sel),
                ],
                "errback": self.errback,
            },
        )

    async def parse_detail(self, response):
        page = response.meta["playwright_page"]
        title = await page.title()
        await page.close()

        def title_image_url(query):
            return response.xpath(query).get(default="")

        yield LuxonisSrealityItem(
            title=title,
            img_url=title_image_url("//img[has-class('ob-c-gallery__img')]/@src"),
        )

    async def parse_items(self, response):
        follow_get_details = response.xpath("//a[has-class('title')]/@href").getall()
        for link in follow_get_details:
            yield scrapy.Request(
                f"https://www.sreality.cz{link}",
                self.parse_detail,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "errback": self.errback,
                },
            )

        # how many times to follow to next page for more items
        if not self.follow_count:
            self.follow_count = ceil(self.ITEMS_GOAL / len(follow_get_details))

        next_page = response.xpath(
            "//a[has-class('btn-paging-pn icof icon-arr-right paging-next')]/@href"
        ).get()
        if next_page is not None:
            page_num = next_page.rsplit("=", 1)[1]
            if int(page_num) <= self.follow_count:
                yield scrapy.Request(
                    f"https://www.sreality.cz{next_page}",
                    self.parse_items,
                    meta={
                        "playwright": True,
                        "errback": self.errback,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", self.detail_anchors_sel),
                        ],
                    },
                )

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
