from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Utilisateur {self.nom}>'
