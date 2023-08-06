from requests_html import HTMLSession
from src.utils import Common

baseUrl = 'http://top.baidu.com/buzz?b=23&c=5&fr=topcategory_c5'


class BaiDu:

    @staticmethod
    def parse_top(element):
        rank = element[0].find('span.num-top', first=True).text
        title = element[0].find('a.list-title', first=True).text
        url = element[0].find('a.list-title', first=True).attrs['href']

        img = element[1].find('img', first=True).attrs['src']
        info = element[1].find('p.item-text', first=True).text
        return {'rank': rank, 'title': title, 'url': url, 'img': img, 'info': info}

    @staticmethod
    def page(page, limit=None):
        session = HTMLSession()
        result = session.get(baseUrl)
        browserItemListresult = result.html.find('tr')
        arr = [BaiDu.parse_top(browserItemListresult[1:3]), BaiDu.parse_top(browserItemListresult[3:5]),
               BaiDu.parse_top(browserItemListresult[5:7])]
        browserItemListresult = browserItemListresult[7:len(browserItemListresult)]
        for browserItem in browserItemListresult:
            rank = browserItem.find('span.num-normal', first=True).text
            title = browserItem.find('a.list-title', first=True).text
            url = browserItem.find('a.list-title', first=True).attrs['href']
            img = ''
            info = ''
            arr.append({'rank': rank, 'title': title, 'url': url, 'img': img, 'info': info})

        arr = Common.limit(arr, limit)

        for arr_item in arr:
            print('Rank:%s\n标题:%s\n介绍:%s\n图片:%s\n页面:%s\n' % (
                arr_item['rank'], arr_item['title'], arr_item['info'], arr_item['img'], arr_item['url']))
