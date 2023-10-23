#!/usr/bin/env python3
# I did not feel like configuring lighttpd, nginx or whatever
# so I GPTed this vulnerable http server script
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class VulnerableServer(SimpleHTTPRequestHandler):

    def __init__(self, *args, directory=None, **kwargs):
        self.custom_directory = directory if directory else os.getcwd()
        super().__init__(*args, directory=self.custom_directory, **kwargs)

    def do_GET(self):
        if self.path == "/logs/access_log":
            log_path = os.path.join(self.custom_directory, "logs", "access_log")
            if os.path.exists(log_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                with open(log_path, "r") as file:
                    self.wfile.write(file.read().encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"File not found")
        elif self.path == "/logs":
            logs_path = os.path.join(self.custom_directory, "logs")
            files = os.listdir(logs_path)
            response = "\n".join(files)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            super().do_GET()

    def log_request(self, code='-', size='-'):
        log_path = os.path.join(self.custom_directory, "logs", "access_log")
        log_line = f"{self.client_address[0]} - - [{self.log_date_time_string()}] \"{self.requestline}\" {str(code)} {str(size)}"
        with open(log_path, "a") as file:
            file.write(log_line + "\n")


if __name__ == "__main__":
    custom_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "htdocs")
    logs_path = os.path.join(custom_directory, "logs")

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    log_file_path = os.path.join(logs_path, "access_log")
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as file:
            pass

    httpd = HTTPServer(('localhost', 8080), lambda *args, **kwargs: VulnerableServer(*args, directory=custom_directory, **kwargs))
    print(f"Vulnerable server started at http://localhost:8080 with document root {custom_directory}")
    httpd.serve_forever()
