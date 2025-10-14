from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

ultimo_registro = {}
process = None
status_processo = "parado"

@app.route('/registro', methods=['POST'])
def receber_dados():
    global ultimo_registro
    dados = request.json
    ultimo_registro = dados
    return jsonify({"status": "ok"})

@app.route('/registro', methods=['GET'])
def obter_dados():
    return jsonify(ultimo_registro)

@app.route('/toggle', methods=['GET'])
def toggle_safeopear():
    global process, status_processo
    if process is None:
        process = subprocess.Popen(["python", "main/safe_opear.py"])
        status_processo = "iniciado"
        return jsonify({"status": "iniciado"})
    else:
        process.terminate()
        process = None
        status_processo = "parado"
        return jsonify({"status": "parado"})

@app.route('/reset_botao', methods=['GET'])
def reset_botao():
    global process, ultimo_registro, status_processo
    if process:
        process.terminate()
    process = None
    status_processo = "parado"
    ultimo_registro = {}
    return jsonify({"status": "parado"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": status_processo})

if __name__ == '__main__':
    app.run(debug=True, port=5000)