from flask import Flask, render_template, request, redirect, url_for, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['GET'])
def uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('uploads.html', files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    file_path = os.path.join('uploads', filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    return send_file(file_path, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('uploads'))
    else:
        return "Invalid file format", 400

@app.route('/halu')
def halu():
    return "halu from iliyas"
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=8080)
