
from socket import *
from time import time
from datetime import datetime

RESET = "\x1b[0m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"

def red(msg):
    print(f"{RED}{msg}{RESET}")

def green(msg):
    print(f"{GREEN}{msg}{RESET}")

def get_message(n):
    return f"Ping {n} {datetime.now()}".encode()

def ping(n, address, clientSocket, mintime, maxtime, successes, failures):
    message = get_message(n)
    # address = ("localhost", 12000)
    print(f"Sending ping {n}")
    start = time()
    clientSocket.sendto(message, address)

    try:
        message, address = clientSocket.recvfrom(1024)
        end = time()
        delta = end - start
        message = message.decode()
        green(f"Received message response after {delta:.2f}s:")
        green(f"\"{message}\"")

        mintime = min(mintime, delta)
        maxtime = max(maxtime, delta)
        successes += 1
    except timeout:
        red("Request timed out")
        failures += 1
    
    return mintime, maxtime, successes, failures

def main():
    ip = input("IP: ")
    port = input("Port: ")
    address = (ip, int(port))
    print(f"Pinging {ip}:{port} with 10 pings")

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    # clientSocket.bind(('', 12000))

    mintime = float("inf")
    maxtime = 0
    successes = 0
    failures = 0

    for n in range(10):
        mintime, maxtime, successes, failures = ping(n, address, clientSocket, mintime, maxtime, successes, failures)
    
    print()
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Max ping: {maxtime:.2f}s")
    print(f"Min ping: {mintime:.2f}s")

if __name__ == "__main__":
    main()