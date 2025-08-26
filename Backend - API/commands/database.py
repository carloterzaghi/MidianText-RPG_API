import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("commands/keys/firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
usuarios_collection = db.collection("usuarios")
personagens_collection = db.collection("personagens")
