import ssl
import _ssl
import urllib.request
import urllib.parse

# Context for ignoring SSL certificate errors
request_context = ssl.create_default_context()
request_context.check_hostname = False
request_context.verify_mode = _ssl.CERT_NONE


def extract_root(url):
    """
    Extracts the root URL from the given URL.
    :param url: A URL. (string)
    :return: Root URL of the given URL. (string)
    """
    if url.endswith("/"):
        url = url[:-1]

    if url.endswith('.htm') or url.endswith('.html'):
        pointer = url.rfind('/')
        url = url[:pointer]

    return url


def is_relative(url):
    """
    Checks the given URL is a relative URL or not.
    :param url: A URL. (string)
    :return: True or False depending on the URL scheme.
    """
    parse_result = urllib.parse.urlparse(url)
    return len(parse_result.scheme) < 1


def make_absolute(url, path):
    """
    Forms the absolute URL from the root and the path.
    :param url: The root URL. (string)
    :param path: The relative URL. (string)
    :return: The Absolute URL of the given relative URL. (string)
    """
    absolute_url = urllib.parse.urljoin(url, path)
    return absolute_url


def does_exist(url):
    """
    Check the given URL exists or not.
    :param url: A URL. (string)
    :return: True or False depending on the existence of the URL.
    """
    if url is None:
        return False
    elif len(url) < 1:
        return False
    else:
        return True


def is_image(url):
    """
    Checks the given URL is an image or not.
    :param url: A URL. (string)
    :return: True or False depending on the file format.
    """
    return (url.endswith("jpg") or
            url.endswith("jpeg") or
            url.endswith("gif") or
            url.endswith("png"))


def open_url(url):
    """
    Gets the response by making a request to the given url.
    :param url: A URL. (string)
    :return: HTTP Response object of the given URL. (HTTPResponse)
    """
    url_response = urllib.request.urlopen(url, context=request_context)
    return url_response


def get_http_status_code(url_response):
    """
    Gets the HTTP Status Code from the response object.
    :param url_response: An HTTP Response object. (HTTPResponse)
    :return: HTTP Status Code of the given response object. (string)
    """
    status_code = url_response.getcode()
    return status_code


def get_http_content_type(url_response):
    """
    Gets the HTTP Content-Type from the response object.
    :param url_response: An HTTP Response object. (HTTPResponse)
    :return: HTTP Content-Type of the given response object. (string)
    """
    content_type = url_response.info().get_content_type()
    return content_type
