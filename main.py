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
def get_owner_and_peches():
    return jsonify(data)  # 👈 tout renvoyé ici

@app.route("/update", methods=["POST"])
def update_data():
    json_data = request.get_json()
    print("[DEBUG] Données reçues :", json_data)

    if not json_data or "owner" not in json_data:
        return jsonify({"error": "Champ 'owner' manquant"}), 400

    data["owner"] = json_data["owner"]

    # Mise à jour des péchés (si présents)
    for peche in data:
        if peche != "owner" and peche in json_data:
            data[peche] = json_data[peche]

    return jsonify({"message": "Données mises à jour avec succès"}), 200

if __name__ == "__main__":
    app.run(debug=True)
