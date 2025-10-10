from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ultimo_registro = {}

@app.route('/registro', methods=['POST'])
def receber_dados():
    global ultimo_registro
    dados = request.json
    ultimo_registro = dados
    return jsonify({"status": "ok"})

@app.route('/registro', methods=['GET'])
def obter_dados():
    return jsonify(ultimo_registro)

if __name__ == '__main__':
    app.run(debug=True, port=5000)