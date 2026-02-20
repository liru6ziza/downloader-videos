from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import time

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Descargador de Reels, Shorts y TikToks</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; }
            input { width: 80%; max-width: 500px; padding: 12px; font-size: 16px; }
            button { padding: 12px 30px; font-size: 18px; margin-top: 20px; background: #e91e63; color: white; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Descarga videos sin marca de agua</h1>
        <p>Pega el link de TikTok, Instagram Reels o YouTube Shorts</p>
        
        <form id="form" action="/download" method="post">
            <input type="text" name="url" placeholder="https://www.tiktok.com/@usuario/video/123..." required>
            <br>
            <button type="button" onclick="iniciarDescarga()">Descargar</button>
        </form>

        <script>
            function iniciarDescarga() {
                alert("Mostrando anuncio... espera 5 segundos y empezará la descarga 😊");
                setTimeout(() => {
                    document.getElementById('form').submit();
                }, 5000);
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        def generate():
            with open(filename, 'rb') as f:
                yield from f
            time.sleep(1)
            os.remove(filename)

        return app.response_class(generate(), mimetype='video/mp4', headers={
            'Content-Disposition': f'attachment; filename="{os.path.basename(filename)}"'
        })
    except Exception as e:
        return f"¡Ups! Error: {str(e)}<br><a href='/'>Volver</a>", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)