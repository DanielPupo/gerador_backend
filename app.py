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

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Chave fornecida pela API-Football (geralmente via RapidAPI)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") 

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

def buscar_dados_api_football(nome_jogador):
    """
    Busca a foto e estatísticas reais do jogador na API-Football usando o nome.
    Devolve dados reais ou um fallback padrão se não encontrar.
    """
    if not RAPIDAPI_KEY:
        return None

    url = "https://api-football-v1.p.rapidapi.com/v3/players"
    querystring = {"search": nome_jogador}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            # Verifica se a API retornou pelo menos um jogador correspondente
            if dados.get("response") and len(dados["response"]) > 0:
                player_data = dados["response"][0]["player"]
                statistics = dados["response"][0]["statistics"][0] if dados["response"][0]["statistics"] else {}
                
                # Mapeia as estatísticas brutas da API para algo amigável para o card do FIFA
                # Nota baseada em performance (se não houver rating, gera uma estimativa baseada em gols)
                rating_str = player_data.get("rating")
                ovr = int(float(rating_str) * 10) if rating_str else 82
                if ovr > 99: ovr = 99

                # Simulando/Mapeando atributos do FIFA baseados em dados reais para preencher o card
                gols = statistics.get("goals", {}).get("total") or 0
                assistencias = statistics.get("goals", {}).get("assists") or 0
                passes_totais = statistics.get("passes", {}).get("total") or 50
                
                return {
                    "foto": player_data.get("photo") or "",
                    "logo_clube": statistics.get("team", {}).get("logo") or "",
                    "stats": {
                        "ovr": ovr,
                        "pac": 75 + (gols if gols < 20 else 20), # Dinâmico simples baseado em gols
                        "sho": 70 + (gols if gols < 25 else 25),
                        "pas": 65 + (assistencias * 2 if assistencias < 15 else 30),
                        "dri": 75 + (gols + assistencias if (gols+assistencias) < 20 else 20),
                        "def": 30 + (50 if statistics.get("games", {}).get("position") in ["Defender", "Goalkeeper"] else 0)
                    }
                }
    except Exception as e:
        print(f"Erro ao conectar na API-Football para {nome_jogador}: {e}")
    
    return None

def generate_team(jogadores):
    lista_jogadores = ", ".join(jogadores)
    conteudo_prompt = f"Crie uma escalação utilizando obrigatoriamente estes jogadores: {lista_jogadores}."
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conteudo_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=1.2,
            response_mime_type="application/json",
            response_schema=TEAM_SCHEMA
        )
    )
    return response.text

@app.route("/")
def root():
    return jsonify({"status": "success", "message": "API Gerador de Escalação Avançado!"}), 200

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data or "jogadores" not in data:
        return jsonify({"status": "error", "message": "Por favor, envie uma lista de jogadores."}), 400
        
    jogadores = data.get("jogadores", [])
    if not isinstance(jogadores, list) or len(jogadores) < 3:
        return jsonify({"status": "error", "message": "Forneça uma lista válida de jogadores."}), 400
    
    try:
        escalacao_json_string = generate_team(jogadores)
        escalacao_estruturada = json.loads(escalacao_json_string)
        
        # NOVO: Enriquecimento de dados coletando imagens e métricas reais da API-Football
        dados_jogadores_enriquecidos = {}
        
        # Percorre os titulares gerados para buscar os dados visuais e estatísticos reais
        for jog_completo in escalacao_estruturada.get("jogadores", []):
            # Limpa o nome removendo o clube entre parênteses para pesquisar melhor na API
            nome_limpo = jog_completo.split("(")[0].strip()
            info_real = buscar_dados_api_football(nome_limpo)
            if info_real:
                dados_jogadores_enriquecidos[jog_completo] = info_real

        return jsonify({
            "status": "success",
            "dados_escalacao": escalacao_estruturada,
            "info_real_jogadores": dados_jogadores_enriquecidos # Envia o dicionário de fotos/stats reais
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao gerar a escalação: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)