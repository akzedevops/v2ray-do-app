import os
import qrcode
import base64
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# V2Ray configuration details
V2RAY_CONFIG = {
    "v": "2",
    "ps": "v2ray-do-app",
    "add": "oyster-app-34tkd.ondigitalocean.app",  # This should ideally be dynamic
    "port": "443",
    "id": "34c0808e-ca5e-40c9-8e5d-6bacd84bc564",
    "aid": "0",
    "scy": "auto",
    "net": "ws",
    "type": "none",
    "host": "",
    "path": "/ray",
    "tls": "tls",
    "sni": "",
    "alpn": "",
    "fp": ""
}

# Generate the VMess link
def generate_vmess_link(config):
    json_str = json.dumps(config, separators=(',', ':'))
    encoded_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    return f"vmess://{encoded_str}"

# Generate the QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Save the image to a bytes buffer
    import io
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>V2Ray Configuration</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
        }}
        .vmess-link {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            word-wrap: break-word;
            margin: 20px 0;
            text-align: left;
            font-family: monospace;
            font-size: 12px;
        }}
        .qr-code {{
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 30px;
            color: #777;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Your V2Ray Server is Running</h1>
        <p>Scan the QR code below with your V2Ray client (e.g., v2rayNG) to import the configuration.</p>
        
        <div class="qr-code">
            <img src="/qr-code.png" alt="QR Code for V2Ray Config">
        </div>
        
        <div class="vmess-link">
            <strong>VMess Link:</strong><br>
            {vmess_link}
        </div>
        
        <div class="footer">
            <p>This page is for easy configuration. Keep your UUID secret.</p>
        </div>
    </div>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML page
            vmess_link = generate_vmess_link(V2RAY_CONFIG)
            html_content = HTML_TEMPLATE.format(vmess_link=vmess_link)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/qr-code.png':
            # Serve the QR code image
            vmess_link = generate_vmess_link(V2RAY_CONFIG)
            qr_image_buffer = generate_qr_code(vmess_link)
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(qr_image_buffer.read())
        else:
            # Serve a 404 page for other paths
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Page not found')

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting web server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    # Get the port from the environment variable, default to 8000 if not set
    port = int(os.environ.get('PORT', 8000))
    run_server(port)