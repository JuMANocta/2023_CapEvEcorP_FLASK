from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db_utilisateur = SQLAlchemy()

class Utilisateur(db_utilisateur.Model):
    id = db_utilisateur.Column(db_utilisateur.Integer, primary_key=True)
    nom = db_utilisateur.Column(db_utilisateur.String(80), unique=True, nullable=False)
    mot_de_passe = db_utilisateur.Column(db_utilisateur.String(80), nullable=False)
    email = db_utilisateur.Column(db_utilisateur.String(120), unique=True, nullable=False)
    role = db_utilisateur.Column(db_utilisateur.String(80), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)
    
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f'<Utilisateur {self.nom}>'
