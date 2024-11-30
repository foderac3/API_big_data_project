from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import logging
from datetime import datetime

# Configuration de Flask et MongoDB
app = Flask(__name__)
api = Api(app)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["API_bigdata"]
collection = db["bigdata"]
audit_collection = db["audit_logs"]

# Configuration de la journalisation
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Fonction pour enregistrer les actions dans une collection d'audit
def log_action(action, siret):
    audit_collection.insert_one({
        "action": action,
        "siret": siret,
        "timestamp": datetime.now()
    })

# Endpoints CRUD
class SiretResource(Resource):
    # Récupérer un enregistrement par SIRET
    def get(self, siret_id):
        try:
            # Convertir siret_id en entier pour la recherche dans MongoDB
            siret_id = int(siret_id)
        except ValueError:
            logging.warning(f"Le SIRET fourni n'est pas un entier valide : {siret_id}")
            return {"message": "SIRET invalide"}, 400

        logging.info(f"Requête GET sur SIRET: {siret_id}")
        log_action("GET", siret_id)

        record = collection.find_one({"siret": siret_id})
        logging.info(f"Résultat brut MongoDB pour SIRET {siret_id}: {record}")

        if not record:
            logging.warning(f"SIRET non trouvé : {siret_id}")
            return {"message": "SIRET non trouvé"}, 404

        record["_id"] = str(record["_id"])  # Convertir ObjectId en chaîne
        return jsonify(record)

class SiretCreate(Resource):
    # Ajouter un nouvel enregistrement
    def post(self):
        data = request.json
        logging.info(f"Requête POST avec données : {data}")

        if "siret" not in data:
            logging.error("Le champ SIRET est manquant dans la requête POST.")
            return {"message": "Le champ SIRET est requis"}, 400

        collection.insert_one(data)
        logging.info(f"SIRET ajouté avec succès : {data['siret']}")
        log_action("POST", data["siret"])
        return {"message": "Enregistrement ajouté avec succès"}, 201

class SiretUpdate(Resource):
    # Mettre à jour un enregistrement
    def put(self, siret_id):
        try:
            # Convertir siret_id en entier pour la recherche dans MongoDB
            siret_id = int(siret_id)
        except ValueError:
            logging.warning(f"Le SIRET fourni n'est pas un entier valide : {siret_id}")
            return {"message": "SIRET invalide"}, 400

        data = request.json
        logging.info(f"Requête PUT sur SIRET: {siret_id} avec données : {data}")
        log_action("PUT", siret_id)

        result = collection.update_one({"siret": siret_id}, {"$set": data})
        if result.matched_count == 0:
            logging.warning(f"SIRET non trouvé pour mise à jour : {siret_id}")
            return {"message": "SIRET non trouvé"}, 404

        logging.info(f"SIRET mis à jour avec succès : {siret_id}")
        return {"message": "Enregistrement mis à jour avec succès"}, 200

class SiretDelete(Resource):
    # Supprimer un enregistrement
    def delete(self, siret_id):
        try:
            # Convertir siret_id en entier pour la recherche dans MongoDB
            siret_id = int(siret_id)
        except ValueError:
            logging.warning(f"Le SIRET fourni n'est pas un entier valide : {siret_id}")
            return {"message": "SIRET invalide"}, 400

        logging.info(f"Requête DELETE sur SIRET: {siret_id}")
        log_action("DELETE", siret_id)

        result = collection.delete_one({"siret": siret_id})
        if result.deleted_count == 0:
            logging.warning(f"SIRET non trouvé pour suppression : {siret_id}")
            return {"message": "SIRET non trouvé"}, 404

        logging.info(f"SIRET supprimé avec succès : {siret_id}")
        return {"message": "Enregistrement supprimé avec succès"}, 200

# Ajouter les ressources à l'API
api.add_resource(SiretResource, "/siret/<string:siret_id>")
api.add_resource(SiretCreate, "/siret")
api.add_resource(SiretUpdate, "/siret/<string:siret_id>")
api.add_resource(SiretDelete, "/siret/<string:siret_id>")

# Endpoint pour récupérer tous les enregistrements (facultatif)
@app.route("/siret", methods=["GET"])
def get_all_siret():
    logging.info("Requête GET pour récupérer tous les enregistrements.")
    records = list(collection.find())
    for record in records:
        record["_id"] = str(record["_id"])  # Convertir ObjectId en chaîne
    return jsonify(records)

# Vérification des routes disponibles
print("Routes disponibles :")
print(app.url_map)

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
