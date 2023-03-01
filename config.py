# clef générée avec la commande suivante:
# pip install pycryptodome
# python -c "from Crypto.Random import get_random_bytes; import binascii; print(binascii.hexlify(get_random_bytes(16)))"
SECRET_KEY = 'eff57466aade280635ed29ee94f8ae79'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
DEBUG = True