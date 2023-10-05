from socket import *
import os
import sys
import struct
import time
import select
import binascii

RESET = "\x1b[0m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"

def redify(msg):
    return f"{RED}{msg}{RESET}"

def greenify(msg):
    return f"{GREEN}{msg}{RESET}"

def yellify(msg):
    return f"{YELLOW}{msg}{RESET}"

def red(msg):
    print(redify(msg))

def green(msg):
    print(greenify(msg))

def yellow(msg):
    print(yellify(msg))

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(string):
    csum = 0
    count_to = (len(string) // 2) * 2
    count = 0

    while count < count_to:
        this_val = (string[count+1]) * 256 + (string[count])
        csum = csum + this_val
        csum = csum & 0xffffffff
        count = count + 2
    
    if count_to < len(string):
        csum = csum + string[-1]
        csum = csum & 0xffffffff
    
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    # In the send_one_ping() method of the ICMP Ping exercise, firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header, and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    # Append the checksum to the header.

    # Don't send the packet yet, just return the final packet in this function.

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    my_checksum = 0
    id = os.getpid() & 0xffff # Return the current process i
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, id, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(bytes(header + data))

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        my_checksum = htons(my_checksum) & 0xffff
    else:
        my_checksum = htons(my_checksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, id, 1)

    # print(f"header: {header}")
    # print(f"data: {data}")
    packet = header + data
    return packet

def get_route(hostname):
    time_left = TIMEOUT
    for ttl in range(MAX_HOPS, 0, -1):
        for tries in range(TRIES):
            dest_addr = gethostbyname(hostname)
            print(f"dest_addr: {dest_addr}")

            # Fill in start
            # Make a raw socket named my_socket
            icmp = getprotobyname("icmp")
            # SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw

            my_socket = socket(AF_INET, SOCK_RAW, icmp)
            # Fill in end
            yellow(f"Setting ttl to {ttl}")
            my_socket.setsockopt(IPPROTO_IP, IP_TTL, ttl)
            my_socket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                my_socket.sendto(d, (dest_addr, 0))
                t = time.time()
                started_select = time.time()
                what_ready = select.select([my_socket], [], [], time_left)
                how_long_in_select = time.time() - started_select
                if what_ready[0] == []: # Timeout
                    red("  *           *           *           Request timed out")
                recv_packet, addr = my_socket.recvfrom(1024)
                # print(f"Received packet ({len(recv_packet)}): {recv_packet}")
                time_received = time.time()
                time_left = time_left - how_long_in_select
                if time_left <= 0:
                    red("  *           *           *           Request timed out")
            except timeout:
                continue
            else:
                # Fill in start
                # Fetch the icmp type from the IP packet
                bytes = struct.calcsize("b")
                icmp_type = struct.unpack("b", recv_packet[20:20 + bytes])[0]
                # Fill in end

                if icmp_type == 11:
                    bytes = struct.calcsize("d")
                    time_sent = struct.unpack("d", recv_packet[28:28 + bytes])[0]
                    green(f"Received time send: {time_sent}")
                    yellow("  %d    rtt=%.0fms    %s" %(ttl, (time_received - t) * 1000, addr[0]))

                elif icmp_type == 3:
                    bytes = struct.calcsize("d")
                    time_sent = struct.unpack("d", recv_packet[28:28 + bytes])[0]
                    green(f"Received time send: {time_sent}")
                    yellow("  %d    rtt=%.0fms    %s" %(ttl, (time_received - t) * 1000, addr[0]))
                elif icmp_type == 0:
                    bytes = struct.calcsize("d")
                    time_sent = struct.unpack("d", recv_packet[28:28 + bytes])[0]
                    green(f"Received time send:   {time_sent}")
                    green(f"Actual time send:     {t}")
                    green(f"Actual time received: {time_received}")
                    green("  %d    rtt=%.0fms    %s" %(ttl, (time_received - t) * 1000, addr[0]))
                else:
                    red(f"invalid icmp type: {icmp_type}")
                break
            finally:
                my_socket.close()


def main():
    hosts = [
        ("localhost", "localhost"),
        ("google.com", "google.com"),
        ("letu.edu", "letu.edu"),
        ("fr.hma.rocks", "fr.hma.rocks (France)"),
        ("np.hma.rocks", "np.hma.rocks (Nepal)"),
        # ("na.hma.rocks", "na.hma.rocks (Namibia)")
    ]

    print("Starting ping for hosts: ")
    for _, display_name in hosts:
        print(f"\t{display_name}")

    for host, display_name in hosts:
        print()
        yellow(f"\tFor host: {display_name}")
        print()
        get_route(host)

if __name__ == "__main__":
    main()
