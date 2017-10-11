import struct
import socket
import sys


ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris.

ICMP_CODE = socket.getprotobyname('icmp')
ERROR_DESCR = {
    1: ' - Note that ICMP messages can only be '
       'sent from processes running as root.',
    10013: ' - Note that ICMP messages can only be sent by'
           ' users or processes with administrator rights.'
    }

def checksum(source_string):
    #stolen from the gist
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1])*256+ord(source_string[count])
        sum = sum + this_val
        sum = sum & 0xffffffff # Necessary?
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff # Necessary?
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id, dat):
    """Create a new echo request packet based on the given "id"."""
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    if dat:
        data = dat
    else:
        data = 192 * 'Y'
    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)
    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                         socket.htons(my_checksum), id, 1)
    return header + data


def main(dest_addr, dat):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    except socket.error as e:
        if e.errno in ERROR_DESCR:
            # Operation not permitted
            raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
        raise # raise the original error
    try:
        host = socket.gethostbyname(dest_addr)
    except socket.gaierror:
        return
    #packet_id = int((id(timeout) * random.random()) % 65535)
    packet_id = 1337 #this is a special signal
    packet = create_packet(packet_id, dat)
    # The icmp protocol does not use a port, but the function
    # below expects it, so we just give it a dummy port.
    sent = my_socket.sendto(packet, (addr, 1))

if __name__ == "__main__":
    f = open("ips", "r")
    addresses = []
    dat = False
    if len(sys.argv) > 1 and sys.argv[1] == "f":
        dat = sys.argv[2]
    for addr in f:
        main(addr, dat)