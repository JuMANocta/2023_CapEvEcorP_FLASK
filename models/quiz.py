from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), unique=True, nullable=False)
    reponse_1 = db.Column(db.String(255), nullable=False)
    reponse_2 = db.Column(db.String(255), nullable=False)
    reponse_3 = db.Column(db.String(255), nullable=False)
    reponse_4 = db.Column(db.String(255), nullable=False)
    correct_reponse = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f'<Quiz {self.question}>'