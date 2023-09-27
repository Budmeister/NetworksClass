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

def redify(msg):
    return f"{RED}{msg}{RESET}"

def greenify(msg):
    return f"{GREEN}{msg}{RESET}"

def red(msg):
    print(redify(msg))

def green(msg):
    print(greenify(msg))

ICMP_ECHO_REQUEST = 8

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
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff
    
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receive_one_ping(my_socket: socket, id, timeout, dest_addr):
    time_left = timeout
    
    while 1:
        started_select = time.time()
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = (time.time() - started_select)
        if what_ready[0] == []: # Timeout
            return "Request timed out."
        
        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)

        # Fill in start

        # Fetch the ICMP header from the IP packet
        rec_packet = rec_packet[20:]
        (type, code, real_checksum, real_id, sequence, data) = struct.unpack("bbHHhd", rec_packet)
        # The checksum will be different because the pong header is different than the ping header

        is_correct = True
        if type != 0:
            red(f"\tInvalid type - expected: {0}, actual: {type}")
            is_correct = False
        if code != 0:
            red(f"\tInvalid code - expected: {0}, actual: {code}")
            is_correct = False
        if id != real_id:
            red(f"\tInvalid id - expected: {id}, actual: {real_id}")
            is_correct = False
        if dest_addr != addr[0]:
            red(f"\tInvalid pingee address - expected: {dest_addr}, actual: {addr}")
        delay = time_received - data
        if is_correct:
            green(f"\tReceived data: {data}")
            return delay
        else:
            red(f"\tReceived data: {data} (delay={delay})")
            return "Invalid response."



        # Fill in end

        time_left = time_left - how_long_in_select
        if time_left <= 0:
            return "Request timed out."
        
def send_one_ping(my_socket, dest_addr, id):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    my_checksum = 0
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
    packet = header + data

    my_socket.sendto(packet, (dest_addr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object

def do_one_ping(dest_addr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw

    my_socket = socket(AF_INET, SOCK_RAW, icmp)
    my_id = os.getpid() & 0xffff # Return the current process i
    send_one_ping(my_socket, dest_addr, my_id)
    delay = receive_one_ping(my_socket, my_id, timeout, dest_addr)
    my_socket.close()
    return delay

def ping(host, timeout=1, count=4):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print(f"Pinging {host} ({dest}) using Python:")
    print()
    # Send ping requests to a server separated by approximately one second
    for _ in range(count):
        delay = do_one_ping(dest, timeout)
        delay = format_delay(delay)
        print(f"Delay: {delay}")

        time.sleep(1) # one second
    print()

def format_delay(delay):
    if isinstance(delay, str):
        return redify(delay)
    else:
        return greenify(f"{delay * 1000:.4f}ms")

def main():
    hosts = [
        # ("localhost", "localhost"),
        ("google.com", "google.com"),
        # ("letu.edu", "letu.edu"),
        # ("fr.hma.rocks", "fr.hma.rocks (France)"),
        # ("np.hma.rocks", "np.hma.rocks (Nepal)"),
        # ("na.hma.rocks", "na.hma.rocks (Namibia)")
    ]

    print("Starting ping for hosts: ")
    for _, display_name in hosts:
        print(f"\t{display_name}")
    print()

    for host, _ in hosts:
        ping(host)

if __name__ == "__main__":
    main()
