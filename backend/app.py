from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import werkzeug
from transformers import AutoModelForCausalLM, AutoTokenizer
import pymongo
from pymongo import MongoClient
from parse_cvs import parse_cv

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

@app.route('/')
def index():
    return 'Hello, world!'

client = MongoClient("mongodb://localhost:27017/")  # Ejemplo de conexión local
db = client["cvs"]  # Nombre de la base de datos
collection = db["curriculums"]  # Nombre de la colección

# ... (tus rutas /files, /files/<filename>, /uploads/<filename>, /chatbot)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = werkzeug.utils.secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parsear el CV y obtener el JSON
        try:
            cv_json = parse_cv(filepath)
        except ValueError as e:
            return jsonify({'message': str(e)}), 400  # Manejo de errores

        # Insertar en MongoDB
        collection.insert_one(cv_json) 
        
        # Opcional: Eliminar el archivo después de procesarlo
        # os.remove(filepath)

        return jsonify({'message': 'CV subido, parseado y almacenado en MongoDB con éxito'})

    else:
        return jsonify({'message': 'Invalid file type'}), 400

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully'})
    else:
        return jsonify({'message': 'File not found'}), 404

@app.route('/uploads/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.json['message']
    response = process_message(message)
    return jsonify({'response': response})

def process_message(message):

    # Generar respuesta con DialoGPT
    new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = new_user_input_ids

    # Generar la respuesta del chatbot
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=100,
        top_p=0.7,
        temperature=0.8
    )

    # Decodificar la respuesta
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)