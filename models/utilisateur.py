from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db_utilisateur = SQLAlchemy()

class Utilisateur(UserMixin, db_utilisateur.Model):
    id = db_utilisateur.Column(db_utilisateur.Integer, primary_key=True)
    nom = db_utilisateur.Column(db_utilisateur.String(80), unique=True, nullable=False)
    mot_de_passe = db_utilisateur.Column(db_utilisateur.String(80), nullable=False)
    email = db_utilisateur.Column(db_utilisateur.String(120), unique=True, nullable=False)
    role = db_utilisateur.Column(db_utilisateur.String(80), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)
    
    def genPassHash(mot_de_passe):
        return generate_password_hash(mot_de_passe)
    
    # récupérer l'utilisateur par son id
    def get_user_by_id(id):
        return Utilisateur.query.get(id)
    
    def __repr__(self):
        return f'<Utilisateur {self.nom}>'
