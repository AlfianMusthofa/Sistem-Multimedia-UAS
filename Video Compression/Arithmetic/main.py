from flask import Flask
from flask import render_template, request, send_file
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

@app.route('/')
def index() :
   return render_template('index.html')

def compress_video(input_path, output_path, target_size):
    # Load the source video
    clip = VideoFileClip(input_path)
    
    duration_adjustment = max(0, (clip.duration - 300) / 60) * 0.1
    adjusted_target_size = target_size * (1 - duration_adjustment)
    
    # Reduce the bitrate to achieve the adjusted target size (in MB)
    bitrate = (adjusted_target_size * 1024 * 8) / clip.duration
    
    # Write the compressed video
    clip.write_videofile(output_path, bitrate=str(int(bitrate)) + 'k')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    target_size = float(request.form['target_size'])
    input_path = os.path.join('uploads', file.filename)
    output_path = os.path.join('compressed', 'compressed_' + file.filename)
    file.save(input_path)
    compress_video(input_path, output_path, target_size)
    return send_file(output_path, as_attachment=True)



if __name__ == '__main__' :
   os.makedirs('uploads', exist_ok=True)
   os.makedirs('compressed', exist_ok=True)
   app.run(debug=True)