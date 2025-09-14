from flask import Flask, request, render_template_string, Response
import requests
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Mini Web Proxy</title></head>
<body>
  <h2>Mini CroxyProxy-like Web Proxy</h2>
  <form method="get" action="/proxy">
    <input type="text" name="url" placeholder="Enter URL" size="50" required>
    <button type="submit">Go</button>
  </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "No URL provided.", 400
    try:
        resp = requests.get(target_url)
        content_type = resp.headers.get('Content-Type', '')
        # Basic HTML rewriting: rewrite href/src to go through proxy
        if 'text/html' in content_type:
            html = resp.text
            # Rewrite links
            html = html.replace('href="', f'href="/proxy?url=')
            html = html.replace('src="', f'src="/proxy?url=')
            return Response(html, content_type=content_type)
        else:
            return Response(resp.content, content_type=content_type)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6767, debug=True)
