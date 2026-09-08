# story.py
# Dicionário que contém toda a estrutura da história

HISTORY = {
    "inicio": {
        "tipo": "inicio",
        "imagem": "assets/images/capa.png",
        "titulo": "A Jornada do Herói",
        "descricao": "Uma aventura épica em quadrinhos"
    },
    
    "cena_01": {
        "tipo": "cena",
        "imagem": "assets/images/cena_01.png",
        "proxima": "cena_02"
    },
    
    "cena_02": {
        "tipo": "cena",
        "imagem": "assets/images/cena_02.png",
        "proxima": "cena_03"
    },
    
    "cena_03": {
        "tipo": "cena",
        "imagem": "assets/images/cena_03.png",
        "proxima": "cena_04"
    },
    
    "cena_04": {
        "tipo": "cena",
        "imagem": "assets/images/cena_04.png",
        "proxima": "cena_05"
    },
    
    "cena_05": {
        "tipo": "escolha",
        "imagem": "assets/images/cena_05.png",
        "pergunta": "O que o herói deve fazer?",
        "opcoes": {
            "Seguir pela floresta": "cena_06a",
            "Voltar para a cidade": "cena_06b"
        }
    },
    
    "cena_06a": {
        "tipo": "cena",
        "imagem": "assets/images/cena_06a.png",
        "proxima": "final_a"
    },
    
    "cena_06b": {
        "tipo": "cena",
        "imagem": "assets/images/cena_06b.png",
        "proxima": "final_b"
    },
    
    "final_a": {
        "tipo": "final",
        "imagem": "assets/images/final_a.png",
        "mensagem": "Você seguiu pela floresta e encontrou o tesouro! "
    },
    
    "final_b": {
        "tipo": "final",
        "imagem": "assets/images/final_b.png",
        "mensagem": "Você voltou para a cidade e se tornou um herói respeitado! "
    }
}

# Função para obter uma cena específica
def get_cena(cena_id):
    return HISTORY.get(cena_id)

# Função para verificar se uma cena existe
def cena_existe(cena_id):
    return cena_id in HISTORY

# Função para obter todas as imagens da história (útil para verificação)
def get_todas_imagens():
    imagens = []
    for cena in HISTORY.values():
        if "imagem" in cena:
            imagens.append(cena["imagem"])
    return imagens