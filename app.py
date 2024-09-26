from flask import Flask, render_template_string, send_from_directory, abort
import subprocess
import os
import argparse
app = Flask(__name__)

# Keep track of the last modification time for the homepage
last_modified_time = None

@app.route('/')
def home():
    global last_modified_time
    tex_file = 'homepage.tex'
    html_output = 'homepage.html'

    # Get the current modification time of the .tex file
    current_modified_time = os.path.getmtime(tex_file)

    # Only run Pandoc if the file has changed
    if last_modified_time is None or current_modified_time > last_modified_time:
        last_modified_time = current_modified_time
        subprocess.run([
            'pandoc',
            tex_file,
            '-s',
            '-o',
            html_output,
            '--mathjax'
        ], check=True)

    # Read the generated HTML content
    with open(html_output, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Render the HTML content directly
    return render_template_string(html_content)

# Route to serve notebooks as HTML
@app.route('/notebooks/<path:filename>')
def serve_notebook(filename):
    # Sanitize the filename to prevent security issues
    from werkzeug.utils import secure_filename
    filename = secure_filename(filename)

    notebook_path = os.path.join('notebooks', filename)
    if not os.path.exists(notebook_path):
        abort(404)

    # Generate the output HTML filename
    base_name = os.path.splitext(filename)[0]
    html_filename = base_name + '.html'
    html_output_path = os.path.join('notebooks', html_filename)

    # Convert the notebook to HTML using nbconvert
    try:
        subprocess.run([
            'jupyter',
            'nbconvert',
            '--to',
            'html',
            filename,  # Updated to remove 'notebooks/' prefix
            '--output',
            html_filename
        ], check=True, cwd='notebooks', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # Decode and print the error message
        error_message = e.stderr.decode()
        print("Error converting notebook:", error_message)
        abort(500)

    # Read the generated HTML content
    with open(html_output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Optionally, delete the generated HTML file after rendering
    # os.remove(html_output_path)

    # Render the HTML content directly
    return render_template_string(html_content)

# Route to serve images
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)


# if __name__ == '__main__':
#     # Set up argument parser
#     parser = argparse.ArgumentParser(description='Run the Flask application.')
#     parser.add_argument('--host', default='localhost', help='Host to run the app on.')
#     parser.add_argument('--port', default=5000, type=int, help='Port to run the app on.')
#     args = parser.parse_args()
    
#     # Run the app with specified host and port
#     app.run(host=args.host, port=args.port,debug=True)
