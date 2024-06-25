from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
import numpy as np
from compression_algorithms import huffman_encoding, arithmetic_encoding
from fractions import Fraction

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        image = Image.open(file_path).convert('L')  # convert image to grayscale
        image_data = np.array(image)

        # Apply Huffman Encoding
        huffman_result, huffman_codes = huffman_encoding(image_data)
        huffman_compressed_size = len(huffman_result)

        # Apply Arithmetic Encoding
        arithmetic_result, probabilities = arithmetic_encoding(image_data)
        arithmetic_compressed_size = len(str(Fraction(arithmetic_result).limit_denominator(1000000)))  # Approximation of compressed size

        original_size = image_data.size * 8  # in bits
        
        # Results
        huffman_ratio = huffman_compressed_size / original_size
        arithmetic_ratio = arithmetic_compressed_size / original_size

        # Save compressed images for display
        huffman_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'huffman_' + filename)
        arithmetic_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'arithmetic_' + filename)

        # For simplicity, we will just save the original image under new names
        # In a real-world scenario, you would save the decompressed image after compression
        image.save(huffman_image_path)
        image.save(arithmetic_image_path)

        return render_template('index.html', 
                               original_image_url=file_path,
                               huffman_image_url=huffman_image_path,
                               arithmetic_image_url=arithmetic_image_path,
                               original_size=original_size,
                               huffman_compressed_size=huffman_compressed_size,
                               arithmetic_compressed_size=arithmetic_compressed_size,
                               huffman_ratio=huffman_ratio,
                               arithmetic_ratio=arithmetic_ratio)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
