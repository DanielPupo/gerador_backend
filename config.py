# config.py - Evolução EA FC Edition

TEAM_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "nome_do_time": {"type": "STRING", "description": "Nome do Squad (ex: Galácticos FC, Samba Boys)"},
        "formacao_tatica": {"type": "STRING", "description": "A formação ideal do meta do EA FC (ex: 4-3-3, 4-2-3-1, 3-5-2)"},
        "quimica_total": {"type": "INTEGER", "description": "Cálculo fictício de química do elenco de 0 a 33"},
        "estilo_de_jogo": {"type": "STRING", "description": "Mentalidade tática (ex: Tiki-Taka, Contra-Ataque Veloz, Pressão Constante)"},
        "jogadores": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "nome_completo": {"type": "STRING", "description": "Nome (Clube) ex: Erling Haaland (Manchester City)"},
                    "posicao_campo": {"type": "STRING", "description": "Sigla da posição no EA FC (ex: GK, CB, LB, CM, CAM, RW, ST)"},
                    "playstyle_plus": {"type": "STRING", "description": "A habilidade assinatura do jogador (ex: Finesse Shot+, Power Shot+, Whipped Pass+)"}
                },
                "required": ["nome_completo", "posicao_campo", "playstyle_plus"]
            },
            "description": "Lista com exatamente 11 jogadores titulares na ordem da formação escolhida."
        },
        "jogadores_reservas": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Lista de até 7 suplentes com o formato Nome (Clube)"
        },
        "instrucoes_de_jogador": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Instruções individuais cruciais (ex: 'Laterais: Ficar na defesa', 'Atacante: Chegar por trás')"
        }
    },
    "required": ["nome_do_time", "formacao_tatica", "quimica_total", "estilo_de_jogo", "jogadores", "jogadores_reservas", "instrucoes_de_jogador"]
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