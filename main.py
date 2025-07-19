from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage en mémoire vive
data = {
    "owner": "Aucun encore",
    "Luxure": "aucun",
    "Colère": "aucun",
    "Envie": "aucun",
    "Paresse": "aucun",
    "Orgueil": "aucun",
    "Gourmandise": "aucun",
    "Avarice": "aucun"
}

@app.route("/owner", methods=["GET"])
def get_owner():
    return jsonify({"owner": data["owner"]})

@app.route("/peches", methods=["GET"])
def get_peches():
    peches = {k: v for k, v in data.items() if k != "owner"}
    return jsonify(peches)

@app.route("/update", methods=["POST"])
def update_data():
    json_data = request.get_json()
    
    if not json_data or "owner" not in json_data:
        return jsonify({"error": "Champ 'owner' manquant"}), 400

    # Mise à jour de l'owner
    data["owner"] = json_data["owner"]

    # Mise à jour des péchés si présents dans la requête
    for peche in data:
        if peche != "owner" and peche in json_data:
            data[peche] = json_data[peche]

    return jsonify({"message": "Données mises à jour avec succès"}), 200

@app.route("/full", methods=["GET"])
def get_full_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
