from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

class QuizNewForm(FlaskForm):
    question = StringField('Question')
    reponse_1 = StringField('Réponse 1')
    reponse_2 = StringField('Réponse 2')
    reponse_3 = StringField('Réponse 3')
    reponse_4 = StringField('Réponse 4')
    correct_reponse = StringField('Réponse correcte')
    submit = SubmitField('Soumettre')