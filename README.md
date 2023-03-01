# Projet Flask
Mise en place d'une ébauche d'un projet FLASK

mise en place du projet
```bash
pip install virtualenv
virtualenv mon_env
cd mon_env
git clone http://leprojetgit
# pour windows
Scripts/activate.ps1
# pour les autres OS
source bin/activate

pip install -r requirements.txt
python app.py
```
Url d'ajout d'un utilisateur:
```
# /setutilisateur/<nom>/<mot_de_passe>/<email>/<role>
http://localhost:5000/setutilisateur/dev/dev/dev@dev.dev/dev
```
Url de récupération des utilisateurs:
```
http://localhost:5000/getallutilisateurs
```