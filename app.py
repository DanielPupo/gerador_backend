# app.py
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Importando as configurações e o esquema estruturado do config.py
from config import TEAM_SCHEMA, SYSTEM_INSTRUCTION

# Carrega as variáveis de ambiente e inicia o cliente Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Inicializa o Flask com suporte a CORS (requisições de outras origens)
app = Flask(__name__)
CORS(app)

def generate_team(jogadores):
    # Junta os jogadores enviados pelo usuário em uma única linha de texto
    lista_jogadores = ", ".join(jogadores)
    conteudo_prompt = f"Crie uma escalação utilizando obrigatoriamente estes jogadores: {lista_jogadores}."
    
    # Faz a chamada para o modelo gerando uma resposta estritamente estruturada em JSON
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=1.2,                       # Ajustado para equilíbrio entre criatividade e estabilidade
            response_mime_type="application/json", # Obriga o retorno no formato JSON string
            response_schema=TEAM_SCHEMA             # Aplica as regras estruturais e chaves obrigatórias
        )
    )
    # Retorna o texto puro gerado (que será uma string no formato JSON válido)
    return response.text

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
    
    # Validação 1: O JSON ou a chave 'jogadores' foram enviados?
    if not data or "jogadores" not in data:
        return jsonify({
            "status": "error",
            "message": "Por favor, envie uma lista de jogadores no formato JSON."
        }), 400
        
    jogadores = data.get("jogadores", [])
    
    # Validação 2: É uma lista e possui no mínimo 3 itens? (Mudado para aceitar testes menores se necessário)
    if not isinstance(jogadores, list) or len(jogadores) < 3:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer no mínimo uma lista válida de jogadores."
        }), 400
    
    try:
        # Pede para o Gemini gerar a escalação estruturada
        escalacao_json_string = generate_team(jogadores)
        
        # Converte a string JSON em Dicionário nativo do Python
        escalacao_estruturada = json.loads(escalacao_json_string)
        
        return jsonify({
            "status": "success",
            "jogadores_enviados": jogadores,
            "dados_escalacao": escalacao_estruturada
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar a escalação: {str(e)}"
        }), 500

# Executa o servidor local em modo debug
if __name__ == "__main__":
    app.run(debug=True)