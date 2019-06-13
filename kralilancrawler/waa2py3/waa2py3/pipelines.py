class XmlWriterPipeline:
    def __init__(self):
        self.page = 1
        self.item_counter = 0
        self.per_page = 1000
        self.country = ''
        self.vertical = ''
        self.site = ''
        self.crawler_proccess_id = ''

    def process_item(self, item, spider):
        self.item_counter = self.item_counter + 1
        self.country = item['country']
        self.vertical = item['vertical']
        self.site = item['site']
        if self.item_counter == 1:
            path = 'feed/{}/{}/{}_{}.xml'.format(item['country'], item['vertical'], item['file_name'], self.page)
            self.file = open(path, 'w', encoding='utf-8')
            self.file.write('<?xml version="1.0" encoding="utf-8" ?>\n<waa2>\n')

        self.file.write(XmlWriterPipeline.xmlGenerateHome(self, item))

        if self.item_counter >= self.per_page:
            self.page = self.page + 1
            self.item_counter = 0
            self.file.write('</waa2>')

    def close_spider(self, spider):
        if self.item_counter > 0:
            self.file.write('</waa2>')

    def xmlGenerateHome(self, item):
        xml = []
        xml.append('<ad>')
        xml.append('\n<id><![CDATA[%s]]></id>' % (item['id']))
        xml.append('\n<url><![CDATA[%s]]></url>' % (item['url']))
        xml.append('\n<title><![CDATA[%s]]></title>' % (item['title']))
        xml.append('\n<content><![CDATA[%s]]></content>' % (item['content']))
        xml.append('\n<type><![CDATA[%s]]></type>' % (item['type']))
        xml.append('\n<property_type><![CDATA[%s]]></property_type>' % (item['property_type']))
        xml.append('\n<floor_area><![CDATA[%s]]></floor_area>' % (item['floor_area']))
        xml.append('\n<city><![CDATA[%s]]></city>' % (item['city']))
        xml.append('\n<district><![CDATA[%s]]></district>' % (item['district']))
        xml.append('\n<price unit="%s"><![CDATA[%s]]></price>' % (item['currency'], item['price']))
        xml.append('\n<date><![CDATA[%s]]></date>' % (item['date']))
        xml.append('\n<expiration_date><![CDATA[%s]]></expiration_date>' % (item['expiration_date']))
        xml.append('\n<latitude><![CDATA[%s]]></latitude>' % (item['latitude']))
        xml.append('\n<longitude><![CDATA[%s]]></longitude>' % (item['longitude']))
        xml.append('\n<postcode><![CDATA[%s]]></postcode>' % (item['postcode']))
        xml.append('\n<town><![CDATA[%s]]></town>' % (item['town']))
        xml.append('\n<neighborhood><![CDATA[%s]]></neighborhood>' % (item['neighborhood']))
        xml.append('\n<rooms><![CDATA[%s]]></rooms>' % (item['rooms']))
        xml.append('\n<bathrooms><![CDATA[%s]]></bathrooms>' % (item['bathrooms']))
        xml.append('\n<floor_number><![CDATA[%s]]></floor_number>' % (item['floor_number']))
        xml.append('\n<plot_area><![CDATA[%s]]></plot_area>' % (item['plot_area']))
        xml.append('\n<is_parking><![CDATA[%s]]></is_parking>' % (item['is_parking']))
        xml.append('\n<site_title><![CDATA[%s]]></site_title>' % (item['site_title']))
        xml.append('\n<site_keywords><![CDATA[%s]]></site_keywords>' % (item['site_keywords']))
        xml.append('\n<site_description><![CDATA[%s]]></site_description>' % (item['site_description']))
        xml.append('\n<is_furnished><![CDATA[%s]]></is_furnished>' % (item['is_furnished']))
        xml.append('\n<is_new><![CDATA[%s]]></is_new>' % (item['is_new']))
        xml.append('\n<agent><![CDATA[%s]]></agent>' % (item['agent']))
        if len(item['pictures']) > 0:
            xml.append('\n<pictures>')
            for picture in item['pictures']:
                xml.append('\n<picture><![CDATA[%s]]></picture>' % picture)
            xml.append('\n</pictures>')
        xml.append('\n</ad>\n')
        return ''.join((xml))
