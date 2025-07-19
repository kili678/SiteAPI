from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Pour autoriser les appels CORS

data = {
    "owner": "inconnu",
    "PL": "aucun"
}

@app.route('/update', methods=['POST'])
def update():
    global data
    content = request.json
    if not content:
        return jsonify({"error": "Aucun JSON reçu"}), 400

    owner = content.get("owner")
    pl = content.get("PL")

    if owner:
        data["owner"] = owner
    if pl:
        data["PL"] = pl

    return jsonify({"message": "Données mises à jour"}), 200

@app.route('/owner', methods=['GET'])
def get_owner():
    return jsonify(data)

if __name__ == '__main__':
    app.run()
