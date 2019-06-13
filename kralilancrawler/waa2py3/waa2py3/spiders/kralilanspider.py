import scrapy
import json
from scrapy.spiders import CrawlSpider
import re
from ..items import HomeCrawlerItem


class KralilanSpider(CrawlSpider):

    name = 'kralilanspider'

    def __init__(self):
        super().__init__()
        self.allowed_domains = ['kralilan.com']

        self.start_urls = [
            'https://www.kralilan.com/liste/satilik-konut',
            'https://www.kralilan.com/liste/kiralik-konut',
            'https://www.kralilan.com/liste/gunluk-kiralik-konut',
            'https://www.kralilan.com/liste/devren-satilik-konut',
            'https://www.kralilan.com/liste/satilik-isyeri',
            'https://www.kralilan.com/liste/kiralik-isyeri',
            'https://www.kralilan.com/liste/devren-isyeri',
            'https://www.kralilan.com/liste/satilik-arsa',
            'https://www.kralilan.com/liste/kiralik-arsa',
            'https://www.kralilan.com/liste/satilik-bina',
            'https://www.kralilan.com/liste/kiralik-bina',
            'https://www.kralilan.com/liste/satilik-turistik-tesis',
            'https://www.kralilan.com/liste/kiralik-turistik-tesis',
        ]

    # start_urls in which the listings are located requires AJAX requests to load listings
    # Those requests require Content-Type header and request payload for every specific type
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url='https://www.kralilan.com/services/ki_operation.asmx/getFilter',
                method='POST',
                headers={'Content-Type': 'application/json; charset=utf-8', 'referer_url': url},
                body=json.dumps(PAYLOAD[url]),
                callback=self.parse,
                meta={'start_url': url}
            )

    def parse(self, response):
        # Extracting links from response
        text = json.loads(response.text)['d']
        links = re.findall('/ilan/.*/detay', text)
        links = ['https://www.kralilan.com' + link for link in links]

        # Extracting prices from response
        prices = re.findall("<h5 class='item-price'> &#x20BA;\s*.*</h5>", text)
        prices = [price.split(' ')[-1].replace('</h5>', '') for price in prices]

        # Prices are only listed on the main page, so they need to be sent between requests
        for link, price in zip(links, prices):
            yield scrapy.Request(url=link, callback=self.parse_items, meta={'price': price})

        # Since the listings are in an infinite scroll page, they are iterated here
        # start_url is carried with meta in order to find request body and the index is incremented by 1
        # Incrementing the index by 1 on the same request body returns the next 10 listings
        body = PAYLOAD[response.meta['start_url']]
        body['index'] = str(int(body['index']) + 1)

        # This loop will keep running until the returned request has no listings left
        if text != '':
            yield scrapy.Request(
                url='https://www.kralilan.com/services/ki_operation.asmx/getFilter',
                method='POST',
                headers={'Content-Type': 'application/json; charset=utf-8', 'referer_url': response.meta['start_url']},
                body=json.dumps(body),
                callback=self.parse,
                meta={'start_url': response.meta['start_url']}
            )


    def parse_items(self, response):

        item = HomeCrawlerItem()

        if response.css('.main-container').get():
            item['id'] = response.css('aside div.key-features div.media div.media-body span.media-heading::text').get()
            item['url'] = response.url
            item['title'] = response.css('h1[style*="font-size: 24px"]::text').get().strip()
            item['property_type'] = response.css('aside div.key-features div.media div.media-body span.media-heading::text').getall()[2].split()[1]
            item['floor_area'] = response.css('div.key-features ul:nth-child(3) div.media div.media-body span.media-heading::text').get(default='')
            location_string = response.css('span.item-location::text').get().strip().split(' ')
            location_string = [s for s in location_string if s.isalnum()]
            item['city'] = location_string[0]
            item['district'] = location_string[1]
            item['town'] = location_string[0]
            item['neighborhood'] = location_string[-1]
            item['latitude'] = ''
            item['longitude'] = ''
            item['postcode'] = ''
            item['address'] = ''
            item['pictures'] = ''
            item['is_new'] = ''
            item['content'] = response.css('div#ContentPlaceHolder1_lblAciklama *::text').getall()
            item['currency'] = 'try'
            item['price'] = response.meta['price']
            item_type = response.css('aside div.key-features div.media div.media-body span.media-heading::text').getall()[2].split()[0]
            item['type'] = 'sale' if item_type == 'Satılık' else 'rent'
            item['rooms'] = ''
            item['bathrooms'] = ''
            item['floor_number'] = ''
            item['plot_area'] = ''
            item['expiration_date'] = ''
            item['date'] = response.css('span.date i.icon-clock::text').get(default='').strip()
            item['is_parking'] = ''
            item['is_furnished'] = ''
            item['agent'] = response.css('div.seller-info h3.no-margin::text').get(default='')
            item['site_keywords'] = ''
            item['site_title'] = ''
            item['site_description'] = ''
            item['country'] = 'tr'
            item['vertical'] = 'home'
            item['file_name'] = 'kralilancom'
            item['site'] = 'kralilan.com'

        yield item


