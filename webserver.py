from constants import Color
import http.server
import socketserver
import os

PORT = 8000
VIEWER = "viewer.html"

class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # disables logging

def serve_cme_movies(cme_date, port=PORT, directory="."):
    os.chdir(directory)

    handler = SilentHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"{Color.OKCYAN}[INFO]{Color.ENDC}: CME Server: Serving latest CME movies at http://localhost:{port}/{VIEWER}?date={cme_date}")
        httpd.serve_forever()
