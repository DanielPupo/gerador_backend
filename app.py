# app.py
import os
import json
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from dotenv import load_dotenv

from config import TEAM_SCHEMA, SYSTEM_INSTRUCTION

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Inicializa o cliente oficial da nova biblioteca do Google
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def buscar_dados_api_football(nome_jogador):
    """ Busca a foto e dados reais do atleta usando a API-SPORTS """
    if not RAPIDAPI_KEY:
        return None

    url = "https://v3.football.api-sports.io/players"
    querystring = {"search": nome_jogador}
    headers = {"x-apisports-key": RAPIDAPI_KEY}

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("results", 0) > 0:
                player_info = dados["response"][0]["player"]
                return {
                    "photo": player_info.get("photo"),
                    "id": player_info.get("id"),
                    "nationality": player_info.get("nationality")
                }
    except Exception as e:
        print(f"Erro ao consultar a API-Sports para {nome_jogador}: {e}")
    return None

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "online", "servico": "Gerador Tático EA FC"}), 200

@app.route("/generate", methods=["POST"])
def generate_team():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"status": "error", "message": "Faltando o campo prompt"}), 400

        user_prompt = data["prompt"]

        # Chamada estruturada usando o SDK moderno
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TEAM_SCHEMA,
                system_instruction=SYSTEM_INSTRUCTION
            ),
        )

        if not response.text:
            return jsonify({"status": "error", "message": "Resposta vazia da IA"}), 500

        try:
            escalacao_estruturada = json.loads(response.text)
        except json.JSONDecodeError as exc:
            return jsonify({"status": "error", "message": f"Resposta da IA em formato inválido: {exc}"}), 500
        dados_jogadores_reais = {}

        # Busca enriquecida de fotos para Titulares
        for player in escalacao_estruturada.get("jogadores", []):
            nome = player.get("nome_completo")
            info = buscar_dados_api_football(nome)
            if info:
                dados_jogadores_reais[nome] = info

        # Busca enriquecida de fotos para Reservas
        for player in escalacao_estruturada.get("jogadores_reservas", []):
            nome = player.get("nome_completo")
            info = buscar_dados_api_football(nome)
            if info:
                dados_jogadores_reais[nome] = info

        return jsonify({
            "status": "success",
            "dados_escalacao": escalacao_estruturada,
            "info_real_jogadores": dados_jogadores_reais
        }), 200

    except ClientError as e:
        status_code = getattr(e, "code", None) or 500
        message = str(e)
        if "RESOURCE_EXHAUSTED" in message or "quota" in message.lower() or "429" in message:
            return jsonify({"status": "error", "message": "A API do Gemini excedeu a cota gratuita. Tente novamente mais tarde ou troque de modelo/chave."}), 429
        return jsonify({"status": "error", "message": message}), status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)