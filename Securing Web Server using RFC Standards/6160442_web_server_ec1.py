#!/usr/bin/env python3

import argparse
import os.path
from os import path
import sys
import itertools
import socket
from socket import socket as Socket
import ssl

# A simple web server


def main():

    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', args.port))
        server_socket.listen(1)
        with context.wrap_socket(server_socket, server_side=True) as server_socket1:

            print("server ready")

            while True:

                with server_socket1.accept()[0] as connection_socket:
                    # This is a hackish way to make sure that we can receive and process multi
                    # line requests.
                    request = ""
                    received = connection_socket.recv(1024).decode('utf-8')
                    request += received
                    # splitting the request recieved for getting the filename.
                    r = request.split("\r\n")[0].split(" ")
                    filename = r[1]
                    f = open('.' + filename)  # opening the requested file.
                    # reading the contents of the file and saving it in a variable.
                    content = f.read()
                    # looping through the content.
                    for i in range(0, len(content)):
                        # sending the content in the file through the connection.
                        connection_socket.send(content[i].encode())
                    # calling the function to handle the request recieved  so that correct http request can be saved.
                    reply = http_handle(request)
                    # connection_socket.sendall(reply.encode('utf-8'))

                print("\n\nReceived request")
                print("======================")
                print(request.rstrip())
                print("======================")

                print("\n\nReplied with")
                print("======================")
                print(reply.rstrip())
                print("======================")

        return 0


def http_handle(request_string):
    """Given a http requst return a response

    Both request and response are unicode strings with platform standard
    line endings.
    """

    # send data per line
    # getting the request line
    request = request_string.split("\r\n")[0].split(" ")

    # splitting the request line into method, url and the version
    method = request[0]
    url = request[1]
    version = request[2]
    # creating a new dictionary for storing Key-value pairs
    dictionary = {"METHOD": method, "URL": url, "VERSION": version}

    # if this condition satisfies then '200 ok' along with some html is sent as the response message
    if method == 'GET' and url == '/' or url == '/index.html' and version == 'HTTP/1.1':
        response = "200 OK \n \n"
        #response+= data

    # If the request method is other than GET method then will reply with '501 Not Implemented' message
    # This HTTP response means that this request method is not supported by the server and it cannot handle it.
    if method != 'GET':
        response = '501 Not Implemented \n'

    # If the version in the request line is not compliant then we will reply with "505 HTTP Version Not Supported" message.
    # This HTTP repsonse means that the server does not support this HTTP version
    if version != 'HTTP/1.1':
        response = "505 HTTP Version Not Supported \n"

    # If the file requested by the client is not present as the server path then we will reply with "HTTP 404 File not found" message.
    if path.exists("." + url) == False:
        response = "HTTP 404 File not found \n"

    # if the request entered is in the wrong format then we will return '400 Bad Request' message
    # This HTTP response means that the request made is incorrectly formatted.
    if len(request) != 3:
        response = '400 Bad Request \n'
    if "favicon" in request_string:
        data = "HTTP/1.1 404 Not Found \r\n\r\n"

    # returning the response based on the request made.
    return response

    #assert not isinstance(request_string, bytes)

    # Fill in the code to handle the http request here. You will probably want
    # to write additional functions to parse the http request into a nicer data
    # structure (e.g., not a string) and to easily create http responses.

    # Used Figure 2.8 in book as guideline: Request line and Header lines
    # Step 0: Split the string by line

    # Step 1: Get the first line (request line) and split into method, url, version
    # Step 2: Until you see <CR><LF> (\r\n), read lines as key, value with header name and value. Store as a dictionary
    # Step 3: Check to make sure method, url, and version are all compliant
    # Step 3a: if method is a GET and url is "/" or "/index.html" and correct HTTP version, we need to respond with 200 OK and some HTML
    # Step 3b: If method is compliant, but not implemented, we need to respond with a correct HTTP response
    # Step 3c: If the version is not compliant, we need to respond with correct HTTP response
    # Step 3d: If file does not exist in server path, respond with HTTP 404 File not found response
    # Step 4: Checking to make sure headers are correctly formatted

    raise NotImplementedError

    pass


if __name__ == "__main__":
    sys.exit(main())
