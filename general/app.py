from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)

UPLOAD_FOLDER = './data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', alert="Aucune partie de fichier n'a été trouvée.")
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', alert="Aucun fichier n'a été sélectionné.")
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return render_template('index.html', alert=f"Fichier {file.filename} téléchargé avec succès !")
    else:
        return render_template('index.html', alert="Format de fichier invalide. Seuls les fichiers CSV sont autorisés.")

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if allowed_file(filename):
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    with open(filepath, 'r') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if query.lower() in str(row).lower():  # Search case-insensitively in row data
                                results.append(row)
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
