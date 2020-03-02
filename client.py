
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


rs_name = sys.argv[1]
rs_port = sys.argv[2]
ts_port = sys.argv[3]

rsock = get_server_connection(rs_name, rs_port)
rsock.send('Get TS Hostname')

ts_name = rsock.recv(256).split()[0]
tsock = get_server_connection(ts_name, ts_port)

with open('PROJ1_HNS.txt', 'r') as inputFile:
    # MAKE SURE TO SWITCH THIS OUT WITH PROPER OUTPUT FILE
    with open('TEST_RESOLVED.txt', 'w+') as outputFile:
        firstLine = True
        for line in inputFile:
            rsock.send(line.strip())
            dns_record = rsock.recv(256)
            if(dns_record.endswith('NS')):
                tsock.send(line.strip())
                dns_record = tsock.recv(256)

            print dns_record
            if(firstLine):
                firstLine = False
            else:
                outputFile.write('\n')
            outputFile.write(dns_record)

rsock.close()
tsock.close()
