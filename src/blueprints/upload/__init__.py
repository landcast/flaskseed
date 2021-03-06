#!/usr/bin/env python

from flask import g, Blueprint, request, current_app, redirect, flash, \
    send_from_directory, url_for, jsonify
import datetime
import hashlib
import os
# from werkzeug.utils import secure_filename
from src.models import db, session_scope, Teacher

from src.utils import generate_pdf_from_template


from src.models import db, session_scope, Attachment

upload = Blueprint('upload', __name__)


def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    current_app.logger.debug(ext + ', ' + str(ext in current_app.config[
        'ALLOWED_EXTENSIONS']))
    return '.' in filename and ext in current_app.config[
        'ALLOWED_EXTENSIONS']


@upload.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        result = []
        for file in request.files.getlist('file'):
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # secure_filename can't handle chinese filename correctly
                # TODO: find another way to do filename check
                # filename = secure_filename(file.filename)
                hashed_fn = save_attachment(file)
                result.append({'upload_file': file.filename,
                               'download_file': url_for('upload.download_file',
                                                        filename=hashed_fn)})
            else:
                return jsonify({
                    "error": "File format error：pdf, png, jpg, jpeg, gif,ppt"
                }), 500



        return jsonify(result)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    '''


@upload.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)

def save_attachment(file):
    fn = file.filename
    ext = fn.rsplit('.', 1)[1].lower()
    hashed_fn = hashlib.sha256(fn.encode('utf8')).hexdigest()+'.'+ext
    disk_file = os.path.join(current_app.config['UPLOAD_FOLDER'], hashed_fn)
    file.save(disk_file)
    size = os.stat(disk_file).st_size
    updated_by = getattr(g, current_app.config['CUR_ID'])
    with session_scope(db) as session:
        attachment = Attachment(file_name=fn, url_path=hashed_fn, size=size,
                                mime_type=ext, state=1, updated_by=updated_by)
        result = session.add(attachment)
        current_app.logger.debug(result)
    return hashed_fn
