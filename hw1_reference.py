
import threading
import time
import random
import socket as mysoc

# server task


def stringToAscii(string):
    tempString = ""
    for char in string:
        tempString += str(ord(char)) + '_'
    return tempString[0:-1]

def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error " + str(err)))
    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ", host)
    localhost_ip = (mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ", localhost_ip)
    addr = ss.accept()
    print("[S]: Got a connection request from a client at", addr)
    # send a intro  message to the client.
    # msg = "Welcome to CS 352"
    wordFromClient = ""
    
    while True:
        wordFromClient = ss.recv(128)
        # wordFromClient.decode('utf-8')
        if(wordFromClient == ''):
            continue
        print(wordFromClient)
        msg = stringToAscii(wordFromClient)
        ss.send(msg.encode('utf-8'))
        if(wordFromClient == 'EOF'):
            break
    # csockid.send(msg.encode('utf-8'))

    # Close the server socket
    ss.close()
    exit()

# client task


def client():
    try:
        cs = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error " + str(err)))

    # Define the port on which you want to connect to the server
    port = 50007
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    # connect to the server on local machine
    server_binding = (sa_sameas_myaddr, port)
    cs.connect(server_binding)
    # data_from_server = cs.recv(100)
    # receive data from the server

    with open('readFrom.txt', 'r') as inputFile:
        with open('writeTo.txt', 'w+') as outputFile:
            firstLine = True
            for line in inputFile:
                cs.send(line.rstrip('\n').encode('utf-8'))
                dataFromServer = cs.recv(100)
                if(firstLine):
                    firstLine = False
                else:
                    outputFile.write('\n')
                outputFile.write(dataFromServer.decode('utf-8'))
    # close the cclient socket
    cs.close()
    exit()


t1 = threading.Thread(name='server', target=server)
t1.start()
time.sleep(random.random()*5)
t2 = threading.Thread(name='client', target=client)
t2.start()

input("Hit ENTER  to exit")

exit()
