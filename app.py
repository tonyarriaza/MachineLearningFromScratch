from flask import Flask, abort, render_template_string
import nbformat
from nbconvert import HTMLExporter
import os

app = Flask(__name__)

# Path to the directory containing notebooks
NOTEBOOK_DIR = os.path.dirname(os.path.abspath(__file__))
from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Convert the LaTeX document to HTML using Pandoc
    subprocess.run(['pandoc', '-s', 'templates/homepage.tex', '-o', 'templates/homepage.html'], check=True)

    # Serve the generated HTML
    return render_template('output.html')

# @app.route('/')
# def index():
#     # List all .ipynb files in the directory
#     notebooks = [f for f in os.listdir(NOTEBOOK_DIR) if f.endswith('.ipynb')]
#     notebook_links = ''.join([
#         f'<li><a href="/notebook/{nb}">{nb}</a></li>' for nb in notebooks
#     ])
#     return f'''
#     <h1>Available Notebooks</h1>
#     <ul>
#         {notebook_links}
#     </ul>
#     '''

# @app.route('/notebook/<path:notebook_name>')
# def render_notebook(notebook_name):
#     notebook_path = os.path.join(NOTEBOOK_DIR, notebook_name)
#     if not os.path.exists(notebook_path):
#         abort(404)
#     with open(notebook_path, 'r', encoding='utf-8') as f:
#         nb = nbformat.read(f, as_version=4)
#     html_exporter = HTMLExporter()
#     (body, _) = html_exporter.from_notebook_node(nb)
#     return body

if __name__ == '__main__':
    app.run(debug=True)
