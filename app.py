# app.py
import streamlit as st
from story import HISTORY, get_cena

# Configuração da página (deve ser a primeira chamada Streamlit)
st.set_page_config(
    page_title="História em Quadrinhos Interativa",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para melhorar a aparência
def aplicar_css():
    st.markdown("""
        <style>
        /* Remove espaçamentos padrão */
        .main > div {
            padding-top: 0;
        }
        
        /* Estilo para o título da história */
        .titulo-historia {
            font-size: 3.5rem;
            font-weight: bold;
            color: #FFFFFF;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 20px;
            font-family: 'Georgia', serif;
        }
        
        /* Estilo para a descrição */
        .descricao-historia {
            font-size: 1.2rem;
            color: #E0E0E0;
            text-align: center;
            max-width: 600px;
            margin: 0 auto 30px auto;
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
        }
        
        /* Estilo para a pergunta das escolhas */
        .pergunta-escolha {
            font-size: 1.5rem;
            color: #FFFFFF;
            text-align: center;
            margin: 20px 0;
            font-weight: bold;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        }
        
        /* Estilo para mensagem final */
        .mensagem-final {
            font-size: 1.3rem;
            color: #FFD700;
            text-align: center;
            margin: 20px 0;
            font-weight: bold;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            background-color: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
        }
        
        /* Estilo para o container da imagem */
        .imagem-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto;
            max-width: 900px;
        }
        
        /* Estilo para as imagens */
        .imagem-historia {
            width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.6);
            transition: transform 0.3s ease;
        }
        
        .imagem-historia:hover {
            transform: scale(1.01);
        }
        
        /* Estilo para botões personalizados */
        .stButton > button {
            width: 100%;
            padding: 12px 30px;
            font-size: 1.2rem;
            font-weight: bold;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Estilo para botões de escolha */
        .botao-escolha {
            width: 100%;
            padding: 15px 20px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 12px;
            border: 2px solid #667eea;
            background: rgba(102, 126, 234, 0.1);
            color: white;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .botao-escolha:hover {
            background: rgba(102, 126, 234, 0.3);
            transform: scale(1.02);
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }
        
        /* Ocultar elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Estilo do container principal */
        .main-container {
            background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        /* Indicador de cena */
        .indicador-cena {
            color: rgba(255,255,255,0.5);
            text-align: center;
            font-size: 0.9rem;
            margin-top: 10px;
            font-family: 'Arial', sans-serif;
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .titulo-historia {
                font-size: 2.2rem;
            }
            
            .descricao-historia {
                font-size: 1rem;
                padding: 0 20px;
            }
            
            .pergunta-escolha {
                font-size: 1.2rem;
            }
            
            .stButton > button {
                font-size: 1rem;
                padding: 10px 20px;
            }
            
            .botao-escolha {
                font-size: 1rem;
                padding: 12px 15px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

# Função para exibir a imagem centralizada
def exibir_imagem(caminho_imagem):
    try:
        st.markdown(f"""
            <div class="imagem-container">
                <img src="{caminho_imagem}" class="imagem-historia" alt="Página da história">
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao carregar imagem: {e}")
        st.info(f"Verifique se a imagem '{caminho_imagem}' existe na pasta assets/images/")

# Função para inicializar o estado da sessão
def inicializar_estado():
    if "cena_atual" not in st.session_state:
        st.session_state.cena_atual = "inicio"
    if "historico" not in st.session_state:
        st.session_state.historico = []

# Função para navegar para uma cena
def ir_para_cena(cena_id):
    if cena_id in HISTORY:
        st.session_state.cena_atual = cena_id
        st.rerun()

# Função para reiniciar a história
def reiniciar_historia():
    st.session_state.cena_atual = "inicio"
    st.session_state.historico = []
    st.rerun()

# Aplicar CSS
aplicar_css()

# Inicializar estado da sessão
inicializar_estado()

# Container principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Obter cena atual
cena_id = st.session_state.cena_atual
cena = get_cena(cena_id)

if cena:
    # Tela inicial
    if cena["tipo"] == "inicio":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Título
            st.markdown(f'<h1 class="titulo-historia">{cena.get("titulo", "História em Quadrinhos")}</h1>', unsafe_allow_html=True)
            
            # Capa
            exibir_imagem(cena["imagem"])
            
            # Descrição
            if "descricao" in cena:
                st.markdown(f'<p class="descricao-historia">{cena["descricao"]}</p>', unsafe_allow_html=True)
            
            # Botão começar
            if st.button("🎯 Começar a História", key="btn_comecar", use_container_width=True):
                # Verifica se existe uma próxima cena
                proxima_cena = "cena_01"  # Primeira cena da história
                if proxima_cena in HISTORY:
                    ir_para_cena(proxima_cena)
                else:
                    st.error("Erro: Primeira cena da história não encontrada!")
    
    # Cena normal
    elif cena["tipo"] == "cena":
        # Exibir imagem
        exibir_imagem(cena["imagem"])
        
        # Indicador de cena
        st.markdown(f'<p class="indicador-cena">📖 {cena_id.replace("_", " ").title()}</p>', unsafe_allow_html=True)
        
        # Botão continuar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶ Continuar", key="btn_continuar", use_container_width=True):
                if "proxima" in cena:
                    ir_para_cena(cena["proxima"])
                else:
                    st.error("Erro: Próxima cena não definida!")
    
    # Cena de escolha
    elif cena["tipo"] == "escolha":
        # Exibir imagem
        exibir_imagem(cena["imagem"])
        
        # Pergunta
        st.markdown(f'<p class="pergunta-escolha">❓ {cena.get("pergunta", "O que fazer?")}</p>', unsafe_allow_html=True)
        
        # Botões de escolha
        col1, col2 = st.columns(2)
        
        opcoes = list(cena["opcoes"].items())
        if len(opcoes) >= 2:
            with col1:
                if st.button(f"🔹 {opcoes[0][0]}", key="escolha_1", use_container_width=True):
                    ir_para_cena(opcoes[0][1])
            
            with col2:
                if st.button(f"🔸 {opcoes[1][0]}", key="escolha_2", use_container_width=True):
                    ir_para_cena(opcoes[1][1])
        
        # Indicador de cena
        st.markdown(f'<p class="indicador-cena">📖 {cena_id.replace("_", " ").title()}</p>', unsafe_allow_html=True)
    
    # Final
    elif cena["tipo"] == "final":
        # Exibir imagem
        exibir_imagem(cena["imagem"])
        
        # Mensagem final
        if "mensagem" in cena:
            st.markdown(f'<p class="mensagem-final">🎬 {cena["mensagem"]}</p>', unsafe_allow_html=True)
        
        # Botão recomeçar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Recomeçar História", key="btn_reiniciar", use_container_width=True):
                reiniciar_historia()

# Fim do container principal
st.markdown('</div>', unsafe_allow_html=True)