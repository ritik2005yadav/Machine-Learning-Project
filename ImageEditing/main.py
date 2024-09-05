from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
    file_base = filename.rsplit('.', 1)[0]  # Get the file name without the extension
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{file_base}_gray.png"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{file_base}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{file_base}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{file_base}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "resize":
            width = int(request.form.get('width'))
            height = int(request.form.get('height'))
            imgResized = cv2.resize(img, (width, height))
            newFilename = f"static/{file_base}_resized.png"
            cv2.imwrite(newFilename, imgResized)
            return newFilename
        case "crop":
            x = int(request.form.get('x'))
            y = int(request.form.get('y'))
            crop_width = int(request.form.get('crop_width'))
            crop_height = int(request.form.get('crop_height'))
            imgCropped = img[y:y + crop_height, x:x + crop_width]
            newFilename = f"static/{file_base}_cropped.png"
            cv2.imwrite(newFilename, imgCropped)
            return newFilename
        case "left":
            imgProcessed = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            newFilename = f"static/{file_base}_rotated.png"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename



        
    return None

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
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file_path = processImage(filename, operation)
            if new_file_path:
                flash(f"Your image has been processed and is available <a href='/{new_file_path}' target='_blank'>here</a>")
            else:
                flash("Error processing the image.")
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
