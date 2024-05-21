from flask import Flask, request, send_file, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    upload_folder = os.path.join(app.root_path, 'static')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    image_path = os.path.join(upload_folder, 'uploaded_image.png')
    image_file.save(image_path)

    output_image_path = os.path.join(upload_folder, 'output.png')
    upscale_command = ['realesrgan-ncnn-vulkan.exe', '-i', image_path, '-o', output_image_path]
    subprocess.run(upscale_command, check=True)

    return send_file(output_image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)