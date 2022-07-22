import socketserver
import os
import html_generator
import gzip
from email.utils import formatdate
import argparse
from urllib.parse import unquote
import http_response


class HttpHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        print("{} wrote:".format(self.client_address[0]))

        path = self.check_http()
        path = unquote(path)

        try:
            # Request for favicon.ico
            if path == "/favicon.ico":
                response = http_response.create_favicon_http_response()
            # Request for directory
            elif os.path.isdir(path):
                files = os.listdir(path)
                html = html_generator.get_html_page(path, files)
                response = http_response.create_text_http_response(html)
            # Request to download file
            else:
                print('Download path', path)
                file_data = open(path, "rb").read()
                response = http_response.create_file_http_response(file_data)

        except Exception as e:
            print(e)
            response = http_response.create_bad_request_http_response(path)

        self.request.sendall(response)

    def _readline(self):
        byte = None
        line = b''
        while byte != b'\r':
            byte = self.request.recv(1)
            line += byte
        if self.request.recv(1) != b'\n':
            return None

        return line.decode()

    def check_http(self):
        line = self._readline()
        request_arr = line.split()
        if request_arr[0] != 'GET':
            return None
        return request_arr[1]

    @staticmethod
    def create_base_http_response():
        # https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python
        date = formatdate(timeval=None, localtime=False, usegmt=True)

        HTTP_LINES = [
            'HTTP/1.0 200 OK',
            'Date: {}'.format(date),
        ]

        return HTTP_LINES

    @staticmethod
    def create_text_http_response(http_lines, html):
        http_lines.append("Content-Type: text/html; charset=UTF-8")
        response = bytes('\r\n'.join(http_lines) + '\r\n' * 2 + html, encoding='utf8')

        return response

    @staticmethod
    def create_favicon_http_response(http_lines):
        icon = open("favicon.ico", 'br')
        favicon = icon.read()
        http_lines.append("Content-Type: text/html; charset=UTF-8")

        response = bytes('\r\n'.join(http_lines), encoding='utf8') + b'\r\n' * 2 + favicon
        return response

    @staticmethod
    def create_file_http_response(http_lines, file_data):
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        gzip_file = gzip.compress(file_data)
        content_type = ['Content-Type: application/octet-stream', 'Content-Encoding: gzip',
                        'Content-Length: {}'.format(len(gzip_file))]
        http_lines = http_lines + content_type

        response = bytes('\r\n'.join(http_lines), encoding='utf8') + b'\r\n' * 2 + gzip_file
        return response

    @staticmethod
    def create_bad_request_http_response(path):
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        http_lines = [
            'HTTP/1.0 404 Not Found',
            'Date: {}'.format(date),
            'Content-Type: text/html; charset=UTF-8',
        ]

        with open("html_error_page.html", "r", encoding="UTF-8") as f:
            html = f.read()

        html = html.format(path)

        response = bytes('\r\n'.join(http_lines) + '\r\n' * 2 + html, encoding='utf8')
        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-ho', type=str, default="0.0.0.0")
    parser.add_argument('--port', '-p', type=int, default=80)
    args = parser.parse_args()

    # Create the server
    with socketserver.TCPServer((args.host, args.port), HttpHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


if __name__ == '__main__':
    main()
