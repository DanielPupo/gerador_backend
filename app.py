import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from services.gemini_service import gerar_escalacao
from services.football_api import buscar_dados_jogador
from services.team_analyzer import analisar_time

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def root():

    return jsonify({
        "status": "success",
        "message": "FC Ultimate Team AI Online"
    })


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    if not data or "jogadores" not in data:

        return jsonify({
            "status": "error",
            "message": "Lista de jogadores não enviada"
        }), 400

    jogadores = data.get("jogadores")

    if len(jogadores) < 3:

        return jsonify({
            "status": "error",
            "message": "Adicione mais jogadores"
        }), 400

    try:

        resposta_ia = gerar_escalacao(jogadores)

        escalacao = json.loads(resposta_ia)

        info_jogadores = {}

        jogadores_busca = (
            escalacao.get("jogadores", []) +
            escalacao.get("jogadores_reservas", [])
        )

        for jogador in jogadores_busca:

            nome = jogador.split("(")[0].strip()

            dados = buscar_dados_jogador(nome)

            if dados:
                info_jogadores[jogador] = dados

        analise = analisar_time(info_jogadores)

        return jsonify({
            "status": "success",
            "dados_escalacao": escalacao,
            "info_real_jogadores": info_jogadores,
            "analise": analise
        })

    except Exception as erro:

        return jsonify({
            "status": "error",
            "message": str(erro)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)