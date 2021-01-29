#  coding: utf-8
import socketserver
import os


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

def parsePayload(data):
    payload = data.decode("utf-8").split("\n")[0]
    host = data.decode("utf-8").split("\n")[1]
    print(host)
    splitPayload = payload.split(" ")
    method = splitPayload[0]
    page = splitPayload[1]
    return method, page


def readFile(file):
    f = open(file, 'r')
    readPage = f.read()
    f.close()
    return readPage


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(1024).strip()
        print(self.data)
        print("Got a request of: %s\n" % self.data)

        method, page = parsePayload(self.data)
        html = None
        css = None

        directory = "./www" + page

        if os.path.isdir(directory):
            print("dir: " + str(directory))
            for file in os.listdir(directory):
                if file.endswith(".html") and page[-1] == "/":
                    html = readFile("www%s%s" % (page, file))
                if file.endswith(".css"):
                    css = readFile("www%s/%s" % (page, file))
        elif os.path.isfile(directory):
            print("file: " + str(directory))
            if page.endswith(".html"):
                html = readFile("www/%s" % page)
            if page.endswith(".css"):
                css = readFile("www/%s" % page)
            print(html, css)

        if method != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
        elif os.path.isdir("./www" + page) and page[-1] != "/":
            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n", 'utf-8'))
            forwardedPage = page + "/"
            self.request.sendall(bytearray("Location: %s\r\n" % forwardedPage, 'utf-8'))
        elif html:
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", 'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/html; charset=utf-8\r\n\r\n", 'utf-8'))
            self.request.sendall(bytearray("%s\r\n" % html, 'utf-8'))
        elif css:
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n", 'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/css; charset=utf-8\r\n\r\n", 'utf-8'))
            self.request.sendall(bytearray("%s\r\n" % css, 'utf-8'))
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
            self.request.sendall(bytearray("Connection: close\r\n", 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
