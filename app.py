from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1>Hello from a Docker Container!</h1>")

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Starting web server on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()