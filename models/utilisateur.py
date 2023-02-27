from flask_sqlalchemy import SQLAlchemy

db_utilisateur = SQLAlchemy()

class Utilisateur(db_utilisateur.Model):
    id = db_utilisateur.Column(db_utilisateur.Integer, primary_key=True)
    nom = db_utilisateur.Column(db_utilisateur.String(80), unique=True, nullable=False)
    mot_de_passe = db_utilisateur.Column(db_utilisateur.String(80), nullable=False)
    role = db_utilisateur.Column(db_utilisateur.String(80), nullable=False)

    def __repr__(self):
        return f'<Utilisateur {self.nom}>'
