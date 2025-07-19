from flask import Flask, request, jsonify

app = Flask(__name__)

# Stockage temporaire (mémoire vive du serveur)
data = {
    "owner": "Aucun encore"
}

@app.route("/owner", methods=["GET"])
def get_owner():
    return jsonify({"owner": data["owner"]})

@app.route("/update", methods=["POST"])
def update_owner():
    json_data = request.get_json()
    if "owner" in json_data:
        data["owner"] = json_data["owner"]
        return jsonify({"message": "Mise à jour réussie"}), 200
    return jsonify({"error": "Donnée manquante"}), 400
