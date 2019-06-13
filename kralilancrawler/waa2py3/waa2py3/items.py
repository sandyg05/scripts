import scrapy


class HomeCrawlerItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    property_type = scrapy.Field()
    floor_area = scrapy.Field()
    type = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    town = scrapy.Field()
    neighborhood = scrapy.Field()
    postcode = scrapy.Field()
    address = scrapy.Field()
    by_owner = scrapy.Field()
    expiration_date = scrapy.Field()
    date = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    rooms = scrapy.Field()
    bathrooms = scrapy.Field()
    floor_number = scrapy.Field()
    plot_area = scrapy.Field()
    is_parking = scrapy.Field()
    is_furnished = scrapy.Field()
    is_new = scrapy.Field()
    site_title = scrapy.Field()
    site_description = scrapy.Field()
    site_keywords = scrapy.Field()
    site = scrapy.Field()
    agent = scrapy.Field()
    pictures = scrapy.Field()
    country = scrapy.Field()
    vertical = scrapy.Field()
    file_name = scrapy.Field()