import gzip
from email.utils import formatdate


def create_http_response(
        status='200 OK',
        date=None,
        content_type='text/html; charset=UTF-8',
        content_encoding=None,
        content_length=None,
        content=None

):
    # https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
    if date is None:
        date = formatdate(timeval=None, localtime=False, usegmt=True)

    http_parameters = {
        'Date': '{}'.format(date),
        'Content-Type': content_type,
    }

    if content_encoding is not None:
        http_parameters['Content-Encoding'] = content_encoding

    if content_length is not None:
        http_parameters['Content-Length'] = content_length

    response = 'HTTP/1.0 {}\r\n'.format(status)
    response += '\r\n'.join(f'{key}: {value}' for key, value in http_parameters.items())
    response = bytes(response + '\r\n' * 2, encoding='utf8') + content
    return response


def create_text_http_response(html):
    return create_http_response(content=html.encode('UTF-8'))


def create_favicon_http_response():
    with open("favicon.ico", 'br') as file:
        icon = file.read()
    return create_http_response(content=icon)


def create_file_http_response(file_data):
    gzip_file = gzip.compress(file_data)
    return create_http_response(content_type='application/octet-stream', content_encoding='gzip',
                                content_length=f'{len(gzip_file)}', content=gzip_file)


def create_bad_request_http_response(path):
    with open("html_error_page.html", "r", encoding="UTF-8") as f:
        html = f.read().format(path=path)

    return create_http_response(status='404 Not Found', content=html.encode('UTF-8'))
