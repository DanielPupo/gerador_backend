# config.py

# Dicionário que mapeia e instrui o Gemini a responder de forma estritamente estruturada
TEAM_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_time": {
            "type": "STRING", 
            "description": "O nome criativo, imponente e personalizado da escalação ou time"
        },
        "quantidade_de_jogadores": {
            "type": "STRING", 
            "description": "Quantidade de jogadores totais detalhada por extenso (ex: '11 jogadores titulares e 5 reservas')"
        },
        "qualidades_do_time": {
            "type": "STRING", 
            "description": "Descrição detalhada sobre a técnica, velocidade, força e entrosamento tático do time"
        },
        "jogadores": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista contendo EXATAMENTE 11 jogadores titulares da escalação principal organizada por ordem de posição (Goleiro primeiro)"
        },
        "jogadores_reservas": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista de jogadores reservas ou suplentes extras sugeridos por você para complementar o elenco"
        },
        "variabilidade_do_time": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista de instruções sobre variações de esquemas táticos possíveis e comportamento da equipe em campo"
        }
    },
    "required": ["nome_do_time", "quantidade_de_jogadores", "qualidades_do_time", "jogadores", "jogadores_reservas", "variabilidade_do_time"]
}

SYSTEM_INSTRUCTION = """
Você é um Técnico de futebol profissional renomado e um analista tático genial. 
Sua tarefa é criar escalações incríveis utilizando obrigatoriamente os jogadores fornecidos pelo usuário no time titular. 

Regras de Negócio, Posicionamento e Estilo:
1. IDIOMA: Você deve preencher todos os campos do esquema fornecido estritamente em português brasileiro.
2. ORDEM DOS TITULARES: Na lista 'jogadores', você deve inserir exatamente 11 atletas na seguinte ordem tática de posições:
   - O primeiro jogador (índice 0) DEVE ser o Goleiro.
   - Do segundo ao quinto jogador (índices 1 a 4) DEVEM ser os Defensores (Zagueiros/Laterais).
   - Do sexto ao nono jogador (índices 5 a 8) DEVEM ser os Meio-Campistas.
   - Os dois últimos jogadores (índices 9 e 10) DEVEM ser os Atacantes.
3. FORMATAÇÃO OBRIGATÓRIA DE NOME: Cada jogador dentro das listas de titulares e de reservas DEVE seguir estritamente o padrão de texto com o nome e o clube/país histórico entre parênteses. Exemplo: 'Neymar (Santos)' ou 'Pelé (Brasil)' ou 'Cristiano Ronaldo (Real Madrid)'. Não quebre este padrão de parênteses sob hipótese alguma.
4. COMPLEMENTO DE ELENCO: Utilize os jogadores enviados pelo usuário prioritariamente nos titulares. Se faltarem posições para fechar os 11 titulares ou se o usuário enviar atletas extras, jogue os atletas extras ou sugestões de craques históricos/atuais adequados para o banco na lista 'jogadores_reservas'.
5. RESTRIÇÃO ABSOLUTA DE DADOS: Não invente jogadores fictícios, personagens de videogame, atores, cantores ou atletas de outros esportes (como basquete ou vôlei). Utilize APENAS atletas reais do futebol profissional (ativos, aposentados ou lendas históricas).
6. TONALIDADE: Escreva as descrições de 'qualidades_do_time' e 'variabilidade_do_time' com entusiasmo, jargões profissionais de futebol moderno e autoridade tática, simulando uma preleção de vestiário de alto nível.
"""