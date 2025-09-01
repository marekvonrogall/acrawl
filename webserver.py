from constants import Color, FETCHING_DATE
import http.server
import socketserver
import os

PORT = 8000
VIEWER = "viewer/cme.html"

class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # disables logging

def serve_cme_movies(cme_date, port=PORT, directory="."):
    os.chdir(directory)

    handler = SilentHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"{Color.OKCYAN}[INFO]{Color.ENDC}: HTTP Server: Serving latest data at http://localhost:{port}/{VIEWER}?cme_date={cme_date}&fetching_date={FETCHING_DATE}")
        httpd.serve_forever()
