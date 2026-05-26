import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from functools import lru_cache

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


@lru_cache(maxsize=200)
def buscar_dados_jogador(nome_jogador):

    if not RAPIDAPI_KEY:
        return None

    url = "https://v3.football.api-sports.io/players"

    headers = {
        "x-apisports-key": RAPIDAPI_KEY
    }

    querystring = {
        "search": nome_jogador
    }

    try:
        response = session.get(
            url,
            headers=headers,
            params=querystring,
            timeout=10
        )

        if response.status_code != 200:
            return None

        dados = response.json()

        if not dados.get("response"):
            return None

        jogador = dados["response"][0]

        player = jogador.get("player", {})
        statistics = jogador.get("statistics", [])

        stats = statistics[0] if statistics else {}

        gols = stats.get("goals", {}).get("total") or 0
        assists = stats.get("goals", {}).get("assists") or 0
        jogos = stats.get("games", {}).get("appearences") or 1
        minutos = stats.get("games", {}).get("minutes") or 0
        nota = stats.get("games", {}).get("rating")

        try:
            overall = int(float(nota) * 10) if nota else 80
        except:
            overall = 80

        overall = max(70, min(overall, 99))

        posicao = stats.get("games", {}).get("position", "Midfielder")

        defending = 40

        if posicao in ["Defender", "Goalkeeper"]:
            defending = 82

        return {
            "nome": player.get("name"),
            "idade": player.get("age"),
            "nacionalidade": player.get("nationality"),
            "altura": player.get("height"),
            "peso": player.get("weight"),
            "foto": player.get("photo"),
            "time": stats.get("team", {}).get("name"),
            "logo_time": stats.get("team", {}).get("logo"),
            "liga": stats.get("league", {}).get("name"),
            "estatisticas": {
                "overall": overall,
                "pace": min(99, 70 + gols),
                "shooting": min(99, 68 + gols),
                "passing": min(99, 65 + assists * 2),
                "dribbling": min(99, 72 + gols + assists),
                "defending": defending,
                "physical": 78,
                "gols": gols,
                "assistencias": assists,
                "jogos": jogos,
                "minutos": minutos
            }
        }

    except Exception as erro:
        print(f"Erro API Football: {erro}")
        return None