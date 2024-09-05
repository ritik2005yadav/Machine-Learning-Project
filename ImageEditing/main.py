from flask import Flask, render_template, request, flash, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_base = filename.rsplit('.', 1)[0]  # Get the file name without the extension
    new_filename = None
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_filename = f"{file_base}_gray.png"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), imgProcessed)
        case "cwebp":
            new_filename = f"{file_base}.webp"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), img)
        case "cjpg":
            new_filename = f"{file_base}.jpg"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), img)
        case "cpng":
            new_filename = f"{file_base}.png"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), img)
        case "resize":
            width = int(request.form.get('width'))
            height = int(request.form.get('height'))
            imgResized = cv2.resize(img, (width, height))
            new_filename = f"{file_base}_resized.png"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), imgResized)
        case "crop":
            x = int(request.form.get('x'))
            y = int(request.form.get('y'))
            crop_width = int(request.form.get('crop_width'))
            crop_height = int(request.form.get('crop_height'))
            imgCropped = img[y:y + crop_height, x:x + crop_width]
            new_filename = f"{file_base}_cropped.png"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), imgCropped)
        case "left":
            imgProcessed = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            new_filename = f"{file_base}_rotated.png"
            cv2.imwrite(os.path.join(app.config['STATIC_FOLDER'], new_filename), imgProcessed)

    return new_filename

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file_path = processImage(filename, operation)
            if new_file_path:
                flash(
                    f"Your image has been processed. Download it <a href='/static/{new_file_path}' download>here</a>."
                )
            else:
                flash("Error processing the image.")
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
