"""
Extract python news from python.org
"""
import re
from pomp.core.base import BaseCrawler, BasePipeline
from pomp.core.item import Item, Field
from pomp.contrib import SimpleDownloader


news_re = re.compile(r'<h2 class="news">(.*?)</h2>([\s\S]*?)<div class="pubdate">(.*?)</div>')


class PythonNewsItem(Item):
    title = Field()
    published = Field()

    def __repr__(self):
        return '%s\n\t%s\n' % (
            self.title,
            self.published,
        )


class PythonNewsCrawler(BaseCrawler):
    ENTRY_URL = 'http://python.org/news/'

    def extract_items(self, url, page):

        for i in news_re.findall(page):
            item = PythonNewsItem()
            item.title, item.published = i[0], i[2]
            yield item

    def next_url(self, page):
        return None # one page crawler


class PrintPipeline(BasePipeline):

    def process(self, item):
        print(item)


if __name__ == '__main__':
    from pomp.core.engine import Pomp

    pomp = Pomp(
        downloader=SimpleDownloader(),
        pipelines=[PrintPipeline()],
    )

    pomp.pump(PythonNewsCrawler())