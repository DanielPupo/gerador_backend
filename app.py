import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_INSTRUCTION, TEAM_SCHEMA

app = Flask(__name__)
CORS(app)

# Inicialização da API do Gemini
if not GEMINI_API_KEY:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo de ambiente (.env).")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": TEAM_SCHEMA
    },
    system_instruction=SYSTEM_INSTRUCTION
)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "online", "message": "Gerador de Elencos EA FC rodando perfeitamente."}), 200

@app.route("/generate", methods=["POST"])
def generate_team():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "O campo 'prompt' é obrigatório no corpo da requisição."}), 400
        
        user_prompt = data["prompt"]
        
        # Envia a requisição estruturada ao Gemini
        response = model.generate_content(user_prompt)
        
        if not response.text:
            return jsonify({"error": "A IA gerou uma resposta vazia. Tente novamente."}), 500
            
        team_data = json.loads(response.text)
        return jsonify(team_data), 200

    except json.JSONDecodeError:
        return jsonify({"error": "Erro interno ao processar a estrutura JSON retornada pela IA."}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado no backend: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)