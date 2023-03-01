from flask import Flask, render_template, redirect, abort, url_for, request, flash
from flask_bootstrap import Bootstrap
from models.utilisateur import Utilisateur, db_utilisateur
from models.quiz import Quiz, db_quiz
from models.quiz_new_form import QuizNewForm
from models.connexion_form import ConnexionForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models.crea_user_form import NouvelUtilisateurForm


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

@login_manager.user_loader
def load_user(id):
    return Utilisateur.query.get(int(id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/401')
def error_401():
    abort(401)


@app.errorhandler(404)
def error_404(error):
    return ("404"), 404


@app.route('/setutilisateur/<nom>/<mot_de_passe>/<email>/<role>')
def utilisateur(nom, mot_de_passe, email, role):
    mot_de_passe_hash = Utilisateur.set_password(mot_de_passe)
    utilisateur = Utilisateur(
        nom=nom, mot_de_passe=mot_de_passe_hash, email=email, role=role)
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
@login_required
def quiz_new():
    form = QuizNewForm()
    if request.method == 'POST':
        quiz = Quiz()
        form.populate_obj(quiz)
        # Ajout de l'objet dans la session de la base de données
        db_quiz.session.add(quiz)
        db_quiz.session.commit()
        return redirect(url_for('quiz'))
    return render_template('quiz/quiz_new.html', form=form)


@app.route('/quiz/<int:id>', methods=['GET', 'POST'])
@login_required
def quiz_id(id):
    quiz = Quiz.query.get(id)
    if request.method == 'POST':
        reponse = request.form['choice']
        print(quiz.correct_reponse, request.form['choice'])
        if reponse == quiz.correct_reponse:
            return render_template('quiz/quiz_win.html')
        else:
            return render_template('quiz/quiz_lose.html')
    return render_template('quiz/quiz_id.html', quiz=quiz)


@app.route('/quiz_modif/<int:id>', methods=['GET', 'POST'])
@login_required
def quiz_modif(id):
    quiz = Quiz.query.get(id)
    form = QuizNewForm(obj=quiz)
    if request.method == 'POST':
        form.populate_obj(quiz)
        db_quiz.session.commit()
        return redirect(url_for('quiz'))
    return render_template('quiz/quiz_modif.html', form=form)


@app.route('/quiz_delete/<int:id>', methods=['GET', 'POST'])
@login_required
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


@app.route('/nouvelutilisateur', methods=['GET', 'POST'])
def nouvelutilisateur():
    form = NouvelUtilisateurForm()
    if form.validate_on_submit():
        mot_de_passe_hash = Utilisateur.set_password(form.mot_de_passe.data)
        utilisateur = Utilisateur(
            nom=form.login.data, mot_de_passe=mot_de_passe_hash, email=form.email.data, role=form.role.data)
        db_utilisateur.session.add(utilisateur)
        db_utilisateur.session.commit()
        flash('L\'utilisateur a été créé avec succès.')
        return redirect(url_for('index'))
    return render_template('connexion/crea_user.html', title='Nouvel utilisateur', form=form)


@app.route('/moncompte')
@login_required
def moncompte():
    utilisateur = Utilisateur.get_user_by_id(current_user.id)
    return render_template('connexion/moncompte.html', utilisateur=utilisateur, current_user=current_user)

if __name__ == '__main__':
    app.run()
