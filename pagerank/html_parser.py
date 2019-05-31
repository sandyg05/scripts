from bs4 import BeautifulSoup


def parse_html(url_response):
    """
    Gets the parsed and repaired BeautifulSoup object.
    :param url_response: An HTTP Response object. (HTTPResponse)
    :return: Parsed BeautifulSoup object of the given response object. (bs4.BeautifulSoup)
    """
    html_code = url_response.read()
    soup = BeautifulSoup(html_code, "html.parser")
    return soup


def get_tags(soup, tag):
    """
    Gets a sequence of tags in the given BeautifulSoup object.
    :param soup: Parsed BeautifulSoup object. (bs4.BeautifulSoup)
    :param tag: Tag to search in the HTML file. (string)
    :return: An iterable object contains the found tags. (bs4.element.ResultSet)
    """
    return soup(tag)


def get_attribute(tag, attribute):
    """
    Gets the attribute of the given tag object.
    :param tag: A single tag object from the soup. (bs4.element.Tag)
    :param attribute: Attribute to search in the given tag. (string)
    :return: Found attribute in the given tag in a string form (string)
    """
    tag_attribute = tag.get(attribute, None)
    return tag_attribute
