# app.py
import streamlit as st
import streamlit.components.v1 as components
from story import HISTORY, get_cena
from pathlib import Path
import base64

# ==========================================
# CONFIGURAÇÃO
# ==========================================
st.set_page_config(
    page_title="A Garrafa do Futuro",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# IMAGENS
# ==========================================
def caminho_imagem(caminho):
    if not caminho:
        return None
    caminho = str(caminho).replace('\\', '/')
    candidatos = [Path(caminho), Path(__file__).resolve().parent / caminho.lstrip('/')]
    if '/assets/' in caminho:
        rel = 'assets/' + caminho.split('/assets/', 1)[1]
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
    mime = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.gif':'image/gif'}.get(arquivo.suffix.lower(), 'application/octet-stream')
    dados = base64.b64encode(arquivo.read_bytes()).decode('ascii')
    return f'data:{mime};base64,{dados}'

def renderizar_imagem(caminho, alt='Imagem da história'):
    uri = imagem_data_uri(caminho)
    if uri is None:
        st.error(f'Imagem não encontrada: {caminho}')
        return False
    st.markdown(f'''
        <div class="imagem-container">
            <img src="{uri}" alt="{alt}">
        </div>
    ''', unsafe_allow_html=True)
    return True


# ==========================================
# CSS GLOBAL
# ==========================================
def aplicar_css():
    st.markdown("""
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
    """, unsafe_allow_html=True)


# ==========================================
# DADOS DO QUIZ (2 perguntas = 2 desafios)
# ==========================================

PERGUNTAS_QUIZ = [
    {
        "pergunta": "Karla mostra a garrafa de PET encontrada pelos amigos e pergunta: qual decisão ajuda a dar um destino correto ao material e evita que ele permaneça no ambiente causando impactos?",
        "alternativas": {
            "A": "Juntá-la com outros resíduos sem separar os materiais",
            "B": "Colocá-la no lixo comum junto aos demais resíduos",
            "C": "Deixá-la em um terreno vazio até encontrar uma nova utilidade",
            "D": "Levá-la a um ponto de coleta ou encaminhá-la para reciclagem"
        },
        "correta": "D"
    },
    {
        "pergunta": "Depois de descobrirem o que significa PET, os amigos precisam escolher uma atitude para diminuir o problema antes que novas garrafas sejam produzidas. Qual decisão atende melhor a esse objetivo?",
        "alternativas": {
            "A": "Aumentar os pontos de coleta para receber mais garrafas descartáveis",
            "B": "Guardar as garrafas usadas para evitar que sejam encontradas no ambiente",
            "C": "Substituir garrafas descartáveis por recipientes que possam ser usados novamente",
            "D": "Separar as garrafas usadas e enviá-las para uma cooperativa"
        },
        "correta": "C"
    }
]


# ==========================================
# ESTADO DO QUIZ
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

    if "quiz_finalizado" not in st.session_state:
        st.session_state.quiz_finalizado = False


def ir_para_cena(cena_id):

    st.session_state.cena_atual = cena_id
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.session_state.quiz_finalizado = False

    st.rerun()


def reiniciar_historia():

    st.session_state.cena_atual = "inicio"
    st.session_state.quiz_pontuacao = 0
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.session_state.quiz_finalizado = False

    st.rerun()


# ==========================================
# DESAFIO: QUIZ
# ==========================================

def renderizar_quiz(numero_pergunta):

    pergunta = PERGUNTAS_QUIZ[numero_pergunta]

    # ==========================================
    # CARTÃO DA PERGUNTA
    # ==========================================

    st.markdown(
        f"""
        <div style="
            width: 100%;
            max-width: 900px;
            margin: 10px auto 25px auto;
            padding: 32px 40px;
            background: white;
            border: 2px solid #d4a843;
            border-radius: 24px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            box-sizing: border-box;
        ">

            <div style="
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                color: #9a761f;
                font-family: Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
            ">

                <span style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 42px;
                    height: 42px;
                    margin-right: 12px;
                    border-radius: 50%;
                    background: #d4a843;
                    color: white;
                    font-size: 18px;
                    letter-spacing: 0;
                ">K</span>

                DESAFIO DE KARLA

            </div>

            <div style="
                color: #222222;
                font-family: Arial, sans-serif;
                font-size: 18px;
                line-height: 1.65;
                font-weight: 500;
            ">
                {pergunta["pergunta"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # ALTERNATIVAS
    # ==========================================

    if not st.session_state.quiz_respondeu:

        for letra, texto in pergunta["alternativas"].items():

            if st.button(
                f"{letra})  {texto}",
                key=f"alt_{numero_pergunta}_{letra}",
                use_container_width=True
            ):

                st.session_state.quiz_respondeu = True
                st.session_state.quiz_resposta_dada = letra

                if letra == pergunta["correta"]:
                    st.session_state.quiz_pontuacao += 1

                st.rerun()


    # ==========================================
    # RESULTADO
    # ==========================================

    else:

        resposta_dada = st.session_state.quiz_resposta_dada
        resposta_correta = pergunta["correta"]

        for letra, texto in pergunta["alternativas"].items():

            if letra == resposta_correta:

                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        max-width: 900px;
                        margin: 0 auto 10px auto;
                        padding: 15px 20px;
                        box-sizing: border-box;
                        border-radius: 14px;
                        background: #f3faf4;
                        border: 2px solid #78a982;
                        color: #315f38;
                        font-family: Arial, sans-serif;
                        font-size: 16px;
                    ">
                        <strong>{letra})</strong> {texto} ✅
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif letra == resposta_dada:

                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        max-width: 900px;
                        margin: 0 auto 10px auto;
                        padding: 15px 20px;
                        box-sizing: border-box;
                        border-radius: 14px;
                        background: #fff5f5;
                        border: 2px solid #d77b7b;
                        color: #8a3535;
                        font-family: Arial, sans-serif;
                        font-size: 16px;
                    ">
                        <strong>{letra})</strong> {texto} ❌
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        max-width: 900px;
                        margin: 0 auto 10px auto;
                        padding: 15px 20px;
                        box-sizing: border-box;
                        border-radius: 14px;
                        background: #f7f7f7;
                        border: 1px solid #dddddd;
                        color: #999999;
                        font-family: Arial, sans-serif;
                        font-size: 16px;
                    ">
                        <strong>{letra})</strong> {texto}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ==========================================
        # FEEDBACK
        # ==========================================

        if resposta_dada == resposta_correta:

            st.markdown(
                """
                <div style="
                    width: 100%;
                    max-width: 900px;
                    margin: 20px auto 0 auto;
                    padding: 18px 22px;
                    box-sizing: border-box;
                    border-radius: 14px;
                    background: #f3faf4;
                    border-left: 5px solid #78a982;
                    color: #315f38;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                    <strong>✅ Resposta correta!</strong><br><br>
                    Karla está orgulhosa de vocês!
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            texto_correto = pergunta["alternativas"][resposta_correta]

            st.markdown(
                f"""
                <div style="
                    width: 100%;
                    max-width: 900px;
                    margin: 20px auto 0 auto;
                    padding: 18px 22px;
                    box-sizing: border-box;
                    border-radius: 14px;
                    background: #fff9ef;
                    border-left: 5px solid #d4a843;
                    color: #70561c;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                    line-height: 1.5;
                ">
                    <strong>❌ Resposta incorreta.</strong><br><br>
                   💡 A resposta correta é:
                    <strong>{resposta_correta}) {texto_correto}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ==========================================
        # RECOMEÇAR
        # ==========================================

        st.markdown(
            "<div style='height:25px;'></div>",
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            if st.button(
                "↻ RECOMEÇAR HISTÓRIA",
                key=f"reiniciar_quiz_{numero_pergunta}",
                use_container_width=True
            ):

                reiniciar_historia()
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
        body {
            font-family: Arial, sans-serif;
            background: #f5f1e8;
            color: #222;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 950px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        h1 {
            text-align: center;
            font-size: 28px;
            margin-bottom: 25px;
            color: #222;
        }
        .karla {
            background: #f0f0f0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 16px;
            line-height: 1.5;
            color: #222;
        }
        .karla strong { display: block; margin-bottom: 5px; }
        h2 {
            font-size: 18px;
            margin-top: 25px;
            margin-bottom: 12px;
            color: #222;
        }
        .banco {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-bottom: 30px;
        }
        .palavra {
            background: #eeeeee;
            border-radius: 8px;
            padding: 9px 13px;
            font-weight: bold;
            font-size: 14px;
            color: #222;
        }
        .numeros {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin: 30px 0;
        }
        .numero {
            flex: 1;
            min-height: 70px;
            border: none;
            border-bottom: 3px solid #222;
            background: transparent;
            font-size: 30px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
            color: #222;
        }
        .numero:hover { background: #f0f0f0; }
        .numero.selecionado { background: #e6e6e6; }
        .numero.concluido { border-bottom: 4px solid #333; background: #dcdcdc; }
        .desafio {
            display: none;
            margin-top: 20px;
            padding: 25px;
            border-radius: 15px;
            background: #f7f7f7;
        }
        .desafio.ativo { display: block; }
        .pista-titulo {
            font-weight: bold;
            font-size: 19px;
            margin-bottom: 10px;
            color: #222;
        }
        .pista {
            font-size: 17px;
            line-height: 1.5;
            margin-bottom: 20px;
            color: #333;
        }
        .opcoes {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .opcao {
            border: 2px solid #333;
            background: white;
            border-radius: 9px;
            padding: 11px 16px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
            font-size: 14px;
            color: #222;
        }
        .opcao:hover { background: #eeeeee; }
        .opcao:disabled { cursor: default; }
        .feedback {
            margin-top: 18px;
            font-weight: bold;
            font-size: 17px;
            min-height: 25px;
        }
        .final {
            display: none;
            margin-top: 25px;
            padding: 22px;
            background: #eeeeee;
            border-radius: 12px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #222;
        }
        @media (max-width: 650px) {
            .container { padding: 20px; }
            h1 { font-size: 22px; }
            .numeros { gap: 4px; }
            .numero { font-size: 22px; min-height: 55px; }
            .pista { font-size: 15px; }
        }
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

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <style>

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }


            body {

                min-height: 100vh;

                font-family: Arial, sans-serif;

                background: white;

                padding: 28px 20px 35px;
            }


            /* =========================================
               QUADRINHO PRINCIPAL
            ========================================= */

            .container {

                width: 100%;

                max-width: 900px;

                margin: 0 auto;

                background: white;

                border-radius: 24px;

                padding: 38px 45px 42px;

                border: 1px solid #e9e2d6;

                box-shadow:
                    0 12px 35px rgba(0, 0, 0, 0.09);
            }


            /* =========================================
               TÍTULO
            ========================================= */

            h1 {

                text-align: center;

                font-size: 27px;

                font-weight: 800;

                letter-spacing: .5px;

                color: #222;

                margin-bottom: 13px;
            }


            h1::after {

                content: "";

                display: block;

                width: 55px;

                height: 3px;

                background: #d4a843;

                margin: 13px auto 28px;

                border-radius: 5px;
            }


            /* =========================================
               KARLA
            ========================================= */

            .karla {

                background: #faf7f0;

                border-left: 4px solid #d4a843;

                border-radius: 12px;

                padding: 18px 22px;

                margin-bottom: 30px;

                font-size: 16px;

                line-height: 1.6;

                color: #333;
            }


            /* =========================================
               SUBTÍTULO
            ========================================= */

            h2 {

                font-size: 15px;

                letter-spacing: 2px;

                text-transform: uppercase;

                text-align: center;

                color: #555;

                margin-bottom: 18px;
            }


            /* =========================================
               ÁREA DO DESAFIO
            ========================================= */

            .desafio {

                padding: 27px 30px;

                border-radius: 17px;

                background: #faf8f4;

                border: 1px solid #e8e1d5;

                text-align: center;
            }


            .pergunta {

                font-size: 19px;

                line-height: 1.7;

                color: #333;

                margin-bottom: 20px;
            }


            .lacuna {

                color: #b38725;

                font-weight: bold;
            }


            /* =========================================
               BOTÕES
            ========================================= */

            button {

                border: none;

                padding: 12px 20px;

                border-radius: 10px;

                cursor: pointer;

                font-weight: bold;

                font-size: 14px;

                transition: .2s;
            }


            .dica-btn {

                background: #333;

                color: white;

                margin-bottom: 15px;
            }


            .dica-btn:hover {

                transform: translateY(-2px);

                opacity: .9;
            }


            /* =========================================
               DICA
            ========================================= */

            .dica {

                display: none;

                text-align: left;

                background: white;

                border-left: 4px solid #d4a843;

                border-radius: 10px;

                padding: 16px 18px;

                margin: 5px 0 20px;

                font-size: 15px;

                line-height: 1.6;

                color: #444;
            }


            /* =========================================
               INPUT
            ========================================= */

            input {

                width: 100%;

                padding: 15px;

                border: 1px solid #ddd;

                border-radius: 10px;

                font-size: 16px;

                outline: none;

                background: white;

                margin-bottom: 15px;
            }


            input:focus {

                border-color: #d4a843;
            }


            /* =========================================
               RESPONDER
            ========================================= */

            .responder {

                background: #d4a843;

                color: white;

                width: 100%;

                padding: 14px;

                font-size: 15px;
            }


            .responder:hover {

                background: #bd922f;

                transform: translateY(-2px);
            }


            /* =========================================
               RESULTADO
            ========================================= */

            #resultado {

                margin-top: 18px;

                font-size: 17px;

                font-weight: bold;
            }


            .acerto {

                color: #247a3d;
            }


            .erro {

                color: #b3261e;
            }


            /* =========================================
               RESPONSIVO
            ========================================= */

            @media (max-width: 650px) {

                body {

                    padding: 18px 12px;
                }


                .container {

                    padding: 28px 20px;

                    border-radius: 18px;
                }


                h1 {

                    font-size: 23px;
                }


                .desafio {

                    padding: 22px 18px;
                }


                .pergunta {

                    font-size: 17px;
                }

            }

        </style>

    </head>


    <body>


        <!-- =========================================
             QUADRINHO
        ========================================== -->

        <div class="container">


            <h1>
                DESAFIO — POLÍMERO
            </h1>


            <!-- KARLA -->

            <div class="karla">

                <strong>Karla:</strong><br>

                "Antes de continuar nossa investigação,
                quero saber se vocês entenderam o que
                existe por trás do material da garrafa."

            </div>


            <!-- SUBTÍTULO -->

            <h2>
                IDENTIFIQUE O MATERIAL
            </h2>


            <!-- DESAFIO -->

            <div class="desafio">


                <p class="pergunta">

                    O PET é um
                    <span class="lacuna">
                        __________
                    </span>

                    formado pela repetição de unidades
                    menores, formando uma cadeia de moléculas.

                </p>


                <!-- DICA -->

                <button
                    class="dica-btn"
                    onclick="mostrarDica()"
                    id="dicaBtn"
                >

                    💡 VER DICA

                </button>


                <div
                    class="dica"
                    id="dica"
                >

                    Imagine um colar: uma grande estrutura
                    construída pela repetição de várias peças
                    menores. Na Química, damos um nome específico
                    para esse tipo de estrutura. A palavra começa com
                    <strong>P</strong>.

                </div>


                <!-- CAMPO -->

                <input
                    type="text"
                    id="resposta"
                    placeholder="Digite sua resposta..."
                    autocomplete="off"
                >


                <!-- RESPONDER -->

                <button
                    class="responder"
                    onclick="verificarResposta()"
                    id="responderBtn"
                >

                    RESPONDER

                </button>


                <!-- RESULTADO -->

                <div id="resultado"></div>


            </div>


        </div>


        <script>


            // =========================================
            // MOSTRAR / ESCONDER DICA
            // =========================================

            function mostrarDica() {

                const dica =
                    document.getElementById("dica");

                const botao =
                    document.getElementById("dicaBtn");


                if (
                    dica.style.display === "none" ||
                    dica.style.display === ""
                ) {

                    dica.style.display = "block";

                    botao.textContent =
                        "ESCONDER DICA";

                }

                else {

                    dica.style.display = "none";

                    botao.textContent =
                        "💡 VER DICA";

                }

            }


            // =========================================
            // VERIFICAR RESPOSTA
            // =========================================

            function verificarResposta() {

                const campo =
                    document.getElementById("resposta");

                const resultado =
                    document.getElementById("resultado");

                const botao =
                    document.getElementById("responderBtn");


                const resposta =
                    campo.value
                    .trim()
                    .toLowerCase()
                    .normalize("NFD")
                    .replace(/[\\u0300-\\u036f]/g, "");


                if (resposta === "polimero") {

                    resultado.textContent =
                        "✓ ACERTOU! O PET é um polímero.";

                    resultado.className =
                        "acerto";


                    campo.disabled = true;

                    botao.disabled = true;

                    botao.style.opacity = "0.5";

                    botao.style.cursor = "default";

                }


                else {

                    resultado.textContent =
                        "✗ Tente novamente!";

                    resultado.className =
                        "erro";

                    campo.value = "";

                    campo.focus();

                }

            }


            // =========================================
            // ENTER PARA RESPONDER
            // =========================================

            document
                .getElementById("resposta")
                .addEventListener(
                    "keydown",
                    function(event) {

                        if (event.key === "Enter") {

                            verificarResposta();

                        }

                    }
                );


        </script>


    </body>

    </html>
    """


# =========================================
# MOSTRAR QUADRINHO
# =========================================

    components.html(
        html_polimero,
        height=700,
        scrolling=True
    )


# =========================================================
# INÍCIO DO APP
# =========================================================

aplicar_css()

inicializar_estado()


# =========================================================
# CONTAINER PRINCIPAL
# =========================================================

st.markdown(
    '<div class="main-container">',
    unsafe_allow_html=True
)


# =========================================================
# CENA ATUAL
# =========================================================

cena_id = st.session_state.cena_atual


# =========================================================
# DESAFIOS
#
# CADA CENA É CHAMADA UMA ÚNICA VEZ.
# O st.stop() impede que ela seja executada novamente.
# =========================================================


if cena_id == "desafio_quiz_1":

    renderizar_quiz(0)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()


elif cena_id == "desafio_quiz_2":

    renderizar_quiz(1)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()


elif cena_id == "desafio_plasticos":

    renderizar_desafio_plasticos()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()


elif cena_id == "desafio_polimero":

    # =========================================
    # 1. QUADRINHO
    # =========================================

    renderizar_desafio_polimero()


    # =========================================
    # 2. ESPAÇO ABAIXO DO QUADRINHO
    # =========================================

    st.markdown(
        "<div style='height: 25px;'></div>",
        unsafe_allow_html=True
    )


    # =========================================
    # 3. BOTÃO RECOMEÇAR
    #
    # FORA DO QUADRINHO
    # ABAIXO DO QUADRINHO
    # CENTRALIZADO
    # =========================================

    col_esquerda, col_botao, col_direita = st.columns(
        [1, 2, 1]
    )


    with col_botao:

        if st.button(
            "↻ RECOMEÇAR HISTÓRIA",
            key="reiniciar_polimero",
            use_container_width=True
        ):

            reiniciar_historia()


    # =========================================
    # 4. FECHAR CONTAINER
    # =========================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# CENAS NORMAIS DA HISTÓRIA
# =========================================================
#
# A PARTIR DAQUI, COLE AS SUAS CENAS ORIGINAIS.
#
# NÃO COLOQUE NOVAMENTE:
#
# if cena_id == "desafio_polimero":
#
# porque ele já foi tratado acima.
# =========================================================


# ---------------------------------------------------------
# SUAS CENAS ORIGINAIS COMEÇAM AQUI
# ---------------------------------------------------------

# Exemplo da estrutura:
#
# if cena_id == "inicio":
#     ...
#
# elif cena_id == "cena_1":
#     ...
#
# elif cena_id == "cena_2":
#     ...
#
# elif cena_id == "cena_3":
#     ...
#
# etc.


# =========================================================
# FECHAR CONTAINER
# =========================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
# ==========================================
# CENAS NORMAIS DA HISTÓRIA
# ==========================================

# ↓↓↓ AQUI CONTINUA O RESTANTE DO SEU CÓDIGO ↓↓↓


# Exemplo:
#
# if cena_id == "inicio":
#     renderizar_inicio()
#
# elif cena_id == "cena_1":
#     renderizar_cena_1()
#
# elif cena_id == "cena_2":
#     renderizar_cena_2()


# ==========================================
# FECHAR CONTAINER
# ==========================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
# ==========================================
# DESAFIOS (TELAS SEPARADAS)
# ==========================================
if cena_id == "desafio_quiz_1":
    renderizar_quiz(0)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if cena_id == "desafio_quiz_2":
    renderizar_quiz(1)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if cena_id == "desafio_plasticos":
    renderizar_desafio_plasticos()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

if cena_id == "desafio_polimero":
    renderizar_desafio_polimero()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# CENAS DA HISTÓRIA
# ==========================================
cena = get_cena(cena_id)

if cena:
    # ===== INÍCIO =====
    if cena["tipo"] == "inicio":
        # A CAPA APARECE IMEDIATAMENTE AO ABRIR O SITE.
        renderizar_imagem(cena["imagem"], "Capa da história")

        st.markdown(f"""
            <h1 class="titulo">{cena.get("titulo", "História")}</h1>
            <div class="linha"></div>
            <p class="subtitulo">{cena.get("descricao", "")}</p>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="btn-comecar">', unsafe_allow_html=True)
            if st.button("▶ COMEÇAR", key="comecar", use_container_width=True):
                ir_para_cena("pagina_01")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== CENA =====
    elif cena["tipo"] == "cena":
        renderizar_imagem(cena["imagem"])
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ CONTINUAR", key="continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
    
    # ===== ESCOLHA =====
    elif cena["tipo"] == "escolha":
        renderizar_imagem(cena["imagem"])
        
        st.markdown(f'<p class="pergunta">{cena.get("pergunta", "O que fazer?")}</p>', unsafe_allow_html=True)
        
        opcoes = list(cena["opcoes"].items())
        if len(opcoes) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(opcoes[0][0], key="escolha_1", use_container_width=True):
                    ir_para_cena(opcoes[0][1])
            with col2:
                if st.button(opcoes[1][0], key="escolha_2", use_container_width=True):
                    ir_para_cena(opcoes[1][1])
    
    # ===== FINAL =====
    elif cena["tipo"] == "final":
        renderizar_imagem(cena["imagem"])
        
        if "mensagem" in cena:
            st.markdown(f'<p class="mensagem">✦ {cena["mensagem"]} ✦</p>', unsafe_allow_html=True)
        
        # Botão de desafio específico para cada final
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Final 1 → Quiz Pergunta 1
            if cena_id == "feedback_01b":
                if st.button("FAZER O DESAFIO", key="ir_desafio_1", use_container_width=True):
                    ir_para_cena("desafio_quiz_1")
            
            # Final 2 → Quiz Pergunta 2
            elif cena_id == "feedback_02a":
                if st.button("FAZER O DESAFIO", key="ir_desafio_2", use_container_width=True):
                    ir_para_cena("desafio_quiz_2")
            
            # Final 3 → Decodificar Plásticos
            elif cena_id == "feedback_03a":
                if st.button("FAZER O DESAFIO", key="ir_desafio_3", use_container_width=True):
                    ir_para_cena("desafio_plasticos")
            
            # Final 4 (vitória) → Polímero
            elif cena_id == "pagina_12b":
                if st.button("FAZER O DESAFIO FINAL", key="ir_desafio_4", use_container_width=True):
                    ir_para_cena("desafio_polimero")

st.markdown('</div>', unsafe_allow_html=True)