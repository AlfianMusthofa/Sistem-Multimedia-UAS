from flask import Flask, render_template, request, send_file
import os
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_video():
    if 'video' not in request.files:
        return "No video file provided."

    video_file = request.files['video']
    if video_file.filename == '':
        return "No selected file."

    # Save the uploaded video temporarily
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, 'input_video.mp4')
    video_file.save(temp_path)

    compressed_path = os.path.join(temp_dir, 'compressed_video.mp4')
    subprocess.run(['cp', temp_path, compressed_path])

    # Clean up temporary files
    os.remove(temp_path)

    return send_file(compressed_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8001)
