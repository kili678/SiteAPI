# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PECHES = ["Luxure", "Colère", "Envie", "Paresse", "Orgueil", "Gourmandise", "Avarice"]

data = {
    "owner": "Erreur",
    "Luxure": {"name": "Erreur", "avatar": None},
    "Colère": {"name": "Erreur", "avatar": None},
    "Envie": {"name": "Erreur", "avatar": None},
    "Paresse": {"name": "Erreur", "avatar": None},
    "Orgueil": {"name": "Erreur", "avatar": None},
    "Gourmandise": {"name": "Erreur", "avatar": None},
    "Avarice": {"name": "Erreur", "avatar": None},
    "annonces": [],
    "ClassementPeche": [],
    "ClassementJeux": [],
    "apotres": {p: [] for p in PECHES}  # nouveau
}

@app.route("/owner", methods=["GET"])
def get_owner_and_peches():
    # renvoie uniquement owner + péchés (pas annonces)
    out = {"owner": data.get("owner", "Erreur")}
    for p in PECHES:
        out[p] = data.get(p, {"name": "Erreur", "avatar": None})
    return jsonify(out)

@app.route("/annonces", methods=["GET"])
def get_annonces():
    return jsonify({"annonces": data.get("annonces", [])})
    
@app.route("/apotres", methods=["GET"])
def get_apotres():
    return jsonify({"apotres": data.get("apotres", {})})
  
@app.route("/classement", methods=["GET"])
def get_classement():
    return jsonify({
        "ClassementPeche": data.get("ClassementPeche", []),
        "ClassementJeux": data.get("ClassementJeux", [])
    })
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
                
    if "apotres" in json_data:
        if isinstance(json_data["apotres"], dict):
            data["apotres"] = json_data["apotres"]
        else:
            print("[update] apotres non-dict")
            
    if "annonces" in json_data:
        # validation simple : must be list
        if isinstance(json_data["annonces"], list):
            data["annonces"] = json_data["annonces"]
        else:
            print("[update] annonces non-liste")
            
    if "ClassementPeche" in json_data:
        if isinstance(json_data["ClassementPeche"], list):
            data["ClassementPeche"] = json_data["ClassementPeche"]
        else:
            print("[update] ClassementPeche non-liste")
            
    if "ClassementJeux" in json_data:
        if isinstance(json_data["ClassementJeux"], list):
            data["ClassementJeux"] = json_data["ClassementJeux"]
        else:
            print("[update] ClassementJeux non-liste")
            
    return jsonify({"message": "Données mises à jour avec succès"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



