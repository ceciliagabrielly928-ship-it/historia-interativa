# app.py
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
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS GLOBAL
# ==========================================
def aplicar_css():
    st.markdown("""
        <style>
        /* Remove tudo do Streamlit */
        .stApp { background: #0a0a0a !important; }
        .main > div { padding: 0 !important; max-width: 100% !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; padding-top: 0 !important; }
        #MainMenu {display: none !important;}
        footer {display: none !important;}
        header {display: none !important;}
        .stDeployButton {display: none !important;}
        
        /* Container principal */
        .main-container {
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        /* Títulos */
        .titulo {
            font-size: 3.5rem;
            font-weight: 900;
            color: #ffffff;
            font-family: 'Georgia', serif;
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
        
        /* Imagens */
        .imagem-container {
            max-width: 900px;
            width: 100%;
            margin: 0 auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        }
        
        .imagem-container img {
            width: 100%;
            height: auto;
            display: block;
        }
        
        /* Botões */
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
            font-family: 'Arial', sans-serif !important;
        }
        
        .stButton button:hover {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            box-shadow: 0 10px 40px rgba(212,168,67,0.3) !important;
        }
        
        /* Botão COMEÇAR (dourado cheio) */
        .btn-comecar button {
            background: #d4a843 !important;
            color: #0a0a0a !important;
            border: none !important;
        }
        
        .btn-comecar button:hover {
            background: #e8c86a !important;
            transform: scale(1.02) !important;
        }
        
        /* Pergunta */
        .pergunta {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 300;
            text-align: center;
            margin: 30px 0 20px 0;
            font-family: 'Georgia', serif;
        }
        
        /* Mensagem final */
        .mensagem {
            color: #d4a843;
            font-size: 1.3rem;
            text-align: center;
            margin: 30px 0;
            font-family: 'Georgia', serif;
        }
        
        /* Responsivo */
        @media (max-width: 768px) {
            .titulo { font-size: 2.5rem; }
            .stButton button { font-size: 0.8rem !important; padding: 14px 20px !important; }
        }
        </style>
    """, unsafe_allow_html=True)


# ==========================================
# QUIZ - PERGUNTAS
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
# FUNÇÕES DE ESTADO
# ==========================================
def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"
    if "quiz_pergunta_atual" not in st.session_state:
        st.session_state.quiz_pergunta_atual = 0
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
    st.rerun()


def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.session_state.quiz_pergunta_atual = 0
    st.session_state.quiz_pontuacao = 0
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.session_state.quiz_finalizado = False
    st.rerun()


def reiniciar_quiz():
    st.session_state.quiz_pergunta_atual = 0
    st.session_state.quiz_pontuacao = 0
    st.session_state.quiz_respondeu = False
    st.session_state.quiz_resposta_dada = None
    st.session_state.quiz_finalizado = False
    st.rerun()


