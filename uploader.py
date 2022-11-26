from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'tar', 'gz', 'zip', 'xlsx', 'xml'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024 * 1024

@app.route('/')
def main_page():
    home_page = f"""
    Use  /upload & ALLOWED_EXTENSIONS ARE {ALLOWED_EXTENSIONS}
    """
    return home_page


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template("upload.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return "successfully uploaded your file "

    # """ enable  below code for downloading the file after uploading """
    # return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                            filename)


if __name__ == '__main__':

    app.run(debug=True)
