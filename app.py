# app.py (Parte 1)
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Importando o que criamos no outro arquivo:
from config import TEAM_SCHEMA, SYSTEM_INSTRUCTION

# Carrega as variáveis de ambiente e inicia o Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Inicializa o Flask
app = Flask(__name__)
CORS(app)

# app.py (Parte 2)

def generate_team(jogadores):
    # Junta os jogadores enviados em uma única linha de texto
    lista_jogadores = ", ".join(jogadores)
    conteudo_prompt = f"Crie uma escalação utilizando obrigatoriamente estes jogadores: {lista_jogadores}."
    
    # Faz a chamada para o modelo pedindo uma resposta estruturada em JSON
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=1.2, # Reduzido levemente de 1.8 para evitar respostas desconexas
            response_mime_type="application/json", # Garante o retorno em JSON
            response_schema=TEAM_SCHEMA             # Aplica as regras do seu config.py
        )
    )
    return response.text

# app.py (Parte 3)

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Gerador de Escalação!",
        "version": "1.0"
    }), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    
    # Validação 1: O JSON foi enviado?
    if not data or "jogadores" not in data:
        return jsonify({
            "status": "error",
            "message": "Por favor, envie uma lista de jogadores no formato JSON."
        }), 400
        
    jogadores = data.get("jogadores", [])
    
    # Validação 2: É uma lista e possui no mínimo 11 itens?
    if not isinstance(jogadores, list) or len(jogadores) < 3:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer no mínimo 11 jogadores."
        }), 400
    
    try:
        # Pede para o Gemini gerar a escalação (retorna como string JSON)
        escalacao_json_string = generate_team(jogadores)
        
        # Converte a string JSON em Dicionário Python para o Flask organizar a resposta
        escalacao_estruturada = json.loads(escalacao_json_string)
        
        return jsonify({
            "status": "success",
            "jogadores_enviados": jogadores,
            "dados_escalacao": escalacao_estruturada
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar a escalção: {str(e)}"
        }), 500

# Executa o servidor local
if __name__ == "__main__":
    app.run(debug=True)