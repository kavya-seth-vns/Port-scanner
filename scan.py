import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# ==============================
# Professional Port Scanner
# Author: Kavya Seth
# ==============================

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))

            if result == 0:
                try:
                    banner = s.recv(1024).decode().strip()
                except:
                    banner = "No banner"

                print(f"[OPEN] Port {port} | Service: {banner}")
                return port
    except:
        pass
    return None


def main():
    if len(sys.argv) != 4:
        print("Usage: python scan.py <target> <start_port> <end_port>")
        sys.exit(1)

    target_input = sys.argv[1]

    try:
        target = socket.gethostbyname(target_input)
    except socket.gaierror:
        print("[-] Hostname could not be resolved.")
        sys.exit(1)

    try:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except ValueError:
        print("[-] Ports must be integers.")
        sys.exit(1)

    print("=" * 60)
    print(f"Target       : {target_input} ({target})")
    print(f"Port Range   : {start_port} - {end_port}")
    print("Scanning started...")
    print("=" * 60)

    start_time = time.time()
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(target, p),
                               range(start_port, end_port + 1))

        for port in results:
            if port:
                open_ports.append(port)

    end_time = time.time()

    print("\n" + "=" * 60)
    print("Scan Completed")
    print(f"Open Ports    : {open_ports if open_ports else 'None'}")
    print(f"Total Open    : {len(open_ports)}")
    print(f"Time Taken    : {end_time - start_time:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
