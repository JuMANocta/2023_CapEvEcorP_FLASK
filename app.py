from flask import Flask, render_template, redirect, abort, jsonify, url_for, request, send_from_directory, flash
from flask_bootstrap import Bootstrap
from models.utilisateur import Utilisateur, db_utilisateur
from models.quiz import Quiz, db_quiz
from models.quiz_new_form import QuizNewForm
from models.connexion_form import ConnexionForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash


app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py')

Bootstrap(app)
db_utilisateur.init_app(app)
db_quiz.init_app(app)

with app.app_context():
    db_utilisateur.create_all()
    db_quiz.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'connexion'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page'

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/bootstrap')
def bootstrap():
    return render_template('bootstrap.html')

@app.route('/salut')
def salut():
    return 'Salut'

@app.route('/salut/<nom>')
def test_name(nom):
    from datetime import datetime # importation de datetime
    maintenant = datetime.now() # récupération de la date et de l'heure actuelle
    jour = maintenant.day # récupération du jour
    jours_de_la_semaine_fr = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'] # création d'une liste des jours de la semaine en français
    jour_semaine = jours_de_la_semaine_fr[maintenant.weekday()] # récupération du jour de la semaine en français
    mois = maintenant.month # récupération du mois
    annee = maintenant.year # récupération de l'année
    return render_template('salut.html', nom=nom, jour=jour, mois=mois, annee=annee ,jour_semaine=jour_semaine)

@app.route('/google')
def google():
    return redirect('https://google.com')

@app.route('/401')
def error_401():
    abort(401)

@app.errorhandler(404)
def error_404(error):
    return ("404"), 404

@app.route('/json')
def json():
    data = {'key': 'value', 'key2': 'value2', 'key3': 'value3'}
    return jsonify(data)

@app.route('/setutilisateur/<nom>/<mot_de_passe>/<email>/<role>')
def utilisateur(nom, mot_de_passe,email, role):
    mot_de_passe_hache = generate_password_hash(mot_de_passe)
    utilisateur = Utilisateur(nom=nom, mot_de_passe=mot_de_passe_hache, email=email,role=role)
    db_utilisateur.session.add(utilisateur)
    db_utilisateur.session.commit()
    return 'Utilisateur ajouté'

@app.route('/getutilisateur/<id>')
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get(id)
    return f'Utilisateur {utilisateur.nom, utilisateur.mot_de_passe}'

@app.route('/getallutilisateurs')
def get_all_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return f'Utilisateurs {[(utilisateur.nom, utilisateur.mot_de_passe, utilisateur.email, utilisateur.role) for utilisateur in utilisateurs]}'

@app.route('/htmlutilisateurs')
def html_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return render_template('utilisateurs.html', utilisateurs=utilisateurs)

@app.route('/quiz')
def quiz():
    quiz = Quiz.query.all()
    return render_template('quiz/quiz.html', quiz=quiz)

@app.route('/quiz_new', methods=['GET', 'POST'])
def quiz_new():
    form = QuizNewForm()
    if request.method == 'POST':
        quiz = Quiz()
        form.populate_obj(quiz)
        db_quiz.session.add(quiz) # Ajout de l'objet dans la session de la base de données
        db_quiz.session.commit()
        return redirect(url_for('quiz'))
    return render_template('quiz/quiz_new.html', form=form)

@app.route('/quiz/<int:id>', methods=['GET', 'POST'])
def quiz_id(id):
    quiz = Quiz.query.get(id)
    if request.method == 'POST':
        reponse = request.form['choice']
        print(quiz.correct_reponse, request.form['choice'])
        if reponse == quiz.correct_reponse:
            return render_template('quiz/quiz_win.html')
        else:
            return render_template('quiz/quiz_lose.html')
    return render_template('quiz/quiz_id.html',quiz=quiz)

@app.route('/quiz_modif/<int:id>', methods=['GET', 'POST'])
def quiz_modif(id):
    quiz = Quiz.query.get(id)
    form = QuizNewForm(obj=quiz)
    if request.method == 'POST':
        form.populate_obj(quiz)
        db_quiz.session.commit()
        return redirect(url_for('quiz'))
    return render_template('quiz/quiz_modif.html', form=form)

@app.route('/quiz_delete/<int:id>', methods=['GET', 'POST'])
def quiz_delete(id):
    quiz = Quiz.query.get(id)
    db_quiz.session.delete(quiz)
    db_quiz.session.commit()
    return redirect(url_for('quiz'))

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ConnexionForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(nom=form.login.data).first()
        if utilisateur is None or not utilisateur.check_password(form.mot_de_passe.data):
            flash('Email ou mot de passe invalide')
            return redirect(url_for('connexion'))

        login_user(utilisateur, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('connexion/connexion.html', form=form)

@app.route('/deco')
def deconnexion():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return Utilisateur.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)
