from flask import Flask, request, send_file, render_template, abort
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/'
OUTPUT_FILE = 'static/output.png'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.png')
    image_file.save(image_path)

    upscale_command = ['realesrgan-ncnn-vulkan.exe', '-i', image_path, '-o', OUTPUT_FILE]

    try:
        subprocess.run(upscale_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during the upscale process: {e}")
        return 'Error during the upscale process', 500

    return send_file(OUTPUT_FILE, mimetype='image/png')

if __name__ == '__main__':
    app.run()