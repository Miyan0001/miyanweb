from flask import *
import threading, time, subprocess, requests

app = Flask(__name__)

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

def proxy_request(path, target_base_url):
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    headers = add_ip_header(headers)
    response = requests.request(
        method=request.method,
        url=f'{target_base_url}/{path}',
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items() if name.lower() not in excluded_headers]
    return Response(response.content, response.status_code, headers)

@app.route('/api=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    return proxy_request(path, api_path)

@app.route('/web/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_auth(path):
    return proxy_request(path, web_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0')