import optparse
from socket import *
import threading
import socket


def connScan(tgtHost, tgtPort):

    try:
        # TODO Create socket
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(2)
        # TODO Connect to target host and port
        server_socket.connect((tgtHost, tgtPort))
        print('[+]%d/tcp open' % tgtPort)
        # TODO Send garbage data (any string you want)
        message = "hello"
        server_socket.sendto(message.encode(), (tgtHost, tgtPort))
        result, serverAdd = server_socket.recvfrom(2048)
        # TODO Get results from sending garbage string
        print('[+]' + result.decode())
        # TODO close the socket
        server_socket.close()

    except timeout:
        print('[-]%d/tcp closed' % tgtPort)


def portScan(tgtHost, tgtPorts):
    try:
        # tgtIP=socket.gethostbyaddr(tgtHost)
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        print('Scanning port ' + tgtPort)
        # TODO thread the scan so that you run connScan for each target on a separate thread.
        thread_scan = threading.Thread(connScan(tgtHost, int(tgtPort)))
        thread_scan.start()


def main():
    parser = optparse.OptionParser(
        "usage%prog "+"-H <target host> -p <target port>")
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',
                      help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(', ')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print('[-] You must specify a target host and port[s].')
        exit(0)
    portScan(tgtHost, tgtPorts)


if __name__ == '__main__':
    main()