# ==========================================
# RENDERIZAÇÃO: QUIZ
# ==========================================
def renderizar_quiz():
    st.markdown("""
        <style>
        .quiz-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .card-pergunta {
            background: rgba(20, 40, 20, 0.9);
            border: 2px solid #4ade80;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px rgba(74, 222, 128, 0.2);
        }
        
        .numero-pergunta {
            color: #4ade80;
            font-size: 0.9rem;
            font-weight: bold;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 15px;
            font-family: Arial, sans-serif;
        }
        
        .texto-pergunta {
            color: #ffffff;
            font-size: 1.15rem;
            line-height: 1.6;
            font-family: Georgia, serif;
        }
        
        .karla-icone {
            display: inline-block;
            background: #4ade80;
            color: #0d1f0d;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: bold;
            font-size: 1.2rem;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        .feedback-acerto {
            background: rgba(74, 222, 128, 0.15);
            border-left: 4px solid #4ade80;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            color: #4ade80;
            font-size: 1.1rem;
            font-weight: bold;
            font-family: Arial, sans-serif;
        }
        
        .feedback-erro {
            background: rgba(239, 68, 68, 0.15);
            border-left: 4px solid #ef4444;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            color: #fca5a5;
            font-size: 1.1rem;
            font-weight: bold;
            font-family: Arial, sans-serif;
        }
        
        .resposta-correta {
            color: #4ade80;
            display: block;
            margin-top: 10px;
            font-size: 1rem;
        }
        
        .resultado-final {
            text-align: center;
            padding: 40px;
            background: rgba(20, 40, 20, 0.9);
            border: 2px solid #4ade80;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(74, 222, 128, 0.3);
        }
        
        .resultado-titulo {
            color: #4ade80;
            font-size: 2.5rem;
            font-family: Georgia, serif;
            margin-bottom: 10px;
        }
        
        .resultado-pontuacao {
            color: #ffffff;
            font-size: 3rem;
            font-weight: bold;
            font-family: Georgia, serif;
            margin: 20px 0;
        }
        
        .resultado-mensagem {
            color: #a7f3d0;
            font-size: 1.2rem;
            font-family: Georgia, serif;
            margin-top: 20px;
            line-height: 1.6;
        }
        
        .progresso {
            color: #a7f3d0;
            font-size: 0.9rem;
            text-align: center;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 20px;
            font-family: Arial, sans-serif;
        }
        
        .barra-progresso {
            width: 100%;
            height: 6px;
            background: rgba(74, 222, 128, 0.2);
            border-radius: 3px;
            margin-bottom: 30px;
            overflow: hidden;
        }
        
        .barra-progresso-preenchida {
            height: 100%;
            background: linear-gradient(90deg, #4ade80, #22c55e);
            border-radius: 3px;
            transition: width 0.5s ease;
        }
        
        /* Botões do quiz */
        .quiz-container .stButton button {
            border: 2px solid #4ade80 !important;
            background: rgba(74, 222, 128, 0.1) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            text-align: left !important;
            text-transform: none !important;
            letter-spacing: 0 !important;
            padding: 16px 20px !important;
            font-size: 1rem !important;
        }
        
        .quiz-container .stButton button:hover {
            background: rgba(74, 222, 128, 0.3) !important;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    total = len(PERGUNTAS_QUIZ)
    
    # ===== TELA FINAL =====
    if st.session_state.quiz_finalizado:
        pontuacao = st.session_state.quiz_pontuacao
        
        if pontuacao == total:
            mensagem = "🌟 Perfeito! Karla está orgulhosa de vocês! O futuro do planeta está em boas mãos!"
            emoji = "🏆"
        elif pontuacao == 1:
            mensagem = "💚 Muito bem! Vocês estão no caminho certo para salvar o futuro!"
            emoji = "🌱"
        else:
            mensagem = "📚 Karla acredita em vocês! Revisem as decisões e tentem novamente."
            emoji = "🌍"
        
        st.markdown(f"""
            <div class="resultado-final">
                <div style="font-size: 4rem; margin-bottom: 10px;">{emoji}</div>
                <h1 class="resultado-titulo">Quiz Concluído!</h1>
                <div class="resultado-pontuacao">{pontuacao} / {total}</div>
                <p class="resultado-mensagem">{mensagem}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Jogar Novamente", key="quiz_reiniciar"):
                reiniciar_quiz()
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # ===== PERGUNTA ATUAL =====
    pergunta_atual = st.session_state.quiz_pergunta_atual
    pergunta = PERGUNTAS_QUIZ[pergunta_atual]
    progresso_pct = (pergunta_atual / total) * 100
    
    st.markdown(f"""
        <div class="progresso">Pergunta {pergunta_atual + 1} de {total}</div>
        <div class="barra-progresso">
            <div class="barra-progresso-preenchida" style="width: {progresso_pct}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="card-pergunta">
            <div class="numero-pergunta">
                <span class="karla-icone">K</span> Karla pergunta:
            </div>
            <div class="texto-pergunta">{pergunta["pergunta"]}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== NÃO RESPONDEU: MOSTRA BOTÕES =====
    if not st.session_state.quiz_respondeu:
        for letra, texto in pergunta["alternativas"].items():
            if st.button(f"{letra})  {texto}", key=f"alt_{pergunta_atual}_{letra}"):
                st.session_state.quiz_respondeu = True
                st.session_state.quiz_resposta_dada = letra
                if letra == pergunta["correta"]:
                    st.session_state.quiz_pontuacao += 1
                st.rerun()
    
    # ===== RESPONDEU: MOSTRA FEEDBACK =====
    else:
        resposta_dada = st.session_state.quiz_resposta_dada
        resposta_correta = pergunta["correta"]
        
        for letra, texto in pergunta["alternativas"].items():
            if letra == resposta_correta:
                st.markdown(f"""
                    <div style="padding: 12px 20px; margin-bottom: 8px; border-radius: 10px;
                                background: rgba(74, 222, 128, 0.2); border: 2px solid #4ade80;
                                color: #ffffff; font-family: Arial;">
                        <strong>{letra})</strong> {texto} ✅
                    </div>
                """, unsafe_allow_html=True)
            elif letra == resposta_dada:
                st.markdown(f"""
                    <div style="padding: 12px 20px; margin-bottom: 8px; border-radius: 10px;
                                background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444;
                                color: #ffffff; font-family: Arial;">
                        <strong>{letra})</strong> {texto} ❌
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="padding: 12px 20px; margin-bottom: 8px; border-radius: 10px;
                                background: rgba(255, 255, 255, 0.05); border: 1px solid #333;
                                color: #888; font-family: Arial;">
                        <strong>{letra})</strong> {texto}
                    </div>
                """, unsafe_allow_html=True)
        
        if resposta_dada == resposta_correta:
            st.markdown("""
                <div class="feedback-acerto">
                    ✅ Resposta correta! Vocês estão ajudando a salvar o futuro!
                </div>
            """, unsafe_allow_html=True)
        else:
            texto_correto = pergunta["alternativas"][resposta_correta]
            st.markdown(f"""
                <div class="feedback-erro">
                    ❌ Resposta incorreta. Karla avisa que essa decisão não ajuda o planeta.
                    <span class="resposta-correta">💡 Resposta correta: {resposta_correta}) {texto_correto}</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if pergunta_atual < total - 1:
                if st.button("➡️ Próxima Pergunta", key="quiz_proxima"):
                    st.session_state.quiz_pergunta_atual += 1
                    st.session_state.quiz_respondeu = False
                    st.session_state.quiz_resposta_dada = None
                    st.rerun()
            else:
                if st.button("🏁 Ver Resultado", key="quiz_ver_resultado"):
                    st.session_state.quiz_finalizado = True
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# RENDERIZAÇÃO: DESAFIO DOS PLÁSTICOS (7 números)
# ==========================================
def renderizar_desafio_plasticos():
    st.markdown("""
        <style>
        .desafio-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        .desafio-card {
            background: #f5f1e8;
            border-radius: 20px;
            padding: 30px;
            color: #222;
        }
        .desafio-card h1 {
            text-align: center;
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: #222;
        }
        .karla-box {
            background: #f0f0f0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 20px;
            font-size: 1rem;
            line-height: 1.5;
            color: #222;
        }
        .karla-box strong { display: block; margin-bottom: 5px; color: #222; }
        .banco {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }
        .palavra {
            background: #eeeeee;
            border-radius: 8px;
            padding: 9px 13px;
            font-weight: bold;
            font-size: 0.9rem;
            color: #222;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # HTML do desafio (JavaScript funcional)
    html_desafio = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f1e8;
            color: #222;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }
        h1 { text-align: center; font-size: 26px; margin-bottom: 20px; }
        .karla {
            background: #f0f0f0;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            font-size: 15px;
            line-height: 1.5;
        }
        .karla strong { display: block; margin-bottom: 5px; }
        h2 { font-size: 18px; margin-top: 20px; margin-bottom: 10px; }
        .banco {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin-bottom: 25px;
        }
        .palavra {
            background: #eeeeee;
            border-radius: 8px;
            padding: 8px 12px;
            font-weight: bold;
            font-size: 13px;
        }
        .numeros {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            margin: 25px 0;
        }
        .numero {
            flex: 1;
            min-height: 60px;
            border: none;
            border-bottom: 3px solid #222;
            background: transparent;
            font-size: 26px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        .numero:hover { background: #f0f0f0; }
        .numero.selecionado { background: #e6e6e6; }
        .numero.concluido { border-bottom: 4px solid #333; background: #dcdcdc; }
        .desafio-box {
            display: none;
            margin-top: 20px;
            padding: 20px;
            border-radius: 15px;
            background: #f7f7f7;
        }
        .desafio-box.ativo { display: block; }
        .pista-titulo { font-weight: bold; font-size: 17px; margin-bottom: 10px; }
        .pista { font-size: 16px; line-height: 1.5; margin-bottom: 18px; }
        .opcoes { display: flex; flex-wrap: wrap; gap: 8px; }
        .opcao {
            border: 2px solid #333;
            background: white;
            border-radius: 9px;
            padding: 10px 15px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }
        .opcao:hover { background: #eeeeee; }
        .opcao:disabled { cursor: default; }
        .feedback { margin-top: 15px; font-weight: bold; font-size: 16px; min-height: 22px; }
        .final-box {
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: #eeeeee;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .final-box button {
            margin-top: 12px;
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            background: #222;
            color: white;
            font-size: 14px;
            cursor: pointer;
        }
        @media (max-width: 650px) {
            .container { padding: 18px; }
            h1 { font-size: 20px; }
            .numeros { gap: 3px; }
            .numero { font-size: 20px; min-height: 50px; }
            .pista { font-size: 14px; }
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
        <div id="desafio" class="desafio-box">
            <div class="pista-titulo" id="pistaTitulo"></div>
            <div class="pista" id="pista"></div>
            <div class="opcoes" id="opcoes"></div>
            <div class="feedback" id="feedback"></div>
        </div>
        <div id="final" class="final-box">
            🎉 Parabéns! Você decodificou todos os tipos de plástico!
            <br>
            <button onclick="reiniciar()">Jogar novamente</button>
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
    
    function reiniciar() {
        resolvidos = [];
        numeroAtual = null;
        document.getElementById("final").style.display = "none";
        document.getElementById("desafio").classList.remove("ativo");
        document.querySelectorAll(".numero").forEach(b => {
            b.classList.remove("concluido");
            b.classList.remove("selecionado");
        });
    }
    </script>
    </body>
    </html>
    """
    
    components.html(html_desafio, height=800, scrolling=True)
    
    # Botão para voltar
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬅️ Voltar para o Quiz", key="voltar_quiz_plasticos"):
            ir_para_cena("quiz")


# ==========================================
# RENDERIZAÇÃO: DESAFIO POLÍMERO
# ==========================================
def renderizar_desafio_polimero():
    html_polimero = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: #f4f1eb;
            padding: 20px;
        }
        .desafio-box {
            width: 90%;
            max-width: 650px;
            background: white;
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        h1 { font-size: 22px; margin-bottom: 25px; color: #222; }
        .pergunta { font-size: 17px; line-height: 1.6; color: #333; }
        .dica {
            display: none;
            margin: 18px 0;
            padding: 16px;
            background: #f5f5f5;
            border-left: 4px solid #555;
            border-radius: 8px;
            text-align: left;
            line-height: 1.5;
            font-size: 14px;
        }
        button {
            border: none;
            padding: 12px 20px;
            margin: 8px 4px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            background: #222;
            color: white;
            transition: 0.2s;
            font-size: 14px;
        }
        button:hover { transform: translateY(-2px); opacity: 0.9; }
        input {
            width: 100%;
            padding: 14px;
            margin-top: 18px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 15px;
            outline: none;
        }
        input:focus { border-color: #555; }
        #resultado { margin-top: 18px; font-size: 17px; font-weight: bold; }
        .acerto { color: #247a3d; }
        .erro { color: #b3261e; }
    </style>
    </head>
    <body>
    <div class="desafio-box">
        <h1>DESAFIO — DECODIFIQUE OS PLÁSTICOS</h1>
        <p class="pergunta">
            O PET é um <strong>__________</strong> formado pela repetição
            de unidades menores, formando uma cadeia de moléculas.
        </p>
        <button onclick="mostrarDica()" id="dicaBtn">💡 VER DICA</button>
        <div class="dica" id="dica">
            "Imagine um colar: uma grande estrutura construída pela repetição
            de várias peças menores. Na Química, damos um nome específico para
            esse tipo de estrutura. Começa com P."
        </div>
        <input type="text" id="resposta" placeholder="Digite sua resposta..." autocomplete="off">
        <button onclick="verificarResposta()" id="responderBtn">RESPONDER</button>
        <div id="resultado"></div>
    </div>
    <script>
    function mostrarDica() {
        const d = document.getElementById("dica");
        const b = document.getElementById("dicaBtn");
        if (d.style.display === "none" || d.style.display === "") {
            d.style.display = "block";
            b.textContent = "🙈 ESCONDER DICA";
        } else {
            d.style.display = "none";
            b.textContent = "💡 VER DICA";
        }
    }
    
    function verificarResposta() {
        const c = document.getElementById("resposta");
        const r = document.getElementById("resultado");
        const b = document.getElementById("responderBtn");
        const resp = c.value.trim().toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
        if (resp === "polimero") {
            r.textContent = "🎉 ACERTOU! O PET é um polímero.";
            r.className = "acerto";
            c.disabled = true;
            b.disabled = true;
            b.style.opacity = "0.5";
            b.style.cursor = "default";
        } else {
            r.textContent = "❌ Quase! Tente novamente.";
            r.className = "erro";
            c.value = "";
            c.focus();
        }
    }
    </script>
    </body>
    </html>
    """
    
    components.html(html_polimero, height=600, scrolling=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⬅️ Voltar", key="voltar_polimero"):
            ir_para_cena("quiz")


# ==========================================
# APLICAR CSS E INICIALIZAR
# ==========================================
aplicar_css()
inicializar_estado()

# ==========================================
# CONTAINER PRINCIPAL
# ==========================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

cena_id = st.session_state.cena_atual

# ===== PÁGINAS ESPECIAIS =====
if cena_id == "quiz":
    renderizar_quiz()
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

# ===== CENAS DA HISTÓRIA =====
cena = get_cena(cena_id)

if cena:
    # ===== TELA INICIAL =====
    if cena["tipo"] == "inicio":
        st.markdown(f"""
            <h1 class="titulo">{cena.get("titulo", "História")}</h1>
            <div class="linha"></div>
            <p class="subtitulo">{cena.get("descricao", "")}</p>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="btn-comecar">', unsafe_allow_html=True)
            if st.button("▶ COMEÇAR", key="comecar", use_container_width=True):
                ir_para_cena("pagina_01")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== CENA NORMAL =====
    elif cena["tipo"] == "cena":
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ CONTINUAR", key="continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
    
    # ===== CENA DE ESCOLHA =====
    elif cena["tipo"] == "escolha":
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{cena['imagem']}" alt="">
            </div>
        """, unsafe_allow_html=True)
        
        if "mensagem" in cena:
            st.markdown(f'<p class="mensagem">✦ {cena["mensagem"]} ✦</p>', unsafe_allow_html=True)
        
        # Botões especiais para o final
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if cena_id == "pagina_12b":
                # Final de VITÓRIA: mostrar opções de quiz e desafios
                st.markdown("### 🎯 Continue aprendendo!")
                if st.button("📝 Fazer o Quiz", key="ir_quiz", use_container_width=True):
                    ir_para_cena("quiz")
                if st.button("🔢 Decodificar os Plásticos", key="ir_desafio_plasticos", use_container_width=True):
                    ir_para_cena("desafio_plasticos")
                if st.button("🧪 Descobrir o Polímero", key="ir_desafio_polimero", use_container_width=True):
                    ir_para_cena("desafio_polimero")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("↻ RECOMEÇAR HISTÓRIA", key="reiniciar", use_container_width=True):
                reiniciar_historia()

st.markdown('</div>', unsafe_allow_html=True)