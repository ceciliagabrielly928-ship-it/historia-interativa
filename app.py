import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from story import HISTORY, get_cena

# ==========================================
# CONFIGURAÇÃO
# ==========================================
st.set_page_config(
    page_title="A Garrafa do Futuro",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================
# IMAGENS
# ==========================================
def caminho_imagem(caminho):
    if not caminho:
        return None
    caminho = str(caminho).replace("\\", "/")
    candidatos = [
        Path(caminho),
        Path(__file__).resolve().parent / caminho.lstrip("/"),
    ]
    if "/assets/" in caminho:
        rel = "assets/" + caminho.split("/assets/", 1)[1]
        candidatos.append(Path(__file__).resolve().parent / rel)
    for arquivo in candidatos:
        try:
            if arquivo.is_file():
                return arquivo
        except OSError:
            pass
    return None


def imagem_data_uri(caminho):
    arquivo = caminho_imagem(caminho)
    if arquivo is None:
        return None
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(arquivo.suffix.lower(), "application/octet-stream")
    dados = base64.b64encode(arquivo.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{dados}"


def renderizar_imagem(caminho, alt="Imagem da história"):
    uri = imagem_data_uri(caminho)
    if uri is None:
        st.error(f"Imagem não encontrada: {caminho}")
        return False
    st.markdown(
        f"""
        <div class="imagem-container">
            <img src="{uri}" alt="{alt}">
        </div>
    """,
        unsafe_allow_html=True,
    )
    return True


# ==========================================
# CSS GLOBAL
# ==========================================
def aplicar_css():
    st.markdown(
        """
        <style>
        .stApp { background: #ffffff !important; }
        .main > div { padding: 0 !important; max-width: 100% !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; padding-top: 0 !important; }
        .stApp > div:first-child { margin-top: 0 !important; }
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        header {display: none !important;}
        .stDeployButton {display: none !important;}
        
        .main-container {
            background: #ffffff;
            min-height: 0vh;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: 18px 18px 40px 18px;
        }
        
        .titulo {
            font-size: 3.5rem;
            font-weight: 900;
            color: #222222;
            font-family: Georgia, serif;
            text-align: center;
            margin-bottom: 5px;
        }
        
        .subtitulo {
            font-size: 0.9rem;
            color: #666;
            text-align: center;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 20px;
        }
        
        .linha {
            width: 60px;
            height: 2px;
            background: #d4a843;
            margin: 10px auto 25px auto;
        }
        
        .imagem-container {
            width: min(1000px, 100%);
            margin: 0 auto 22px auto;
            background: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 8px 28px rgba(0,0,0,0.10);
        }
        
        .imagem-container img {
            width: 100%;
            max-height: 85vh;
            height: auto;
            object-fit: contain;
            display: block;
            margin: 0 auto;
        }
        
        .stButton button {
            width: 100% !important;
            padding: 16px 40px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 4px !important;
            border-radius: 4px !important;
            border: 2px solid #d4a843 !important;
            background: transparent !important;
            color: #d4a843 !important;
            transition: all 0.3s ease !important;
            font-family: Arial, sans-serif !important;
        }
        
        .stButton button:hover {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            box-shadow: 0 10px 40px rgba(212,168,67,0.3) !important;
        }
        
        .btn-comecar button {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            border: none !important;
        }
        
        .btn-comecar button:hover {
            background: #e8c86a !important;
            transform: scale(1.02) !important;
        }
        
        .pergunta {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 300;
            text-align: center;
            margin: 30px 0 20px 0;
            font-family: Georgia, serif;
        }
        
        .mensagem {
            color: #d4a843;
            font-size: 1.3rem;
            text-align: center;
            margin: 30px 0;
            font-family: Georgia, serif;
        }
        
        @media (max-width: 768px) {
            .main-container { padding: 10px 10px 30px 10px; }
            .titulo { font-size: 2.2rem; }
            .imagem-container { border-radius: 16px; margin-bottom: 16px; }
            .imagem-container img { max-height: 70vh; }
            .stButton button { font-size: 0.8rem !important; padding: 14px 20px !important; }
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


# ==========================================
# DADOS DO QUIZ
# ==========================================
PERGUNTAS_QUIZ = [
    {
        "pergunta": "Karla mostra a garrafa de PET encontrada pelos amigos e pergunta: qual decisão ajuda a dar um destino correto ao material e evita que ele permaneça no ambiente causando impactos?",
        "alternativas": {
            "A": "Juntá-la com outros resíduos sem separar os materiais",
            "B": "Colocá-la no lixo comum junto aos demais resíduos",
            "C": "Deixá-la em um terreno vazio até encontrar uma nova utilidade",
            "D": "Levá-la a um ponto de coleta ou encaminhá-la para reciclagem",
        },
        "correta": "D",
    },
    {
        "pergunta": "Depois de descobrirem o que significa PET, os amigos precisam escolher uma atitude para diminuir o problema antes que novas garrafas sejam produzidas. Qual decisão atende melhor a esse objetivo?",
        "alternativas": {
            "A": "Aumentar os pontos de coleta para receber mais garrafas descartáveis",
            "B": "Guardar as garrafas usadas para evitar que sejam encontradas no ambiente",
            "C": "Substituir garrafas descartáveis por recipientes que possam ser usados novamente",
            "D": "Separar as garrafas usadas e enviá-las para uma cooperativa",
        },
        "correta": "C",
    },
]


# ==========================================
# ESTADO E NAVEGAÇÃO
# ==========================================
def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"
    if "quiz_pontuacao" not in st.session_state:
        st.session_state.quiz_pontuacao = 0
    if "quiz_respondeu" not in st.session_state:
        st.session_state.quiz_respondeu = False
    if "quiz_resposta_dada" not in st.session_state:
        st.session_state.quiz_resposta_dada = None


def ir_para_cena(nome_cena):
    st.session_state.cena_atual = nome_cena
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.rerun()


def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.session_state.quiz_pontuacao = 0
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.rerun()


# ==========================================
# RENDERIZAR QUIZ
# ==========================================
def renderizar_quiz(numero_pergunta):
    pergunta = PERGUNTAS_QUIZ[numero_pergunta]

    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.meu-quiz-container) {
            background-color: white;
            border-radius: 24px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.09);
            border: 1px solid #e9e2d6;
            padding: 38px 45px 42px;
            margin: 0 auto;
        }

        .quiz-header-container { text-align: center; margin-bottom: 25px; }
        .quiz-titulo-principal {
            color: #1a1a1a;
            font-family: Arial, sans-serif;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .quiz-linha-sub {
            width: 45px;
            height: 3px;
            background: #d4a843;
            margin: 0 auto;
            border-radius: 2px;
        }

        .subcard-pergunta {
            background-color: #fbf8f3;
            border: 1px solid #f2e9dc;
            border-radius: 14px;
            padding: 22px 25px;
            margin-bottom: 25px;
        }
        .quiz-pergunta-texto {
            color: #2a2a2a;
            font-family: Arial, sans-serif;
            font-size: 15px;
            line-height: 1.6;
            text-align: left;
        }

        div[data-testid="stButton"] { margin-bottom: 10px !important; }
        div[data-testid="stButton"] > button {
            width: 100% !important;
            min-height: 48px !important;
            border-radius: 0px !important;
            border: 1.5px solid #cb9b39 !important;
            background: #ffffff !important;
            color: #222222 !important;
            font-family: Arial, sans-serif !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            text-align: center !important;
            padding: 12px 20px !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stButton"] > button:hover {
            background: #fffdf9 !important;
            border-color: #b08328 !important;
        }

        .box-resposta {
            padding: 14px 20px;
            margin-bottom: 10px;
            border-radius: 0px;
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: 600;
            text-align: center;
        }
        .box-correta { background-color: #edf7ed; border: 1.5px solid #75ad75; color: #1e5e23; }
        .box-errada { background-color: #fdf2f2; border: 1.5px solid #e58b8b; color: #8c2424; }
        .box-neutra { background-color: #ffffff; border: 1.5px solid #cb9b39; color: #555555; }

        .area-feedback { margin-top: 25px; margin-bottom: 15px; }
        .quiz-feedback {
            padding: 16px;
            border-radius: 0px;
            text-align: center;
            font-family: Arial, sans-serif;
            font-size: 15px;
            font-weight: bold;
        }

        .area-recomecar { margin-top: 15px; }
        .area-recomecar div[data-testid="stButton"] > button {
            border-radius: 0px !important;
            border: 1.5px solid #cb9b39 !important;
            background: #ffffff !important;
            color: #cb9b39 !important;
            font-size: 13px !important;
            letter-spacing: 2px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
        }
        .area-recomecar div[data-testid="stButton"] > button:hover {
            background: #fffdf9 !important;
            border-color: #b08328 !important;
            color: #b08328 !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 8, 1])

    with col2:
        with st.container(border=True):
            st.markdown(
                '<div class="meu-quiz-container"></div>', unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="quiz-header-container">
                    <div class="quiz-titulo-principal">DESAFIO</div>
                    <div class="quiz-linha-sub"></div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="subcard-pergunta">
                    <div class="quiz-pergunta-texto">{pergunta["pergunta"]}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            for letra, texto in pergunta["alternativas"].items():
                if not st.session_state.quiz_respondeu:
                    if st.button(
                        f"{letra}) {texto}",
                        key=f"quiz_{numero_pergunta}_{letra}",
                        use_container_width=True,
                    ):
                        st.session_state.quiz_respondeu = True
                        st.session_state.quiz_resposta_dada = letra
                        if letra == pergunta["correta"]:
                            st.session_state.quiz_pontuacao += 1
                        st.rerun()
                else:
                    resposta_dada = st.session_state.quiz_resposta_dada
                    correta = pergunta["correta"]

                    if letra == correta:
                        st.markdown(
                            f'<div class="box-resposta box-correta">✓ &nbsp; <strong>{letra})</strong> {texto}</div>',
                            unsafe_allow_html=True,
                        )
                    elif letra == resposta_dada:
                        st.markdown(
                            f'<div class="box-resposta box-errada">✕ &nbsp; <strong>{letra})</strong> {texto}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div class="box-resposta box-neutra"><strong>{letra})</strong> {texto}</div>',
                            unsafe_allow_html=True,
                        )

        if st.session_state.quiz_respondeu:
            resposta_dada = st.session_state.quiz_resposta_dada
            correta = pergunta["correta"]

            st.markdown('<div class="area-feedback">', unsafe_allow_html=True)
            if resposta_dada == correta:
                st.markdown(
                    '<div class="quiz-feedback box-correta">Resposta correta! 🎉</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="quiz-feedback box-errada">Resposta incorreta. A certa é a <strong>{correta}</strong>.</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Botão de Avançar após responder
            proxima_cena = (
                "pagina_02" if numero_pergunta == 0 else "pagina_final"
            )
            if st.button("AVANÇAR ▶", key=f"avancar_quiz_{numero_pergunta}"):
                ir_para_cena(proxima_cena)

            st.markdown('<div class="area-recomecar">', unsafe_allow_html=True)
            if st.button(
                "↺ RECOMEÇAR HISTÓRIA", key=f"reiniciar_{numero_pergunta}"
            ):
                reiniciar_historia()
            st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# DESAFIO: DECODIFICAR PLÁSTICOS (7 números)
# ==========================================
def renderizar_desafio_plasticos():
    html_desafio = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: Arial, sans-serif; background: #f5f1e8; color: #222; padding: 20px; min-height: 100vh; }
        .container { width: 100%; max-width: 950px; margin: 0 auto; background: white; border-radius: 20px; padding: 35px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); }
        h1 { text-align: center; font-size: 28px; margin-bottom: 25px; color: #222; }
        .karla { background: #f0f0f0; border-radius: 12px; padding: 18px; margin-bottom: 25px; font-size: 16px; line-height: 1.5; color: #222; }
        .karla strong { display: block; margin-bottom: 5px; }
        h2 { font-size: 18px; margin-top: 25px; margin-bottom: 12px; color: #222; }
        .banco { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 30px; }
        .palavra { background: #eeeeee; border-radius: 8px; padding: 9px 13px; font-weight: bold; font-size: 14px; color: #222; }
        .numeros { display: flex; justify-content: space-between; gap: 10px; margin: 30px 0; }
        .numero { flex: 1; min-height: 70px; border: none; border-bottom: 3px solid #222; background: transparent; font-size: 30px; font-weight: bold; cursor: pointer; transition: 0.2s; color: #222; }
        .numero:hover { background: #f0f0f0; }
        .numero.selecionado { background: #e6e6e6; }
        .numero.concluido { border-bottom: 4px solid #333; background: #dcdcdc; }
        .desafio { display: none; margin-top: 20px; padding: 25px; border-radius: 15px; background: #f7f7f7; }
        .desafio.ativo { display: block; }
        .pista-titulo { font-weight: bold; font-size: 19px; margin-bottom: 10px; color: #222; }
        .pista { font-size: 17px; line-height: 1.5; margin-bottom: 20px; color: #333; }
        .opcoes { display: flex; flex-wrap: wrap; gap: 10px; }
        .opcao { border: 2px solid #333; background: white; border-radius: 9px; padding: 11px 16px; cursor: pointer; font-weight: bold; transition: 0.2s; font-size: 14px; color: #222; }
        .opcao:hover { background: #eeeeee; }
        .opcao:disabled { cursor: default; }
        .feedback { margin-top: 18px; font-weight: bold; font-size: 17px; min-height: 25px; }
        .final { display: none; margin-top: 25px; padding: 22px; background: #eeeeee; border-radius: 12px; text-align: center; font-size: 20px; font-weight: bold; color: #222; }
    </style>
    </head>
    <body>
    <div class="container">
        <h1>DESAFIO — DECODIFIQUE OS PLÁSTICOS</h1>
        <div class="karla">
            <strong>KARLA:</strong>
            "Esses números não estão aqui por acaso. Cada um representa um tipo de plástico. Use as pistas para descobrir qual é qual!"
        </div>
        <h2>BANCO DE PALAVRAS</h2>
        <div class="banco">
            <span class="palavra">PP</span>
            <span class="palavra">PET</span>
            <span class="palavra">PVC</span>
            <span class="palavra">PS</span>
            <span class="palavra">LDPE</span>
            <span class="palavra">OTHER</span>
            <span class="palavra">HDPE</span>
        </div>
        <h2>IDENTIFIQUE CADA PLÁSTICO</h2>
        <div class="numeros">
            <button class="numero" onclick="abrirDesafio(1)">①</button>
            <button class="numero" onclick="abrirDesafio(2)">②</button>
            <button class="numero" onclick="abrirDesafio(3)">③</button>
            <button class="numero" onclick="abrirDesafio(4)">④</button>
            <button class="numero" onclick="abrirDesafio(5)">⑤</button>
            <button class="numero" onclick="abrirDesafio(6)">⑥</button>
            <button class="numero" onclick="abrirDesafio(7)">⑦</button>
        </div>
        <div id="desafio" class="desafio">
            <div class="pista-titulo" id="pistaTitulo"></div>
            <div class="pista" id="pista"></div>
            <div class="opcoes" id="opcoes"></div>
            <div class="feedback" id="feedback"></div>
        </div>
        <div id="final" class="final">
            Parabéns! Você decodificou todos os tipos de plástico!
        </div>
    </div>
    <script>
    const desafios = {
        1: { pista: "Sou transparente, leve e muito usado em garrafas de água e refrigerante. Minha sigla tem três letras.", resposta: "PET" },
        2: { pista: "Sou conhecido por ser resistente e apareço bastante em embalagens de produtos de limpeza, frascos e recipientes.", resposta: "HDPE" },
        3: { pista: "Posso aparecer em canos, tubos e alguns tipos de embalagens. Meu nome é formado por três letras.", resposta: "PVC" },
        4: { pista: "Sou mais flexível e apareço bastante em sacolas plásticas, filmes e embalagens.", resposta: "LDPE" },
        5: { pista: "Posso ser encontrado em potes, tampas e embalagens de alimentos. Sou conhecido por resistir bem ao calor.", resposta: "PP" },
        6: { pista: "Sou usado em alguns copos descartáveis, bandejas e embalagens. Meu nome começa com 'poliestireno'.", resposta: "PS" },
        7: { pista: "Não sou um único tipo de plástico. Essa categoria reúne outros plásticos que não se encaixam nos seis anteriores.", resposta: "OTHER" }
    };
    const palavras = ["PP", "PET", "PVC", "PS", "LDPE", "OTHER", "HDPE"];
    let numeroAtual = null;
    let resolvidos = [];
    
    function abrirDesafio(numero) {
        numeroAtual = numero;
        const d = desafios[numero];
        document.getElementById("desafio").classList.add("ativo");
        document.getElementById("pistaTitulo").textContent = "PISTA " + numero;
        document.getElementById("pista").textContent = '"' + d.pista + '"';
        document.getElementById("feedback").textContent = "";
        criarOpcoes();
        document.querySelectorAll(".numero").forEach((b, i) => {
            b.classList.remove("selecionado");
            if (i + 1 === numero) b.classList.add("selecionado");
        });
    }
    
    function criarOpcoes() {
        const area = document.getElementById("opcoes");
        area.innerHTML = "";
        palavras.forEach(p => {
            const b = document.createElement("button");
            b.className = "opcao";
            b.textContent = p;
            b.onclick = () => verificarResposta(p);
            area.appendChild(b);
        });
    }
    
    function verificarResposta(resposta) {
        const correta = desafios[numeroAtual].resposta;
        const fb = document.getElementById("feedback");
        if (resposta === correta) {
            fb.textContent = "✓ Acertou!";
            fb.style.color = "#247a3d";
            if (!resolvidos.includes(numeroAtual)) resolvidos.push(numeroAtual);
            document.querySelectorAll(".numero")[numeroAtual - 1].classList.add("concluido");
            document.querySelectorAll(".opcao").forEach(b => b.disabled = true);
            if (resolvidos.length === 7) {
                setTimeout(() => {
                    document.getElementById("final").style.display = "block";
                    document.getElementById("desafio").classList.remove("ativo");
                }, 600);
            }
        } else {
            fb.textContent = "✗ Tente novamente!";
            fb.style.color = "#b3261e";
        }
    }
    </script>
    </body>
    </html>
    """
    components.html(html_desafio, height=900, scrolling=True)


# =========================================================
# DESAFIO — POLÍMERO
# =========================================================
def renderizar_desafio_polimero():
    html_polimero = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { min-height: 100vh; font-family: Arial, sans-serif; background: white; padding: 28px 20px 35px; }
            .container { width: 100%; max-width: 900px; margin: 0 auto; background: white; border-radius: 24px; padding: 38px 45px 42px; border: 1px solid #e9e2d6; box-shadow: 0 12px 35px rgba(0, 0, 0, 0.09); }
            h1 { text-align: center; font-size: 27px; font-weight: 800; letter-spacing: .5px; color: #222; margin-bottom: 13px; }
            h1::after { content: ""; display: block; width: 55px; height: 3px; background: #d4a843; margin: 13px auto 28px; border-radius: 5px; }
            .karla { background: #faf7f0; border-left: 4px solid #d4a843; border-radius: 12px; padding: 18px 22px; margin-bottom: 30px; font-size: 16px; line-height: 1.6; color: #333; }
            .desafio { padding: 27px 30px; border-radius: 17px; background: #faf8f4; border: 1px solid #e8e1d5; text-align: center; }
            .pergunta { font-size: 19px; line-height: 1.7; color: #333; margin-bottom: 20px; }
            input { width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 10px; font-size: 16px; outline: none; background: white; margin-bottom: 15px; }
            button { border: none; padding: 14px; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 15px; transition: .2s; background: #d4a843; color: white; width: 100%; }
            button:hover { background: #bd922f; }
            #resultado { margin-top: 18px; font-size: 17px; font-weight: bold; }
            .acerto { color: #247a3d; }
            .erro { color: #b3261e; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DESAFIO — A ESTRUTURA DOS PLÁSTICOS</h1>
            <div class="karla">
                <strong>KARLA:</strong>
                "Para entender os plásticos, precisamos saber como eles são formados!"
            </div>
            <div class="desafio">
                <div class="pergunta">Qual é o termo químico para a grande molécula formada por várias partes menores unidas?</div>
                <input type="text" id="respostaInput" placeholder="Digite sua resposta aqui...">
                <button onclick="verificar()">RESPONDER</button>
                <div id="resultado"></div>
            </div>
        </div>
        <script>
            function verificar() {
                const resp = document.getElementById("respostaInput").value.trim().toLowerCase();
                const resDiv = document.getElementById("resultado");
                if (resp === "polímero" || resp === "polimero") {
                    resDiv.className = "acerto";
                    resDiv.textContent = "✓ Excelente! Plásticos são polímeros!";
                } else {
                    resDiv.className = "erro";
                    resDiv.textContent = "✕ Tente novamente!";
                }
            }
        </script>
    </body>
    </html>
    """
    components.html(html_polimero, height=600, scrolling=True)


# ==========================================
# EXECUÇÃO E RENDERIZADOR PRINCIPAL
# ==========================================
def main():
    aplicar_css()
    inicializar_estado()

    # Busca a cena atual através da função do story.py ou do estado
    chave_cena = st.session_state.cena_atual
    cena = get_cena(chave_cena) if "get_cena" in globals() else HISTORY.get(chave_cena)

    if not cena:
        st.error(f"A cena '{chave_cena}' não foi encontrada.")
        if st.button("Voltar ao Início"):
            reiniciar_historia()
        return

    # Renderiza o conteúdo conforme o tipo da cena
    tipo = cena.get("tipo", "cena")

    if tipo == "inicio":
        renderizar_imagem(cena.get("imagem"), "Capa da história")
        st.markdown(
            f"""
            <h1 class="titulo">{cena.get("titulo", "A Garrafa do Futuro")}</h1>
            <div class="linha"></div>
            <p class="subtitulo">{cena.get("descricao", "")}</p>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="btn-comecar">', unsafe_allow_html=True)
            if st.button(
                "▶ COMEÇAR", key="comecar", use_container_width=True
            ):
                ir_para_cena("pagina_01")
            st.markdown("</div>", unsafe_allow_html=True)

    elif tipo == "cena":
        if "imagem" in cena:
            renderizar_imagem(cena["imagem"])
        if "texto" in cena:
            st.write(cena["texto"])

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if "proxima" in cena and cena["proxima"]:
                if st.button(
                    "AVANÇAR ▶", key=f"btn_{chave_cena}", use_container_width=True
                ):
                    ir_para_cena(cena["proxima"])

    elif tipo == "quiz":
        renderizar_quiz(cena.get("numero_pergunta", 0))

    elif tipo == "desafio_plasticos":
        renderizar_desafio_plasticos()

    elif tipo == "desafio_polimero":
        renderizar_desafio_polimero()


if __name__ == "__main__":
    main()