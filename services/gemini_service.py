import os

from google import genai
from google.genai import types

from config import TEAM_SCHEMA, SYSTEM_INSTRUCTION

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def gerar_escalacao(jogadores):

    lista_jogadores = ", ".join(jogadores)

    prompt = f"""
    Monte um Ultimate Team competitivo utilizando obrigatoriamente estes jogadores:

    {lista_jogadores}

    Gere:
    - formação ideal
    - análise tática
    - estilo de jogo
    - química do time
    - reservas
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=1.1,
            response_mime_type="application/json",
            response_schema=TEAM_SCHEMA
        )
    )

    return response.text