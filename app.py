import os
import tika
import zlib
import base64
import datetime
from tika import parser
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'tikka'

#key = Fernet.generate_key()
key = b'QIq6wIzhBFLQk0zvr7VRunMsMmJYI-bfnOjM9e2PGcg='
cipher = Fernet(key)

tika.initVM()

def pretty_date(date):
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')

def pretty_size(num, suffix='B'):
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse(filename):
    parsed = parser.from_file(filename)
    print('Parsing:', filename)
    return parsed

def encrypt(str):
    return base64.urlsafe_b64encode(zlib.compress(cipher.encrypt(str.encode()), 9)).decode()

def decrypt(str):
    return cipher.decrypt(zlib.decompress(base64.urlsafe_b64decode(str))).decode()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filename = ''
    encrypted_filename = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        #if file and allowed_file(file.filename):
        if file:
            filename = secure_filename(file.filename)
            target_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(target_file)
            encrypted_filename = encrypt(filename)
            flash('File: <a href="/d/' + encrypted_filename + '">' + filename + '</a> (<a href="/i/' + encrypted_filename + '">info</a>)')
            return redirect(request.url)
    return render_template('upload.html', filename=filename, encrypted_filename=encrypted_filename)

@app.route('/d/<encrypted_filename>')
def download_file(encrypted_filename):
    filename = decrypt(encrypted_filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

@app.route('/r/<encrypted_filename>')
def remove_file(encrypted_filename):
    filename = decrypt(encrypted_filename)
    source_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(source_file)
    flash('File removed: ' + filename)
    return redirect(url_for('list_files'))

@app.route('/i/<encrypted_filename>')
def parse_file(encrypted_filename):
    filename = decrypt(encrypted_filename)
    source_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    flash('File: <a href="/d/' + encrypted_filename + '">' + filename + '</a> (<a href="/i/' + encrypted_filename + '">info</a>)')
    parsed = parse(source_file)
    return render_template('info.html', filename=filename, parsed=parsed)

@app.route('/u')
def list_files():
    files = list(os.walk(app.config['UPLOAD_FOLDER'], topdown=False))[0][2]
    files.remove('.gitkeep')
    links = list(map(lambda f: encrypt(f), files))
    sizes = list(map(lambda f: pretty_size(os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))), files))
    dates = list(map(lambda f: pretty_date(os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f))), files))
    return render_template('uploads.html', files=files, links=links, sizes=sizes, dates=dates)
