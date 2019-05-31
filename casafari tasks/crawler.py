import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from reppy.robots import Robots


def is_absolute(url):
    return bool(urlparse(url).netloc)  # Returns True if the url has host name


def fix_relative_url(url, host):
    absolute_url = urljoin(host, url)  # Joining the host with the url
    return absolute_url


def get_robots_url(url):

    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url

    # Going to root and fetching /robots.txt
    root = urlparse(url).hostname

    return 'https://' + root + '/robots.txt'


def get_links(url):

    base = url
    links = []

    res = requests.get(base)
    soup = BeautifulSoup(res.text, 'html.parser')  # Parsing the html file

    # Getting all the links in page with href attribute and extracting their href attributes
    a_tags = soup.find_all('a', href=True)

    # Starting the robots parser
    rp = Robots.fetch(get_robots_url(base))
    agent = rp.agent('*')

    # Looping all the links found in the page
    for a_tag in a_tags:
        link = a_tag.get('href')  # Getting the href attribute

        if is_absolute(link) is False:
            link = fix_relative_url(link, base)  # Fixing relative urls

        # If robot_parser allows link to be scraped, appending it to a list
        if agent.allowed(link):
            links.append(link)
        else:
            print('Link is not allowed for scraping ({})'.format(link))

    return set(links)  # Casting to set for eliminating duplicates
