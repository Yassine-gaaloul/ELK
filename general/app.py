from flask import Flask, render_template, request, redirect
import os
import csv

app = Flask(__name__)

UPLOAD_FOLDER = './data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Vérifie si le fichier a une extension autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer l'upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return f"File {file.filename} uploaded successfully!"
    else:
        return "Invalid file format. Only CSV files are allowed.", 400

# Route de recherche
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Parcourir les fichiers CSV dans le dossier uploadé
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.endswith('.csv'):
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    with open(file_path, 'r') as file:
                        csv_reader = csv.DictReader(file)
                        for row in csv_reader:
                            # Effectuer la recherche sur les valeurs des colonnes
                            if any(query.lower() in str(value).lower() for value in row.values()):
                                results.append(row)
    return render_template('search.html', results=results)

@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
