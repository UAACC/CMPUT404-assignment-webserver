#!/usr/bin/env python
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
import os
import socketserver

def seperate_method(data):
    r_method = data.decode('utf-8').split()[0]
    r_data = data.decode('utf-8').split()[1]

    return r_data, r_method


class MyWebServer(socketserver.BaseRequestHandler):


    #def sendback(self, send):
        #self.request.sendall(send.encode())

#https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
#gets in the type and path
    def check_file_exit(self, path, type):
        if os.path.exists(path):
            f = open(path, 'r')
            value = '\r\n\r\n'+ f.read()
            print(value)
            f.close()
            self.request.sendall(bytearray(
                'HTTP/1.1 200 OK\r\nContent-Type: '+type+'\r\n'+value+'\r\n', 'utf-8'))
            return
        

        else:
            self.request.sendall(
                bytearray("HTTP/1.1 404 Not Found\r\nConnection: close\r\n", 'utf-8'))
            return

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        data, method = seperate_method(self.data)
        #cssContent = None
        #htmlContent = None

        if method != 'GET':
            # 405
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
            return
        elif '.' not in data.split('/')[-1] and data[-1] != '/':
            # 301
            self.request.sendall(bytearray('HTTP/1.1 301 Moved Permanently\r\n', 'utf-8'))
            des_page = data +'/'
            self.request.sendall(bytearray('Location: %s\r\n' %des_page, 'utf-8'))
            return
        else:
            
                

            if 'css' in data:
                type = 'text/css'
            elif 'html' in data:
                type = 'text/html'

                

            elif data[-1] == '/':

                data = data + 'index.html'
                type = 'text/html'

            #if data == "/" or data == "/index.html":
                #for file in os.listdir(os.getcwd()+'/www'):
                    #if file == 'base.css':
                        #f = open(os.getcwd()+'/www/base.css', 'r')
                        #value = f.read()
                       # print(value)
                       # f.close()
                       # cssContent = value
                    #elif file == 'index.html':
                        #f = open(os.getcwd()+'/www/index.html', 'r')
                        #value = f.read()
                        #print(value)
                        #f.close()
                        #htmlContent = value
                        

            #elif htmlContent != None:
                #self.request.sendall(bytearray(
                    #"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"+htmlContent+"\r\n", 'utf-8'))
            ##elif cssContent:
                #self.request.sendall(bytearray(
                    #"HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n"+cssContent+"\r\n", 'utf-8'))
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\nConnection: close\r\n", 'utf-8'))
                return


            
            
            path = 'www' + data
            self.check_file_exit(path, type)
            return



            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
