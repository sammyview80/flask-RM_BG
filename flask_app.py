   
import os
from flask import Flask, flash, request, redirect, url_for, session
from flask_session import Session
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from example_inference import example_inference
from flask import send_from_directory


UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Session(app)
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/rm-bg/<transparent>', methods=['GET', 'POST'])
def upload_file(transparent):
    print(transparent)
    transparent = True if transparent == "true" else False
    print(transparent)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return {"status": "Failed", "message": "Please Provide file name(file)."}
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return  {"status": "Failed", "message": "Filename Not Found."}
        if file and allowed_file(file.filename):
            filename = secure_filename('normal_image.png')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im_path = f"{os.path.dirname(os.path.abspath(__file__))}/images/{filename}"
            rm_image_path = example_inference(im_path, transparent)
            return send_from_directory(app.config["UPLOAD_FOLDER"], rm_image_path)
    return {
        "message": "Get Request not allowed"
    }

if __name__ == '__main__':
    # http_server = WSGIServer(('', 8000), app)
    # http_server.serve_forever()
    app.debug = True
    app.run(port=8000)