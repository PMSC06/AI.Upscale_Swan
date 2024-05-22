from flask import Flask, request, send_file, render_template
import subprocess
import os
import logging

app = Flask(__name__)

# Configurar o logger
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    if 'image' not in request.files:
        app.logger.error('Nenhuma imagem foi enviada.')
        return 'No image uploaded', 400

    image_file = request.files['image']
    upload_folder = os.path.join(app.root_path, 'static')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    image_path = os.path.join(upload_folder, 'uploaded_image.png')
    try:
        image_file.save(image_path)
        app.logger.info(f'Imagem salva em {image_path}')
    except Exception as e:
        app.logger.error(f'Erro ao salvar a imagem: {e}')
        return 'Failed to save image', 500

    output_image_path = os.path.join(upload_folder, 'output.png')
    try:
        upscale_command = ['realesrgan-ncnn-vulkan.exe', '-i', image_path, '-o', output_image_path]
        app.logger.info(f'ficheiro encontrado')
    except Exception:
        app.logger.error(f'Erro no processo')
        return 'ficheiro nao encontrado', 500
    try:
        subprocess.run(upscale_command, check=True)
        app.logger.info(f'Imagem upscaling salva em {output_image_path}')
    except subprocess.CalledProcessError as e:
        app.logger.error(f'Erro no subprocesso: {e}')
        return 'Upscale process failed', 500
    except Exception as e:
        app.logger.error(f'Erro desconhecido: {e}')
        return 'Unknown error', 500

    try:
        return send_file(output_image_path, mimetype='image/png')
    except Exception as e:
        app.logger.error(f'Erro ao enviar a imagem: {e}')
        return 'Failed to send image', 500

if __name__ == '__main__':
    app.run(debug=True)