# Request payloads for every listing type
PAYLOAD = {
    'https://www.kralilan.com/liste/satilik-konut': {'incomestr': '["Konut","1",-1,-1,-1,-1,-1,5]',
                                                     'intextstr': '{"isCoordinates":false,'
                                                                  '"ListDrop":[],'
                                                                  '"ListText":[],'
                                                                  '"FiyatData":{"Max":"","Min":""}}',
                                                     'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/kiralik-konut': {'incomestr': '["Konut","2",-1,-1,-1,-1,-1,5]',
                                                     'intextstr': '{"isCoordinates":false,'
                                                                  '"ListDrop":[],'
                                                                  '"ListText":[],'
                                                                  '"FiyatData":{"Max":"","Min":""}}',
                                                     'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/gunluk-kiralik-konut': {'incomestr': '["Konut","3",-1,-1,-1,-1,-1,5]',
                                                            'intextstr': '{"isCoordinates":false,'
                                                                         '"ListDrop":[],'
                                                                         '"ListText":[],'
                                                                         '"FiyatData":{"Max":"","Min":""}}',
                                                            'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/devren-satilik-konut': {'incomestr': '["Konut","5",-1,-1,-1,-1,-1,5]',
                                                            'intextstr': '{"isCoordinates":false,'
                                                                         '"ListDrop":[],'
                                                                         '"ListText":[],'
                                                                         '"FiyatData":{"Max":"","Min":""}}',
                                                            'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/satilik-isyeri': {'incomestr':'["İşyeri","1",-1,-1,-1,-1,-1,5]',
                                                      'intextstr':'{"isCoordinates":false,'
                                                                  '"ListDrop":[],'
                                                                  '"ListText":[],'
                                                                  '"FiyatData":{"Max":"","Min":""}}',
                                                      'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/kiralik-isyeri': {'incomestr':'["İşyeri","2",-1,-1,-1,-1,-1,5]',
                                                      'intextstr':'{"isCoordinates":false,'
                                                                  '"ListDrop":[],'
                                                                  '"ListText":[],'
                                                                  '"FiyatData":{"Max":"","Min":""}}',
                                                      'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/devren-isyeri': {'incomestr':'["İşyeri","4",-1,-1,-1,-1,-1,5]',
                                                     'intextstr':'{"isCoordinates":false,'
                                                                 '"ListDrop":[],'
                                                                 '"ListText":[],'
                                                                 '"FiyatData":{"Max":"","Min":""}}',
                                                     'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/satilik-arsa': {'incomestr':'["Arsa","1",-1,-1,-1,-1,-1,5]',
                                                    'intextstr':'{"isCoordinates":false,'
                                                                '"ListDrop":[],'
                                                                '"ListText":[{"id":"78","Min":"","Max":""},'
                                                                            '{"id":"12","Min":"","Max":""},'
                                                                            '{"id":"107","Min":"","Max":""}],'
                                                                '"FiyatData":{"Max":"","Min":""}}',
                                                    'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},
    'https://www.kralilan.com/liste/kiralik-arsa': {'incomestr':'["Arsa","2",-1,-1,-1,-1,-1,5]',
                                                    'intextstr':'{"isCoordinates":false,'
                                                                '"ListDrop":[],'
                                                                '"ListText":[{"id":"78","Min":"","Max":""},'
                                                                            '{"id":"12","Min":"","Max":""},'
                                                                            '{"id":"107","Min":"","Max":""}],'
                                                                '"FiyatData":{"Max":"","Min":""}}',
                                                    'index':'0' , 'count':'10' , 'opt':'1' , 'type':'3'},

    'https://www.kralilan.com/liste/satilik-bina': {'incomestr': '["Bina","1",-1,-1,-1,-1,-1,5]',
                                                    'intextstr': '{"isCoordinates":false,"ListDrop":[],'
                                                                 '"ListText":[{"id":"78","Min":"","Max":""},'
                                                                 '{"id":"107","Min":"","Max":""}],'
                                                                 '"FiyatData":{"Max":"","Min":""}}',
                                                    'index': '0', 'count': '10', 'opt': '1', 'type': '3'},
    'https://www.kralilan.com/liste/kiralik-bina': {'incomestr': '["Bina","2",-1,-1,-1,-1,-1,5]',
                                                    'intextstr': '{"isCoordinates":false,"ListDrop":[],'
                                                                 '"ListText":[{"id":"78","Min":"","Max":""},'
                                                                 '{"id":"107","Min":"","Max":""}],'
                                                                 '"FiyatData":{"Max":"","Min":""}}',
                                                    'index': '0', 'count': '10', 'opt': '1', 'type': '3'},
    'https://www.kralilan.com/liste/satilik-turistik-tesis': {'incomestr': '["Turistik Tesis","1",-1,-1,-1,-1,-1,5]',
                                                              'intextstr': '{"isCoordinates":false,"ListDrop":[],'
                                                                           '"ListText":[{"id":"78","Min":"","Max":""},'
                                                                           '{"id":"107","Min":"","Max":""}],'
                                                                           '"FiyatData":{"Max":"","Min":""}}',
                                                              'index': '0', 'count': '10', 'opt': '1', 'type': '3'},
    'https://www.kralilan.com/liste/kiralik-turistik-tesis': {'incomestr': '["Turistik Tesis","2",-1,-1,-1,-1,-1,5]',
                                                              'intextstr': '{"isCoordinates":false,"ListDrop":[],'
                                                                           '"ListText":[{"id":"78","Min":"","Max":""},'
                                                                           '{"id":"107","Min":"","Max":""}],'
                                                                           '"FiyatData":{"Max":"","Min":""}}',
                                                              'index': '0', 'count': '10', 'opt': '1', 'type': '3'},

}
