import streamlit as st
import streamlit.components.v1 as components

# Tenta importar as funções do arquivo de história
try:
    from story import get_cena, HISTORIA
except ImportError:
    # Estrutura de fallback caso o story.py não esteja no mesmo diretório
    def get_cena(cena_id):
        return HISTORIA.get(cena_id, None)

    HISTORIA = {
        "inicio": {
            "texto": "Bem-vindo à jornada sobre reciclagem e polímeros!",
            "opcoes": [{"texto": "Iniciar Desafio", "proxima_cena": "quiz_1"}]
        },
        "quiz_1": {
            "tipo": "quiz",
            "quiz_index": 0,
            "opcoes": []
        }
    }


# =========================================================
# CONFIGURAÇÃO DE PÁGINA E CSS
# =========================================================

st.set_page_config(
    page_title="A Garrafa do Futuro",
    page_icon="🍾",
    layout="centered"
)

def aplicar_css():
    st.markdown(
        """
        <style>
            /* Configuração Geral */
            body {
                background-color: #f5f1e8;
                color: #222222;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            .main-container {
                text-align: center;
                padding: 20px 0;
            }

            /* Estilo dos Títulos e Capa */
            .titulo-capa {
                font-size: 32px;
                font-weight: 900;
                color: #2c3e50;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: 5px;
            }

            .subtitulo-capa {
                font-size: 16px;
                color: #7f8c8d;
                font-weight: 600;
                letter-spacing: 1px;
                margin-bottom: 25px;
            }

            /* Estilo do Header de Desafio (Quiz) */
            .quiz-header {
                text-align: center;
                margin: 25px 0 15px 0;
            }

            .quiz-titulo-destaque {
                font-size: 26px;
                font-weight: 800;
                color: #d4a843;
                text-transform: uppercase;
                letter-spacing: 2px;
                display: inline-block;
            }

            /* Caixas de Diálogo e Texto */
            .texto-cena {
                font-size: 18px;
                line-height: 1.6;
                color: #333333;
                background: #ffffff;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                margin-bottom: 20px;
            }

            .personagem {
                font-weight: bold;
                color: #d4a843;
                font-size: 16px;
                margin-top: 10px;
            }

            .dialogo {
                font-style: italic;
                background: #faf8f4;
                border-left: 4px solid #d4a843;
                padding: 12px 16px;
                border-radius: 0 8px 8px 0;
                margin-bottom: 15px;
            }

            .pergunta {
                font-size: 18px;
                font-weight: 600;
                text-align: center;
                margin: 20px 0 15px 0;
                color: #2c3e50;
            }

            .mensagem {
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: #2e7d32;
                margin: 30px 0;
            }

            /* Personalização dos Botões */
            div.stButton > button {
                width: 100%;
                border-radius: 8px;
                border: 2px solid #d4a843;
                background-color: #ffffff;
                color: #d4a843;
                font-weight: bold;
                padding: 12px 16px;
                transition: all 0.3s ease;
            }

            div.stButton > button:hover {
                background-color: #d4a843;
                color: #ffffff;
                border-color: #d4a843;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# GERENCIAMENTO DE ESTADO E NAVEGAÇÃO
# =========================================================

def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"
    if "respostas_quiz" not in st.session_state:
        st.session_state.respostas_quiz = {}

def ir_para_cena(proxima_cena):
    st.session_state.cena_atual = proxima_cena
    st.rerun()

def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.session_state.respostas_quiz = {}
    st.rerun()


# =========================================================
# COMPONENTES E INTERFACES VISUAIS
# =========================================================

def renderizar_imagem(caminho_imagem, alt="Imagem"):
    try:
        st.image(caminho_imagem, use_container_width=True, caption=alt)
    except Exception:
        pass

def renderizar_quiz(num_pergunta):
    # Renderiza apenas a palavra DESAFIO em destaque, negrito e centralizada
    st.markdown(
        """
        <div class="quiz-header">
            <div class="quiz-titulo-destaque">DESAFIO</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Exemplo de Pergunta Integrada
    st.markdown(
        """
        <div class="texto-cena">
            Karla mostra a garrafa de PET encontrada pelos amigos e pergunta: 
            qual decisão ajuda a dar um destino correto ao material e evita que ele permaneça no ambiente causando impactos?
        </div>
        """,
        unsafe_allow_html=True
    )

    opcoes = [
        "A) Juntá-la com outros resíduos sem separar os materiais",
        "B) Colocá-la no lixo comum junto aos demais resíduos",
        "C) Deixá-la em um terreno vazio até encontrar uma nova utilidade",
        "D) Levá-la a um ponto de coleta ou encaminhá-la para reciclagem"
    ]

    for idx, opt in enumerate(opcoes):
        if st.button(opt, key=f"quiz_opt_{num_pergunta}_{idx}"):
            if idx == 3:  # Alternativa D correta
                st.success("Resposta Correta!")
                ir_para_cena("desafio_polimero")
            else:
                st.error("Tente novamente!")

def renderizar_desafio_plasticos():
    st.markdown(
        """
        <div class="quiz-header">
            <div class="quiz-titulo-destaque">DESAFIO DE SEPARAÇÃO</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.info("Classifique os plásticos de acordo com seus símbolos de reciclagem.")


def renderizar_desafio_polimero():
    html_polimero = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Arial, sans-serif; background: #f5f1e8; color: #222; padding: 20px; }
            .container { width: 100%; max-width: 950px; margin: 0 auto; background: white; border-radius: 20px; padding: 35px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); }
            h1 { text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #d4a843; text-transform: uppercase; letter-spacing: 1.5px; }
            .karla { background: #faf8f4; border-left: 4px solid #d4a843; border-radius: 8px; padding: 18px; margin-bottom: 25px; font-size: 16px; line-height: 1.6; color: #333; }
            .karla strong { color: #d4a843; display: block; margin-bottom: 5px; }
            .area-montagem { background: #f9f9f9; border: 2px dashed #d4a843; border-radius: 12px; padding: 25px; min-height: 120px; display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 25px; }
            .elo { background: #d4a843; color: white; padding: 10px 18px; border-radius: 20px; font-weight: bold; font-size: 14px; display: flex; align-items: center; gap: 8px; animation: pop 0.3s ease; }
            .elo-ligacao { color: #888; font-weight: bold; font-size: 18px; }
            .banco-monomeros { display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 25px; }
            .btn-monomero { background: white; border: 2px solid #d4a843; color: #d4a843; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; transition: all 0.2s ease; }
            .btn-monomero:hover { background: #d4a843; color: white; }
            .botoes-controle { display: flex; justify-content: center; gap: 15px; }
            .btn-acao { padding: 10px 20px; border-radius: 6px; border: none; font-weight: bold; cursor: pointer; font-size: 14px; }
            .btn-limpar { background: #e53935; color: white; }
            .feedback { margin-top: 20px; text-align: center; font-weight: bold; font-size: 18px; min-height: 30px; }
            @keyframes pop { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DESAFIO</h1>

            <div class="karla">
                <strong>KARLA:</strong>
                "Um polímero é como um colar de contas! Cada pequena unidade é um <b>monômero</b>. Ligue 4 unidades de monômeros para formar a cadeia do polímero de PET!"
            </div>

            <div class="area-montagem" id="cadeia">
                <span style="color:#aaa;" id="placeholder">Clique nos monômeros abaixo para iniciar a cadeia...</span>
            </div>

            <div class="banco-monomeros">
                <button class="btn-monomero" onclick="adicionarMonomero('Ácido Tereftálico')">+ Monômero A (Ácido Tereftálico)</button>
                <button class="btn-monomero" onclick="adicionarMonomero('Etilenoglicol')">+ Monômero B (Etilenoglicol)</button>
            </div>

            <div class="botoes-controle">
                <button class="btn-acao btn-limpar" onclick="limparCadeia()">Reiniciar Cadeia</button>
            </div>

            <div class="feedback" id="feedback"></div>
        </div>

        <script>
            let cadeia = [];

            function adicionarMonomero(nome) {
                if (cadeia.length >= 4) return;

                cadeia.push(nome);
                renderizarCadeia();

                if (cadeia.length === 4) {
                    const fb = document.getElementById("feedback");
                    fb.textContent = "✓ Excelente! Você sintetizou a cadeia do Polietileno Tereftalato (PET)!";
                    fb.style.color = "#2e7d32";
                }
            }

            function limparCadeia() {
                cadeia = [];
                renderizarCadeia();
                document.getElementById("feedback").textContent = "";
            }

            function renderizarCadeia() {
                const container = document.getElementById("cadeia");
                container.innerHTML = "";

                if (cadeia.length === 0) {
                    container.innerHTML = '<span style="color:#aaa;">Clique nos monômeros abaixo para iniciar a cadeia...</span>';
                    return;
                }

                cadeia.forEach((item, index) => {
                    const elo = document.createElement("div");
                    elo.className = "elo";
                    elo.textContent = item;
                    container.appendChild(elo);

                    if (index < cadeia.length - 1) {
                        const ligacao = document.createElement("span");
                        ligacao.className = "elo-ligacao";
                        ligacao.textContent = "—";
                        container.appendChild(ligacao);
                    }
                });
            }
        </script>
    </body>
    </html>
    """

    components.html(html_polimero, height=620, scrolling=True)


# =========================================================
# EXECUÇÃO DA CENA ATUAL
# =========================================================

def renderizar_cena_atual():
    cena_id = st.session_state.cena_atual
    cena = get_cena(cena_id)

    if not cena:
        # Se for uma tela de desafio direto
        if cena_id == "quiz_1":
            renderizar_quiz(1)
            return
        elif cena_id == "desafio_polimero":
            renderizar_desafio_polimero()
            return
        else:
            st.error(f"Cena '{cena_id}' não encontrada.")
            if st.button("Voltar ao Início"):
                reiniciar_historia()
            return

    # 1. Imagem
    if cena.get("imagem"):
        renderizar_imagem(cena["imagem"], alt=f"Cena: {cena_id}")

    # 2. Texto
    if cena.get("texto"):
        st.markdown(f'<div class="texto-cena">{cena["texto"]}</div>', unsafe_allow_html=True)

    # 3. Diálogos
    if cena.get("dialogos"):
        for d in cena["dialogos"]:
            st.markdown(
                f'''
                <div class="personagem">{d.get("personagem", "")}</div>
                <div class="dialogo">"{d.get("fala", "")}"</div>
                ''',
                unsafe_allow_html=True
            )

    # 4. Elementos Especiais
    tipo_cena = cena.get("tipo", "normal")
    if tipo_cena == "quiz":
        renderizar_quiz(cena.get("quiz_index", 0))
    elif tipo_cena == "desafio_plasticos":
        renderizar_desafio_plasticos()
    elif tipo_cena == "desafio_polimero":
        renderizar_desafio_polimero()

    # 5. Navegação
    opcoes = cena.get("opcoes", [])
    if opcoes:
        st.markdown('<div class="pergunta">O que fazer agora?</div>', unsafe_allow_html=True)
        cols = st.columns(len(opcoes))
        for idx, opcao in enumerate(opcoes):
            with cols[idx]:
                if st.button(opcao["texto"], key=f"btn_{cena_id}_{idx}"):
                    ir_para_cena(opcao["proxima_cena"])

    elif tipo_cena == "final":
        st.markdown('<div class="mensagem">FIM DA JORNADA!</div>', unsafe_allow_html=True)
        if st.button("↻ JOGAR NOVAMENTE", use_container_width=True):
            reiniciar_historia()


# =========================================================
# PONTO DE ENTRADA (MAIN)
# =========================================================

def main():
    aplicar_css()
    inicializar_estado()

    # Capa / Cabeçalho Principal (Com título e estilo limpo)
    st.markdown(
        """
        <div class="main-container">
            <div class="titulo-capa">DESAFIO</div>
            <div class="subtitulo-capa">A GARRAFA DO FUTURO</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    renderizar_cena_atual()


if __name__ == "__main__":
    main()