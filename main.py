from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 import du module

app = Flask(__name__)
CORS(app)  # 👈 active CORS pour toutes les routes

# Stockage en mémoire vive
# Stockage en mémoire vive
data = {
    "owner": "Erreur",
    "Luxure": {"name": "Erreur", "avatar": None},
    "Colère": {"name": "Erreur", "avatar": None},
    "Envie": {"name": "Erreur", "avatar": None},
    "Paresse": {"name": "Erreur", "avatar": None},
    "Orgueil": {"name": "Erreur", "avatar": None},
    "Gourmandise": {"name": "Erreur", "avatar": None},
    "Avarice": {"name": "Erreur", "avatar": None},
    "annonces": []  # 👈 nouveau champ pour stocker les messages
}

@app.route("/owner", methods=["GET"])
def get_owner_and_peches():
    return jsonify(data)

@app.route("/annonces", methods=["GET"])
def get_annonces():
    return jsonify({"annonces": data.get("annonces", [])})

@app.route("/update", methods=["POST"])
def update_data():
    json_data = request.get_json()
    print("[DEBUG] Données reçues :", json_data)

    if not json_data or "owner" not in json_data:
        return jsonify({"error": "Champ 'owner' manquant"}), 400

    data["owner"] = json_data["owner"]

    if "players" in json_data:
        for peche, info in json_data["players"].items():
            if peche in data:
                data[peche] = info

    # 👇 Nouveau : on stocke les annonces
    if "annonces" in json_data:
        data["annonces"] = json_data["annonces"]

    return jsonify({"message": "Données mises à jour avec succès"}), 200
    

if __name__ == "__main__":
    app.run(debug=True)


