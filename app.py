from flask import Flask, render_template, redirect, abort, jsonify
from flask_bootstrap import Bootstrap
from models.utilisateur import Utilisateur, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bootstrap')
def test():
    return render_template('bootstrap.html')

@app.route('/salut')
def salut():
    return 'Salut'

@app.route('/salut/<nom>')
def test_name(nom):
    #return f'Salut {nom} !'
    return render_template('salut.html', nom=nom)

@app.roote('/google')
def google():
    return redirect('https://google.com')

@app.route('/401')
def error_401():
    abort(401)

@app.route('/json')
def json():
    data = {'key': 'value', 'key2': 'value2', 'key3': 'value3'}
    return jsonify(data)

@app.route('/setutilisateur/<nom>/<mot_de_passe>')
def utilisateur(nom, mot_de_passe):
    utilisateur = Utilisateur(nom=nom, mot_de_passe=mot_de_passe)
    db.session.add(utilisateur)
    db.session.commit()
    return 'Utilisateur ajouté'

@app.route('/getutilisateur/<id>')
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get(id)
    return f'Utilisateur {utilisateur.nom, utilisateur.mot_de_passe}'

@app.route('/getallutilisateurs')
def get_all_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return f'Utilisateurs {utilisateurs}'

@app.route('/htmlutilisaterus')
def html_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return render_template('utilisateurs.html', utilisateurs=utilisateurs)

app.run()
