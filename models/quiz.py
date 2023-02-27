from flask_sqlalchemy import SQLAlchemy

db_quiz = SQLAlchemy()

class Quiz(db_quiz.Model):
    id = db_quiz.Column(db_quiz.Integer, primary_key=True)
    question = db_quiz.Column(db_quiz.String(255), unique=True, nullable=False)
    reponse_1 = db_quiz.Column(db_quiz.String(255), nullable=False)
    reponse_2 = db_quiz.Column(db_quiz.String(255), nullable=False)
    reponse_3 = db_quiz.Column(db_quiz.String(255), nullable=False)
    reponse_4 = db_quiz.Column(db_quiz.String(255), nullable=False)
    correct_reponse = db_quiz.Column(db_quiz.String(1), nullable=False)

    def __repr__(self):
        return f'<Quiz {self.question}>'