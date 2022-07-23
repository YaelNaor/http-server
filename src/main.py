import socketserver
import os
import html_generator
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
                with open(path, "rb") as file:
                    file_data = file.read()
                response = http_response.create_file_http_response(file_data)

        except Exception as e:
            print(e)
            response = http_response.create_bad_request_http_response(path)
        print('response length', len(response))
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
