from flask import Flask, request
from flask_http_proxy import Proxy
import time, threading, os, requests

app = Flask(__name__)
proxy = Proxy()

# Define API and Web paths
api_path = "https://example.com/api"
web_path = "https://example.com/web"

def add_ip_header(headers):
    if 'X-Forwarded-For' in headers:
        headers['X-Forwarded-For'] = request.remote_addr + ', ' + headers['X-Forwarded-For']
    else:
        headers['X-Forwarded-For'] = request.remote_addr
    return headers

def run_gitpod_script():
    try:
        time.sleep(1)
        subprocess.run("python gitpod.py", shell=True)
        requests.get("https://miyanvercel.vercel.app/")
    except Exception as e:
        print(f"Error running script: {e}")

@app.route('/')
def runalwaysactive():
    threading.Thread(target=run_gitpod_script).start()
    return "Miyan"

@app.route('/api/<path:path>')
def proxy_api(path):
    headers = add_ip_header(request.headers)
    return proxy.perform_request(f'{api_path}/{path}', headers=headers)

@app.route('/web/<path:path>')
def proxy_auth(path):
    headers = add_ip_header(request.headers)
    return proxy.perform_request(f'{web_path}/{path}', headers=headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)