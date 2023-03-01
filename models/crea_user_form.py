from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class NouvelUtilisateurForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    confirmation_mot_de_passe = PasswordField('Confirmation du mot de passe', validators=[DataRequired(), EqualTo('mot_de_passe')])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Créer l\'utilisateur')
