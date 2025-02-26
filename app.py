from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import main as main_skin_file  # Ensure 'main.py' contains the correct analysis function

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adjust CORS for security

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/skin_analysis/', methods=['POST'])
def analyze_skin():
    print("requset received")
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    print(file_path)
    file.save(file_path)

    try:
        # Ensure 'main.py' has a function 'analyze_image(file_path)'
        analysis_result = main_skin_file.main(file_path)  # Pass file path to your function
        print("analysis_result>>>>", analysis_result)

        # Optional: Delete the file after analysis
        # os.remove(file_path)

        return jsonify(analysis_result), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Flask API running at: http://192.168.1.77:5000")
    app.run(debug=True, port=5000, host="192.168.1.77")  # Runs on your local IP