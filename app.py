# app.py
import streamlit as st
from story import HISTORY, get_cena
import base64

# Configuração da página
st.set_page_config(
    page_title="História em Quadrinhos Interativa",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS SUPER ESTILIZADO
def aplicar_css():
    st.markdown("""
        <style>
        /* Reset e fundo */
        .stApp {
            background: linear-gradient(135deg, #0F0E17 0%, #1A1A2E 50%, #16213E 100%);
        }
        
        .main > div {
            padding: 0 !important;
        }
        
        /* Container principal */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        /* Título da história */
        .titulo-historia {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FFD93D 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 20px 0;
            font-family: 'Georgia', serif;
            text-shadow: 0 0 40px rgba(255,107,107,0.3);
            letter-spacing: 2px;
        }
        
        /* Descrição */
        .descricao-historia {
            font-size: 1.2rem;
            color: #A8A8B3;
            text-align: center;
            max-width: 600px;
            margin: 0 auto 40px auto;
            font-family: 'Arial', sans-serif;
            line-height: 1.8;
            padding: 0 20px;
        }
        
        /* Container da imagem */
        .imagem-container {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 80px rgba(255,107,107,0.1);
            transition: transform 0.3s ease;
            position: relative;
        }
        
        .imagem-container:hover {
            transform: scale(1.01);
        }
        
        .imagem-container::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #FF6B6B, #FF8E53, #FFD93D, #6C5CE7);
            background-size: 400% 400%;
            border-radius: 22px;
            z-index: -1;
            animation: gradient 3s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .imagem-historia {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 20px;
        }
        
        /* Pergunta de escolha */
        .pergunta-escolha {
            font-size: 1.8rem;
            color: #FFFFFF;
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
            text-shadow: 0 0 30px rgba(255,107,107,0.3);
            font-family: 'Georgia', serif;
        }
        
        .pergunta-escolha::before {
            content: '⚡ ';
        }
        
        .pergunta-escolha::after {
            content: ' ⚡';
        }
        
        /* Mensagem final */
        .mensagem-final {
            font-size: 1.5rem;
            color: #FFD93D;
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
            text-shadow: 0 0 30px rgba(255,217,61,0.3);
            background: rgba(255,107,107,0.1);
            padding: 20px 40px;
            border-radius: 15px;
            border: 2px solid rgba(255,107,107,0.2);
            backdrop-filter: blur(10px);
        }
        
        /* Botões personalizados */
        .stButton > button {
            width: 100%;
            padding: 16px 40px;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 15px;
            border: none;
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            color: white;
            transition: all 0.3s ease;
            box-shadow: 0 8px 30px rgba(255,107,107,0.3);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Arial', sans-serif;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 40px rgba(255,107,107,0.5);
            background: linear-gradient(135deg, #FF8E53 0%, #FFD93D 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0px) scale(0.98);
        }
        
        /* Botões de escolha */
        .botao-escolha {
            width: 100%;
            padding: 18px 25px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 15px;
            border: 2px solid rgba(255,107,107,0.3);
            background: rgba(255,107,107,0.1);
            color: white;
            transition: all 0.3s ease;
            cursor: pointer;
            backdrop-filter: blur(10px);
            text-align: center;
            font-family: 'Arial', sans-serif;
        }
        
        .botao-escolha:hover {
            background: rgba(255,107,107,0.3);
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 30px rgba(255,107,107,0.3);
            border-color: #FF6B6B;
        }
        
        /* Indicador de progresso */
        .indicador-cena {
            color: rgba(255,255,255,0.3);
            text-align: center;
            font-size: 0.9rem;
            margin-top: 20px;
            font-family: 'Arial', sans-serif;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        
        /* Esconder elementos do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Responsividade */
        @media (max-width: 768px) {
            .titulo-historia {
                font-size: 2.5rem;
            }
            
            .descricao-historia {
                font-size: 1rem;
                padding: 0 20px;
            }
            
            .pergunta-escolha {
                font-size: 1.3rem;
            }
            
            .stButton > button {
                font-size: 1rem;
                padding: 14px 20px;
            }
            
            .botao-escolha {
                font-size: 0.9rem;
                padding: 14px 15px;
            }
            
            .mensagem-final {
                font-size: 1.2rem;
                padding: 15px 20px;
            }
        }
        
        /* Animação de fade in */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* Linha decorativa */
        .linha-decorativa {
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, #FF6B6B, #FFD93D);
            margin: 20px auto;
            border-radius: 3px;
        }
        </style>
    """, unsafe_allow_html=True)

# Função para exibir imagem com estilo
def exibir_imagem(caminho_imagem):
    try:
        st.markdown(f"""
            <div class="imagem-container fade-in">
                <img src="{caminho_imagem}" class="imagem-historia" alt="Página da história">
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Erro ao carregar imagem: {e}")
        st.info(f"Verifique se a imagem '{caminho_imagem}' existe na pasta assets/images/")

# Funções de navegação
def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"
    if "historico" not in st.session_state:
        st.session_state.historico = []

def ir_para_cena(cena_id):
    if cena_id in HISTORY:
        st.session_state.cena_atual = cena_id
        st.rerun()

def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.session_state.historico = []
    st.rerun()

# Aplicar CSS
aplicar_css()

# Inicializar estado
inicializar_estado()

# Container principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Obter cena atual
cena_id = st.session_state.cena_atual
cena = get_cena(cena_id)

if cena:
    # TELA INICIAL
    if cena["tipo"] == "inicio":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'<h1 class="titulo-historia fade-in">{cena.get("titulo", "História em Quadrinhos")}</h1>', unsafe_allow_html=True)
            st.markdown('<div class="linha-decorativa"></div>', unsafe_allow_html=True)
            
            exibir_imagem(cena["imagem"])
            
            if "descricao" in cena:
                st.markdown(f'<p class="descricao-historia fade-in">{cena["descricao"]}</p>', unsafe_allow_html=True)
            
            if st.button("🌟 Começar a História", key="btn_comecar", use_container_width=True):
                if "cena_01" in HISTORY:
                    ir_para_cena("cena_01")
                else:
                    st.error("Erro: Primeira cena não encontrada!")
    
    # CENA NORMAL
    elif cena["tipo"] == "cena":
        exibir_imagem(cena["imagem"])
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ Continuar", key="btn_continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
                else:
                    st.error("Erro: Próxima cena não definida!")
        
        st.markdown(f'<p class="indicador-cena">📖 {cena_id.replace("_", " ").title()}</p>', unsafe_allow_html=True)
    
    # CENA DE ESCOLHA
    elif cena["tipo"] == "escolha":
        exibir_imagem(cena["imagem"])
        
        st.markdown(f'<p class="pergunta-escolha">{cena.get("pergunta", "O que fazer?")}</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        opcoes = list(cena["opcoes"].items())
        if len(opcoes) >= 2:
            with col1:
                if st.button(f"✨ {opcoes[0][0]}", key="escolha_1", use_container_width=True):
                    ir_para_cena(opcoes[0][1])
            
            with col2:
                if st.button(f"🔥 {opcoes[1][0]}", key="escolha_2", use_container_width=True):
                    ir_para_cena(opcoes[1][1])
        
        st.markdown(f'<p class="indicador-cena">📖 {cena_id.replace("_", " ").title()}</p>', unsafe_allow_html=True)
    
    # FINAL
    elif cena["tipo"] == "final":
        exibir_imagem(cena["imagem"])
        
        if "mensagem" in cena:
            st.markdown(f'<p class="mensagem-final fade-in">🎬 {cena["mensagem"]}</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Recomeçar História", key="btn_reiniciar", use_container_width=True):
                reiniciar_historia()

st.markdown('</div>', unsafe_allow_html=True)