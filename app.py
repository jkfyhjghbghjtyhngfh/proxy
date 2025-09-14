from flask import Flask, request, Response
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

app = Flask(__name__)

INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head><title>JS-enabled Selenium Proxy</title></head>
<body>
  <h2>JS-enabled Selenium Proxy</h2>
  <form method="get" action="/proxy">
    <input type="text" name="url" placeholder="Enter URL" size="50" required>
    <button type="submit">Go</button>
  </form>
</body>
</html>
'''

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return url if parsed.scheme else "https://" + url

def rewrite_links(html: str, base_url: str) -> str:
    def repl(match):
        attr, link = match.groups()
        absolute = urljoin(base_url, link)
        return f'{attr}="/proxy?url={absolute}"'
    return re.sub(r'(href|src)\s*=\s*["\'](.*?)["\']', repl, html, flags=re.IGNORECASE)

# Initialize a single persistent Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

@app.route("/")
def index():
    return INDEX_HTML

@app.route("/proxy")
def proxy():
    raw_url = request.args.get("url", "").strip()
    if not raw_url:
        return "No URL provided.", 400

    target_url = normalize_url(raw_url)

    try:
        driver.get(target_url)
        html = driver.page_source
        html = rewrite_links(html, target_url)
        return Response(html, content_type="text/html")
    except Exception as e:
        return f"Error loading page: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767, threaded=True, debug=True)
