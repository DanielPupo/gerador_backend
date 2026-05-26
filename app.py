# app.py
import os
import json
import requests
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
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") # Chave obtida diretamente no api-sports.io

client = genai.Client(api_key=GEMINI_API_KEY)

# Inicializa o Flask com suporte a CORS (requisições de outras origens como o app.js)
app = Flask(__name__)
CORS(app)

def buscar_dados_api_football(nome_jogador):
    """
    Busca a foto e dados reais do atleta usando o servidor direto da API-SPORTS.
    """
    if not RAPIDAPI_KEY:
        return None

    # URL oficial direta do fornecedor original
    url = "https://v3.football.api-sports.io/players"
    querystring = {"search": nome_jogador}
    
    # Cabeçalho padrão do provedor direto api-sports
    headers = {
        "x-apisports-key": RAPIDAPI_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=4)
        if response.status_code == 200:
            dados = response.json()
            if dados.get("response") and len(dados["response"]) > 0:
                player_data = dados["response"][0]["player"]
                statistics = dados["response"][0]["statistics"][0] if dados["response"][0]["statistics"] else {}
                
                # Mapeamento inteligente de notas para montar o Card estilo FIFA/EA FC
                rating_str = player_data.get("rating")
                ovr = int(float(rating_str) * 10) if rating_str else 80
                if ovr > 99: ovr = 99

                gols = statistics.get("goals", {}).get("total") or 0
                assistencias = statistics.get("goals", {}).get("assists") or 0
                
                return {
                    "foto": player_data.get("photo") or "",
                    "logo_clube": statistics.get("team", {}).get("logo") or "",
                    "stats": {
                        "ovr": ovr,
                        "pac": 70 + (gols if gols < 20 else 25), 
                        "sho": 68 + (gols if gols < 25 else 30),
                        "pas": 65 + (assistencias * 2 if assistencias < 15 else 30),
                        "dri": 72 + (gols + assistencias if (gols+assistencias) < 20 else 25),
                        "def": 35 + (50 if statistics.get("games", {}).get("position") in ["Defender", "Goalkeeper"] else 0)
                    }
                }
    except Exception as e:
        print(f"Erro ao consultar API-Sports para {nome_jogador}: {e}")
    return None

def generate_team(jogadores):
    # Junta os jogadores enviados pelo usuário em uma única linha de texto
    lista_jogadores = ", ".join(jogadores)
    conteudo_prompt = f"Crie uma escalação utilizando obrigatoriamente estes jogadores: {lista_jogadores}."
    
    try:
        # Faz a chamada para o modelo gerando uma resposta estritamente estruturada em JSON
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=conteudo_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=1.2,                       
                response_mime_type="application/json",
                response_schema=TEAM_SCHEMA # CORREÇÃO: Schema injetado para travar a estrutura do JSON
            )
        )
        
        if response and hasattr(response, 'text') and response.text:
            return response.text
        return None
    except Exception as e:
        print(f"Erro na chamada do Gemini: {e}")
        return None

@app.route("/")
def root():
    return jsonify({
        "status": "success",
        "message": "API Gerador de Escalação ativa e integrada!"
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
    
    # Validação 2: Valida se é uma lista consistente
    if not isinstance(jogadores, list) or len(jogadores) < 3:
        return jsonify({
            "status": "error",
            "message": "Você precisa fornecer uma lista válida de jogadores."
        }), 400
    
    # Pede para o Gemini gerar a escalação (retorna como string JSON)
    escalacao_json_string = generate_team(jogadores)
    
    # Prevenção contra retornos vazios ou instabilidades de rede da IA
    if not escalacao_json_string:
        return jsonify({
            "status": "error",
            "message": "A IA do Gemini enfrentou uma instabilidade temporária ao estruturar a resposta. Por favor, tente enviar novamente."
        }), 502
    
    try:
        # Converte a string JSON estruturada em Dicionário Python
        escalacao_estruturada = json.loads(escalacao_json_string)
        
        # Enriquecimento paralelo com fotos e estatísticas reais da API de futebol
       # === BLOCO DE ENRIQUECIMENTO DE FOTOS BLINDADO ===
        dados_jogadores_reais = {}
        
        def extrair_nome_puro(nome_com_clube):
            # Substitui separadores comuns por uma barra vertical para dar split fácil
            para_limpar = nome_com_clube.replace("(", "|").replace("-", "|").replace("–", "|")
            # Pega apenas a primeira parte (o nome do atleta) e remove espaços inúteis
            return para_limpar.split("|")[0].strip()

        # 1. Buscar fotos para os Titulares
        for jog_completo in escalacao_estruturada.get("jogadores", []):
            nome_limpo = extrair_nome_puro(jog_completo)
            print(f"DEBUG: Buscando na API-Sports por: '{nome_limpo}'") # Log de controle no terminal
            info_real = buscar_dados_api_football(nome_limpo)
            if info_real:
                dados_jogadores_reais[jog_completo] = info_real

        # 2. Buscar fotos para os Reservas
        for jog_completo in escalacao_estruturada.get("jogadores_reservas", []):
            nome_limpo = extrair_nome_puro(jog_completo)
            print(f"DEBUG: Buscando na API-Sports por: '{nome_limpo}'") # Log de controle no terminal
            info_real = buscar_dados_api_football(nome_limpo)
            if info_real:
                dados_jogadores_reais[jog_completo] = info_real

        return jsonify({
            "status": "success",
            "dados_escalacao": escalacao_estruturada,
            "info_real_jogadores": dados_jogadores_reais
        }), 200
        
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Erro ao decodificar a estrutura de dados táticos."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro interno no servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)