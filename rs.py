
import sys
import socket


def load_rs_dict(filename):
    table = {}
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if(stripped_line.endswith('NS')):
                table['NS'] = stripped_line
            else:
                table[stripped_line.split()[0].lower()] = stripped_line
    return table


def get_client_connection(port):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "[S]: Server socket created"
    except socket.error as err:
        print '{} \n'.format("socket open error " + str(err))
    ss.bind(('', int(port)))
    ss.listen(1)
    host = socket.gethostname()
    print "[S]: Server host name is: " + host
    localhost_ip = (socket.gethostbyname(host))
    print "[S]: Server IP address is  " + str(localhost_ip)
    csock, addr = ss.accept()
    print "[S]: Got a connection request from a client at" + str(addr)
    return (ss, csock)


dns_table = load_rs_dict('PROJ1_DNSRS.txt')
rs_port = sys.argv[1]
rss, csock = get_client_connection(rs_port)

while True:
    msg = csock.recv(256)
    print msg
    if(msg == ''):
        break
    elif(msg.lower() in dns_table):
        entry = dns_table[msg.lower()]
        csock.send(entry)
    else:
        csock.send(dns_table['NS'])

rss.close()
