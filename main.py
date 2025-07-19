from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = {
    "owner": "inconnu",
    "Luxure": "aucun",
    "Colère": "aucun",
    "Envie": "aucun",
    "Paresse": "aucun",
    "Orgueil": "aucun",
    "Gourmandise": "aucun",
    "Avarice": "aucun"
}

@app.route('/update', methods=['POST'])
def update():
    global data
    content = request.json
    if not content:
        return jsonify({"error": "Aucun JSON reçu"}), 400

    owner = content.get("owner")
    if owner:
        data["owner"] = owner

    for peche in data.keys():
        if peche != "owner":
            val = content.get(peche)
            if val:
                data[peche] = val

    return jsonify({"message": "Données mises à jour"}), 200

@app.route('/owner', methods=['GET'])
def get_owner():
    return jsonify(data)

if __name__ == '__main__':
    app.run()
