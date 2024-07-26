from flask import Flask, render_template, request, send_file
from PIL import Image, ImageEnhance, ImageFilter
import os
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

img = None
outputImage = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global img
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            img = Image.open(file_path)
            img = img.resize((600, 600))
            img.save(file_path)
            return render_template('index.html', img_path=file_path)
    return render_template('index.html')

def save_image(image, suffix):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'edited_{suffix}_{timestamp}.jpg'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(file_path)
    return send_file(file_path, mimetype='image/jpeg')

@app.route('/brightness', methods=['POST'])
def brightness():
    brightness_value = float(request.form.get('brightness'))
    enhancer = ImageEnhance.Brightness(img)
    enhanced_image = enhancer.enhance(brightness_value)
    return save_image(enhanced_image, 'brightness')

@app.route('/contrast', methods=['POST'])
def contrast():
    contrast_value = float(request.form.get('contrast'))
    enhancer = ImageEnhance.Contrast(img)
    enhanced_image = enhancer.enhance(contrast_value)
    return save_image(enhanced_image, 'contrast')

@app.route('/sharpness', methods=['POST'])
def sharpness():
    sharpness_value = float(request.form.get('sharpness'))
    enhancer = ImageEnhance.Sharpness(img)
    enhanced_image = enhancer.enhance(sharpness_value)
    return save_image(enhanced_image, 'sharpness')

@app.route('/color', methods=['POST'])
def color():
    color_value = float(request.form.get('color'))
    enhancer = ImageEnhance.Color(img)
    enhanced_image = enhancer.enhance(color_value)
    return save_image(enhanced_image, 'color')

@app.route('/rotate', methods=['POST'])
def rotate():
    rotated_image = img.rotate(90)
    return save_image(rotated_image, 'rotate')


@app.route('/blur', methods=['POST'])
def blur():
    blurred_image = img.filter(ImageFilter.BLUR)
    return save_image(blurred_image, 'blur')

@app.route('/resize', methods=['POST'])
def resize():
    resized_image = img.resize((200, 300))
    return save_image(resized_image, 'resize')

@app.route('/crop', methods=['POST'])
def crop():
    cropped_image = img.crop((100, 100, 400, 400))
    return save_image(cropped_image , 'crop')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
