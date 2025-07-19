from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running"

@app.route('/owner', methods=['POST'])
def receive_owner_data():
    try:
        data = request.json
        print("[API] ✅ Données reçues :", data)

        # Tu peux les stocker, logguer ou traiter ici
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"[API] ❌ Erreur de traitement : {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
