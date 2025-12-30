from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from parser import CodeParser
from generator import DocstringGenerator
import html

app = FastAPI(title="DocGen AI")
generator = DocstringGenerator()


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DocGen AI</title>
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                max-width: 900px; 
                margin: 0 auto; 
                padding: 40px 20px;
                background: #f5f5f5;
            }
            h1 { color: #333; margin-bottom: 5px; }
            .subtitle { color: #666; margin-bottom: 30px; }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
            .tab {
                padding: 10px 20px;
                border: none;
                background: #e0e0e0;
                border-radius: 5px;
                cursor: pointer;
            }
            .tab.active { background: #007bff; color: white; }
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            textarea { 
                width: 100%; 
                height: 300px; 
                font-family: 'Consolas', monospace; 
                font-size: 14px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .upload-area {
                border: 2px dashed #ddd;
                border-radius: 10px;
                padding: 60px;
                text-align: center;
                cursor: pointer;
                transition: border-color 0.3s;
            }
            .upload-area:hover { border-color: #007bff; }
            .upload-area input { display: none; }
            button[type="submit"] { 
                background: #007bff; 
                color: white; 
                padding: 12px 30px; 
                border: none; 
                cursor: pointer; 
                margin-top: 15px;
                border-radius: 5px;
                font-size: 16px;
            }
            button[type="submit"]:hover { background: #0056b3; }
            .file-name { margin-top: 15px; color: #28a745; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>DocGen AI</h1>
        <p class="subtitle">Generate Python docstrings automatically using local AI</p>
        
        <div class="container">
            <div class="tabs">
                <button class="tab active" onclick="showTab('paste')">Paste Code</button>
                <button class="tab" onclick="showTab('upload')">Upload File</button>
            </div>
            
            <div id="paste" class="tab-content active">
                <form action="/generate" method="post">
                    <textarea name="code" placeholder="Paste your Python code here..."></textarea>
                    <button type="submit">Generate Docstrings</button>
                </form>
            </div>
            
            <div id="upload" class="tab-content">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <div class="upload-area" onclick="document.getElementById('file-input').click()">
                        <p>Click to select a .py file or drag and drop</p>
                        <input type="file" id="file-input" name="file" accept=".py" onchange="showFileName(this)">
                        <div class="file-name" id="file-name"></div>
                    </div>
                    <button type="submit">Generate Docstrings</button>
                </form>
            </div>
        </div>
        
        <script>
            function showTab(name) {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                document.querySelector(`.tab-content#${name}`).classList.add('active');
                event.target.classList.add('active');
            }
            function showFileName(input) {
                if (input.files[0]) {
                    document.getElementById('file-name').textContent = 'Selected: ' + input.files[0].name;
                }
            }
        </script>
    </body>
    </html>
    """


def generate_results_html(code: str, filename: str = None):
    """Process code and return results HTML."""
    try:
        parser = CodeParser(code)
        functions = parser.extract_functions()
    except SyntaxError as e:
        return f"""
        <html><body style="font-family: sans-serif; max-width: 900px; margin: 50px auto;">
        <h1>Syntax Error</h1><pre>{e}</pre><a href='/'>← Back</a>
        </body></html>
        """
    
    if not functions:
        return """
        <html><body style="font-family: sans-serif; max-width: 900px; margin: 50px auto;">
        <h1>No Functions Found</h1><p>No functions were detected in the code.</p><a href='/'>← Back</a>
        </body></html>
        """
    
    generated = {}
    results = []
    
    for func in functions:
        if func.has_docstring:
            results.append({"name": func.name, "status": "skipped", "docstring": func.existing_docstring})
        else:
            docstring = generator.generate_docstring(func)
            generated[func.name] = docstring
            results.append({"name": func.name, "status": "generated", "docstring": docstring})
    
    documented_code = parser.insert_docstrings(generated)
    escaped_code = html.escape(documented_code)
    
    title = f"Results for {filename}" if filename else "Results"
    
    response = f"""
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                max-width: 900px; 
                margin: 0 auto; 
                padding: 40px 20px;
                background: #f5f5f5;
            }}
            .container {{
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            pre {{ 
                background: #1e1e1e; 
                color: #d4d4d4; 
                padding: 20px; 
                border-radius: 5px; 
                overflow-x: auto;
                font-size: 14px;
            }}
            .func-box {{ 
                padding: 10px 15px; 
                margin: 10px 0;
                border-radius: 5px;
            }}
            .generated {{ background: #d4edda; }}
            .skipped {{ background: #e2e3e5; }}
            button {{ 
                padding: 10px 20px; 
                border: none; 
                cursor: pointer; 
                border-radius: 5px;
                margin-right: 10px;
            }}
            .copy-btn {{ background: #007bff; color: white; }}
            .back-btn {{ background: #6c757d; color: white; }}
            .stats {{ color: #666; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <p class="stats">Found {len(functions)} functions · Generated {len(generated)} docstrings</p>
    """
    
    for r in results:
        css_class = "generated" if r["status"] == "generated" else "skipped"
        icon = "✓" if r["status"] == "generated" else "○"
        response += f'<div class="func-box {css_class}">{icon} {r["name"]}</div>'
    
    response += f"""
            <h2>Complete Code</h2>
            <pre id="code-output">{escaped_code}</pre>
            <br>
            <button class="back-btn" onclick="window.location='/'">← Back</button>
            <button class="copy-btn" onclick="copyCode()">Copy to Clipboard</button>
            
            <script>
            function copyCode() {{
                const code = document.getElementById('code-output').innerText;
                navigator.clipboard.writeText(code).then(() => alert('Copied!'));
            }}
            </script>
        </div>
    </body>
    </html>
    """
    
    return response


@app.post("/generate", response_class=HTMLResponse)
async def generate_from_paste(code: str = Form(...)):
    return generate_results_html(code)


@app.post("/upload", response_class=HTMLResponse)
async def generate_from_upload(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode('utf-8')
    return generate_results_html(code, file.filename)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)