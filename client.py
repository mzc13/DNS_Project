
import sys
import socket


def get_server_connection(hostname, port):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "[C]: Client socket created"
    except socket.error as err:
        print '{} \n'.format("socket open error " + str(err))

    host_ip = socket.gethostbyname(hostname)
    cs.connect((host_ip, int(port)))
    return cs


ls_name = sys.argv[1]
ls_port = sys.argv[2]

lsock = get_server_connection(ls_name, ls_port)

with open('PROJ2_HNS.txt', 'r') as inputFile:
    # MAKE SURE TO SWITCH THIS OUT WITH PROPER OUTPUT FILE
    with open('TEST_RESOLVED.txt', 'w+') as outputFile:
        firstLine = True
        for line in inputFile:
            lsock.send(line.strip())
            dns_record = lsock.recv(256)
            print dns_record
            if(firstLine):
                firstLine = False
            else:
                outputFile.write('\n')
            outputFile.write(dns_record)

lsock.close()
