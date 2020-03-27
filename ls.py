
import sys
import socket
import select


def query_servers(hostname, sock1_tuple, sock2_tuple):
    s1_sock = sock1_tuple[0]
    s1_name = sock1_tuple[1]
    s2_sock = sock2_tuple[0]
    s2_name = sock2_tuple[1]
    s1_sock.send(hostname)
    s2_sock.send(hostname)
    (read_list, _, _) = select.select([s1_sock, s2_sock], [], [], 6)
    if(not read_list):
        return hostname + ' - Error:HOST NOT FOUND'
    else:
        sock = read_list.pop()
        msg = sock.recv(256)
        if(sock == s1_sock):
            return msg + ' ' + s1_name
        else:
            return msg + ' ' + s2_name


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
    print "[S]: Got a connection request from a client at " + str(addr)
    return (ss, csock)


def get_server_connection(hostname, port):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "[C]: Client socket created"
    except socket.error as err:
        print '{} \n'.format("socket open error " + str(err))

    host_ip = socket.gethostbyname(hostname)
    cs.connect((host_ip, int(port)))
    return cs


ls_port = sys.argv[1]
ts1_name = sys.argv[2]
ts1_port = sys.argv[3]
ts2_name = sys.argv[4]
ts2_port = sys.argv[5]

ts1_sock = get_server_connection(ts1_name, ts1_port)
ts2_sock = get_server_connection(ts2_name, ts2_port)
ts1_sock.setblocking(0)
ts2_sock.setblocking(0)

lss, csock = get_client_connection(ls_port)

while True:
    msg = csock.recv(256)
    print msg
    if(msg == ''):
        break
    else:
        dns_record = query_servers(
            msg,
            (ts1_sock, ts1_name),
            (ts2_sock, ts2_name)
        )
        csock.send(dns_record)

lss.close()
ts1_sock.close()
ts2_sock.close()