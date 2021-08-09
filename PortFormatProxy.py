import socket
import threading
import sys
from  color import *

# A string of printable and nonprintable characters ('.'dots in this case)
CHARCTERS = ''.join([(chr(i).isprintable()) and chr(i) or '.' for i in range (256)])


# A fucking hex dump >:[
def hexdump(src, length=16):
    src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(CHARCTERS)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x}  ' + red(f'{hexa:<{hexwidth}}') + green(f'  {printable}'))
    
    for line in results:
        print(line)

# Receive data from local or remote 
def receive_from (socketObject):
    buffer = b""
    try:
        while True:
            dataReceived =socketObject.recv(4096)
            if not dataReceived:
                break
            buffer += dataReceived
            # To be removed !!
            # print(buffer)
        return buffer

    except Exception as receiveException:
        print(red("[-]") + f" Exception Occurs During Data Receiving {receiveException}")


# Send dat to local or remote
def send_to (socketObject, buffer):
    try:
        socketObject.send(buffer)

    except Exception as sendException:
        print(red("[-]") + f" Exception Occurs During Data Sending {sendException}")


# def dataDump (buffer):
    


# Route data between local and remote and vice-versa
def proxy(remoteHost, remotePort, clientSocket):
    
    # Connecting to remote host
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSocket.connect((remoteHost, int(remotePort)))

    while True:
        # Contains data received from client (local application)
        localBuffer = receive_from(clientSocket)

        if localBuffer:
            print(green("[<==+]") + " Data Received From Client Application (localhost) " + green("[<==+]"))
            # To do print data dump
            # print(localBuffer)
            print()
            hexdump(localBuffer)
            print()

            # Send data to remote host
            print(blue("[+==>]") + " Sent Data To Remote Host " + blue("[+==>]"))
            # remoteSocket.send(localBuffer)
            send_to(remoteSocket, localBuffer)

        # Contains data received from remote host s
        remoteBuffer = receive_from(remoteSocket)

        if remoteBuffer:
            print(green("[<==+]") + " Data Received From Remote Host " + green("[<==+]"))

            # To do print data dump
            # print(remoteBuffer)
            print()
            hexdump(remoteBuffer)
            print()

            # Send data to client application
            print(blue("[+==>]") + " Sent Data To client appliction (localhost) " + blue("[+==>]"))
            send_to(clientSocket, remoteBuffer)
        
        if not remoteBuffer or not localBuffer:
            clientSocket.close()
            remoteSocket.close()
            print(red("[-]") + " Connection Closed " + red("[-]"))
            break


def proxy_server (localPort, remoteHost, remotePort ):
    
    # Server socket decleration
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Binding the server to localhost and localport specified by the user 
    try:
        server.bind(( '127.0.0.1', localPort))
    except Exception as BindException:
        print(red("[-]") + f" Can't Bind The Server Due To {BindException} " + red("[-]") )
        exit(0)
    
    print(blue("[+]") + f" Start Listning At: 127.0.0.1:{localPort} " + blue("[+]"))
    
    # How many connection
    server.listen(5)

    # Server loop to receive connections
    while True:
        # Accept connection from client
        # Get client socket object and client address infos
        clientSocket, clientAddr = server.accept()
        print(blue("[+]") + f" Connection Received From {clientAddr[0]}:{clientAddr[1]} " + blue("[+]"))

        # Creating Thread to start proxy
        proxyThreadHandler = threading.Thread(target=proxy,args=(remoteHost, remotePort, clientSocket))
        proxyThreadHandler.start()

        
def main ():
    if len(sys.argv) < 3:
        print(green("[!]") + " Usage: " +green("[!]"))
        print("python3 PortFormatProxy.py <localPort> <remotHost> <remotePort>")
        print(green("[?]") + " Example: " + green("[!]"))
        print("python3 PortFormatProxy.py 8081 172.217.18.238 80")
    else:
        proxy_server(int(sys.argv[1]), sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
    

