# story.py
# Estrutura completa da história em quadrinhos

HISTORY = {
    # ==========================================
    # TELA INICIAL
    # ==========================================
    "inicio": {
        "tipo": "inicio",
        "imagem": "assets/imagens/capa.png",
        "titulo": "A Garrafa do Futuro",
        "descricao": "Uma história sobre escolhas e o destino do planeta"
    },
    
    # ==========================================
    # PÁGINAS LINEARES (1 a 5)
    # ==========================================
    "pagina_01": {
        "tipo": "cena",
        "imagem": "assets/imagens/pagina_01.png",
        "proxima": "pagina_02"
    },
    
    "pagina_02": {
        "tipo": "cena",
        "imagem": "assets/imagens/pagina_02.png",
        "proxima": "pagina_03"
    },
    
    "pagina_03": {
        "tipo": "cena",
        "imagem": "assets/imagens/pagina_03.png",
        "proxima": "pagina_04"
    },
    
    "pagina_04": {
        "tipo": "cena",
        "imagem": "assets/imagens/pagina_04.png",
        "proxima": "pagina_05"
    },
    
    "pagina_05": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_05.png",
        "proxima": "decisao_01"
    },
    
    # ==========================================
    # DECISÃO 1
    # ==========================================
    "decisao_01": {
        "tipo": "escolha",
        "imagem": "assets/images/decisao_01.png",
        "pergunta": "O que Aline deve fazer com a garrafa?",
        "opcoes": {
            "Encaminhar para a coleta seletiva": "pagina_06a",
            "Descartar no lixo comum": "pagina_06b"
        }
    },
    
    # ==========================================
    # CAMINHO B (ERRADO) - Descartar no lixo comum
    # ==========================================
    "pagina_06b": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_06b.png",
        "proxima": "pagina_07b"
    },
    
    "pagina_07b": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_07b.png",
        "proxima": "feedback_01b"
    },
    
    "feedback_01b": {
        "tipo": "final",
        "imagem": "assets/images/feedback_01b.png",
        "mensagem": "O PET não desaparece facilmente na natureza; ele se fragmenta em microplásticos que contaminam o solo e a água. Tente novamente!"
    },
    
    # ==========================================
    # CAMINHO A (CERTO) - Coleta seletiva
    # ==========================================
    "pagina_06a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_06a.png",
        "proxima": "pagina_07a"
    },
    
    "pagina_07a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_07a.png",
        "proxima": "pagina_08a"
    },
    
    "pagina_08a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_08a.png",
        "proxima": "decisao_02"
    },
    
    # ==========================================
    # DECISÃO 2
    # ==========================================
    "decisao_02": {
        "tipo": "escolha",
        "imagem": "assets/images/decisao_02.png",
        "pergunta": "Qual é a melhor destinação para a garrafa?",
        "opcoes": {
            "Reutilizar (vaso ou porta-lápis)": "pagina_09a",
            "Encaminhar para reciclagem": "pagina_09b"
        }
    },
    
    # ==========================================
    # CAMINHO A - Reutilizar (parcialmente incorreto)
    # ==========================================
    "pagina_09a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_09a.png",
        "proxima": "pagina_10a"
    },
    
    "pagina_10a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_10a.png",
        "proxima": "feedback_02a"
    },
    
    "feedback_02a": {
        "tipo": "final",
        "imagem": "assets/images/feedback_02a.png",
        "mensagem": "Transformar a garrafa em um porta-lápis adia o descarte, mas não resolve o problema final. Tente novamente!"
    },
    
    # ==========================================
    # CAMINHO B - Reciclagem (correto)
    # ==========================================
    "pagina_09b": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_09b.png",
        "proxima": "pagina_10b"
    },
    
    "pagina_10b": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_10b.png",
        "proxima": "decisao_03"
    },
    
    # ==========================================
    # DECISÃO 3
    # ==========================================
    "decisao_03": {
        "tipo": "escolha",
        "imagem": "assets/images/decisao_03.png",
        "pergunta": "Qual projeto seria mais eficaz na escola?",
        "opcoes": {
            "Ampliar ecopontos da escola": "pagina_11a",
            "Substituir garrafas PET por reutilizáveis": "pagina_11b"
        }
    },
    
    # ==========================================
    # CAMINHO A - Apenas reciclar (incompleto)
    # ==========================================
    "pagina_11a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_11a.png",
        "proxima": "pagina_12a"
    },
    
    "pagina_12a": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_12a.png",
        "proxima": "feedback_03a"
    },
    
    "feedback_03a": {
        "tipo": "final",
        "imagem": "assets/images/feedback_03a.png",
        "mensagem": "Reciclar não reduz a produção contínua de novos plásticos. É necessário reduzir o consumo na fonte. Tente novamente!"
    },
    
    # ==========================================
    # CAMINHO B - Redução na fonte (VITÓRIA!)
    # ==========================================
    "pagina_11b": {
        "tipo": "cena",
        "imagem": "assets/images/pagina_11b.png",
        "proxima": "pagina_12b"
    },
    
    "pagina_12b": {
        "tipo": "final",
        "imagem": "assets/images/pagina_12b.png",
        "mensagem": "🎉 Parabéns! Vocês entenderam o espírito da coisa! O futuro se tornou um lugar melhor. A preservação do meio ambiente é um compromisso diário!"
    }
}

# Função para obter uma cena
def get_cena(cena_id):
    return HISTORY.get(cena_id)

# Função para verificar se existe
def cena_existe(cena_id):
    return cena_id in HISTORY