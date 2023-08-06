from requests_html import HTMLSession
from src.utils import Common

baseUrl = 'http://bangumi.tv/anime/browser?sort=rank&page=%d'

class Bangumi:

    @staticmethod
    def page(page, limit=None):
        session = HTMLSession()
        result = session.get(baseUrl % page)
        browserItemListresult = result.html.find('li[class="item odd clearit"]')

        browserItemListresult = Common.limit(browserItemListresult, limit)

        for browserItem in browserItemListresult:
            img = browserItem.find('img', first=True).attrs['src']
            title = browserItem.find('a.l', first=True).text
            info = browserItem.find('p.info.tip', first=True).text
            rank = browserItem.find('small.fade', first=True).text
            url = 'http://bangumi.tv/%s' % browserItem.find('a.l', first=True).attrs['href']
            print('Rank:%s\n标题:%s\n介绍:%s\n图片:http:%s\n页面:%s\n' % (rank, title, info, img, url))
