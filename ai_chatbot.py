"""
AURUM AI CHATBOT - Sistema Híbrido com IA Real + Fallback Inteligente
Módulo completo para chatbot com DeepSeek API + Dados Reais do Dashboard
"""

import streamlit as st
from datetime import datetime
import json
import re
import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# ============================================================================
# CONFIGURAÇÃO MULTI-SOURCE: Streamlit Secrets > Variáveis de Ambiente > .env
# ============================================================================

def get_config(key, default=None):
    """
    Obtém configuração de múltiplas fontes na ordem:
    1. Streamlit Secrets (st.secrets)
    2. Variáveis de ambiente (os.environ)
    3. Arquivo .env (via dotenv)

    Args:
        key: Chave da configuração
        default: Valor padrão se não encontrar

    Returns:
        Valor da configuração ou default
    """
    # 1. Tentar Streamlit Secrets (para Streamlit Cloud/GitHub)
    try:
        if hasattr(st, 'secrets') and 'deepseek' in st.secrets:
            secret_key = key.replace("DEEPSEEK_", "").lower()
            if secret_key in st.secrets['deepseek']:
                value = st.secrets['deepseek'][secret_key]
                print(f"[OK] {key} carregado de Streamlit Secrets")
                return value
    except Exception:
        pass

    # 2. Tentar variáveis de ambiente do sistema
    env_value = os.getenv(key)
    if env_value:
        print(f"[OK] {key} carregado de variavel de ambiente")
        return env_value

    # 3. Usar default
    if default:
        print(f"[INFO] {key} usando valor padrao")
    return default

# Configurações da API DeepSeek
DEEPSEEK_API_KEY = get_config("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = get_config("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = get_config("DEEPSEEK_MODEL", "deepseek-chat")

# Converter tipos numéricos
try:
    DEEPSEEK_MAX_TOKENS = int(get_config("DEEPSEEK_MAX_TOKENS", "2000"))
    DEEPSEEK_TEMPERATURE = float(get_config("DEEPSEEK_TEMPERATURE", "0.7"))
except (ValueError, TypeError):
    DEEPSEEK_MAX_TOKENS = 2000
    DEEPSEEK_TEMPERATURE = 0.7

# Verificar se API está disponível
DEEPSEEK_AVAILABLE = bool(DEEPSEEK_API_KEY and DEEPSEEK_API_KEY.startswith("sk-"))

if DEEPSEEK_AVAILABLE:
    print(f"[OK] DeepSeek API configurada: {DEEPSEEK_MODEL}")
else:
    print("[INFO] DeepSeek API nao configurada. Usando modo simulado.")


class AurumAIChatbot:
    """Gerenciador principal do chatbot com IA"""

    def __init__(self, api_key=None, use_api=True, dashboard_data=None):
        """
        Inicializa o chatbot

        Args:
            api_key: Chave da API do DeepSeek (opcional, usa .env se não fornecida)
            use_api: Se True, tenta usar API real. Se False, usa apenas simulação
            dashboard_data: Dados reais do dashboard para contexto (dict)
        """
        # Usar chave do .env se não fornecida
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.use_api = use_api and DEEPSEEK_AVAILABLE and self.api_key
        self.dashboard_data = dashboard_data or {}

        if self.use_api:
            print(f"[OK] DeepSeek API ativa! Modelo: {DEEPSEEK_MODEL}")
        else:
            print("[INFO] Modo simulado ativo")

    def get_ai_response(self, user_message, conversation_history=None):
        """
        Obtém resposta da IA (real ou simulada)

        Args:
            user_message: Mensagem do usuário
            conversation_history: Histórico de conversas anteriores

        Returns:
            dict com 'text' (resposta) e 'source' ('api' ou 'simulated')
        """
        if self.use_api:
            try:
                return self._get_api_response(user_message, conversation_history)
            except Exception as e:
                print(f"[WARNING] Erro na API: {e}. Usando fallback simulado.")
                return self._get_simulated_response(user_message)
        else:
            return self._get_simulated_response(user_message)

    def _get_api_response(self, user_message, conversation_history=None):
        """Obtém resposta da API real do DeepSeek"""

        # Preparar mensagens
        messages = []

        # Adicionar system prompt como primeira mensagem
        messages.append({
            "role": "system",
            "content": self._get_system_prompt()
        })

        # Adicionar histórico se existir (últimas 5 mensagens)
        if conversation_history:
            for msg in conversation_history[-5:]:
                messages.append({
                    "role": msg["type"] if msg["type"] == "user" else "assistant",
                    "content": msg["message"]
                })

        # Adicionar mensagem atual
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Chamar API DeepSeek
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "max_tokens": DEEPSEEK_MAX_TOKENS,
                "temperature": DEEPSEEK_TEMPERATURE,
                "stream": False
            }

            response = requests.post(
                f"{DEEPSEEK_API_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "text": data["choices"][0]["message"]["content"],
                    "source": "api",
                    "model": data.get("model", DEEPSEEK_MODEL),
                    "tokens": data.get("usage", {}).get("total_tokens", 0)
                }
            else:
                print(f"[ERROR] Erro API DeepSeek: {response.status_code} - {response.text}")
                raise Exception(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"[ERROR] Erro ao chamar DeepSeek API: {e}")
            raise

    def _get_system_prompt(self):
        """Retorna o prompt do sistema que define o comportamento do chatbot"""

        base_prompt = """Você é o Aurum IA Assistant, um assistente inteligente especializado em análise de dados de negócios e business intelligence.

**Seu Papel:**
- Ajudar executivos e gerentes a interpretar métricas de negócios
- Fornecer insights acionáveis baseados em dados REAIS
- Explicar KPIs de forma clara e concisa
- Recomendar ações estratégicas baseadas nos dados

**Estilo de Comunicação:**
- Seja conciso e direto ao ponto
- Use emojis ocasionalmente para tornar a conversa mais amigável
- Formate respostas com markdown (negrito, listas, etc.)
- Priorize insights práticos sobre teoria
- Use exemplos concretos quando relevante

**Contexto do Dashboard Aurum:**
- Empresa: Aurum Business
- Foco: Marketing digital, vendas e operações
- Métricas principais: CAC, LTV, ROAS, conversões, ROI
- Canais: Google Ads, Meta Ads, Orgânico, Email, WhatsApp

**Importante:**
- Seja sempre profissional mas acessível
- Admita quando não tiver certeza
- Peça esclarecimentos se a pergunta for vaga
- Ofereça seguir explorando tópicos relacionados
- SEMPRE use os dados reais fornecidos abaixo quando disponíveis"""

        # Adicionar dados reais do dashboard se disponíveis
        if self.dashboard_data:
            base_prompt += "\n\n**📊 DADOS REAIS DO DASHBOARD (USE ESTES DADOS PARA SUAS RESPOSTAS):**\n"

            for key, value in self.dashboard_data.items():
                if isinstance(value, dict):
                    base_prompt += f"\n**{key}:**\n"
                    for subkey, subvalue in value.items():
                        base_prompt += f"  - {subkey}: {subvalue}\n"
                else:
                    base_prompt += f"- **{key}:** {value}\n"

        return base_prompt

    def _get_simulated_response(self, user_message):
        """
        Gera resposta simulada inteligente baseada em keywords
        (Muito melhor que a versão atual do chatbot!)
        """
        message_lower = user_message.lower()

        # Banco de respostas inteligentes por categoria
        responses = self._get_response_database()

        # Detectar categoria da pergunta
        for category, data in responses.items():
            if any(keyword in message_lower for keyword in data["keywords"]):
                return {
                    "text": data["response"],
                    "source": "simulated",
                    "category": category
                }

        # Resposta padrão se não encontrar categoria
        return {
            "text": self._get_default_response(user_message),
            "source": "simulated",
            "category": "general"
        }

    def _get_response_database(self):
        """Banco de respostas inteligentes por categoria"""
        return {
            "tendencias_crescimento": {
                "keywords": ["tendência", "crescimento", "evolução", "progresso", "aumento", "melhoria"],
                "response": """📈 **Análise de Tendências - Insights Estratégicos**

🔥 **Principais Tendências Identificadas:**
• **Crescimento orgânico de 31%** - Maior dos últimos 2 anos
• **Mobile commerce:** +67% de participação
• **Retenção de clientes:** Melhoria de 23%

📊 **Padrões Sazonais Detectados:**
• Picos de conversão: Sextas-feiras (14h-16h) e fins de semana
• Q4 historicamente 40% superior ao Q3
• Black Friday: ROI médio de 8.5x

🎯 **Recomendações Imediatas:**
1. Ampliar investimento em mobile em 25%
2. Implementar programa de fidelidade premium
3. Preparar campanha Q4 com budget +50%

💡 **Quer explorar alguma tendência específica?**"""
            },

            "roi_otimizacao": {
                "keywords": ["roi", "retorno", "otimização", "otimizar", "melhorar", "performance"],
                "response": """💰 **Estratégias de Otimização de ROI**

🎯 **Oportunidades Imediatas (ROI +40%):**
1. **Google Ads:** Focar em long-tail keywords (CPC -60%)
2. **Facebook:** Lookalike audiences 1% (CVR +35%)
3. **Email Marketing:** Segmentação comportamental avançada

📊 **Performance Atual vs Potencial:**
• ROI Geral: **340%** (excelente!)
• Melhor canal: Google Ads (ROI 420%)
• **Oportunidade:** Instagram Ads (+150% potencial não explorado)

🚀 **Plano de Ação 30 Dias:**
✓ Realocar 30% do budget para canais high-ROI
✓ A/B test de criativos semanalmente
✓ Implementar pixel tracking avançado
✓ Revisar audiences para eliminar overlap

📈 **Ganho projetado:** +R$ 180K nos próximos 90 dias"""
            },

            "previsao_futuro": {
                "keywords": ["previsão", "futuro", "próximos", "meses", "trimestre", "previsivel"],
                "response": """🔮 **Previsões Baseadas em IA - Próximos 3 Meses**

📈 **Projeções de Receita (algoritmo preditivo):**
• **Mês 1:** R$ 1.35M (+12% vs atual)
• **Mês 2:** R$ 1.48M (+23% crescimento)
• **Mês 3:** R$ 1.62M (+35% total)
• **Total Trimestre:** R$ 4.45M

🎯 **Fatores de Crescimento Identificados:**
• Campanha Black Friday: +R$ 480K esperados
• Lançamento novos produtos: +R$ 220K
• Otimizações UX: +R$ 150K incrementais

⚠️ **Riscos Monitorados pela IA:**
• Sazonalidade dezembro: -8% histórico
• Concorrência: Possível impacto de 5-12%
• **Cenário conservador:** R$ 3.9M (ainda +18%)

💡 **Recomendação:** Preparar campanha agressiva para compensar sazonalidade"""
            },

            "gargalos_problemas": {
                "keywords": ["gargalo", "problema", "dificuldade", "desafio", "obstáculo", "lentidão"],
                "response": """🔍 **Diagnóstico de Gargalos Operacionais**

⚠️ **Gargalos Críticos Identificados:**

**1. Tempo de Resposta Suporte**
• Atual: 4.2h (meta: <2h)
• Impacto: NPS -12 pontos
• **Solução:** Chatbot para 40% dos tickets

**2. Processamento de Pedidos**
• 23% com atraso de processamento
• Receita perdida: ~R$ 47K/mês
• **Solução:** Automação fulfillment (+30% eficiência)

**3. Capacidade de Atendimento**
• Equipe em 89% de ocupação (zona crítica!)
• Churn: +3.4% por insatisfação
• **Solução:** Contratar 2 novos atendentes

📊 **Priorização por Impacto:**
1. 🔴 **URGENTE:** Chatbot + automação (ROI 450%)
2. 🟡 **ALTO:** Contratação equipe (payback 4 meses)
3. 🟢 **MÉDIO:** Otimização processos internos

💰 **Custo vs Benefício:** Investir R$ 35K resolve 85% dos gargalos"""
            },

            "clientes_cac_ltv": {
                "keywords": ["cliente", "cac", "ltv", "aquisição", "custo", "lifetime", "valor"],
                "response": """👥 **Análise Avançada de Clientes - Economics**

💎 **Métricas de Aquisição & Retenção:**
• **CAC Médio:** R$ 127 (↓8% vs trimestre anterior)
• **LTV Médio:** R$ 890 (↑15% crescimento)
• **Ratio LTV/CAC:** **7.01x** (excepcional! 🎉)

📊 **Segmentação por Valor do Cliente:**

**Tier Premium (20% clientes):**
• LTV: R$ 1,840
• CAC: R$ 195
• Margem: 84%

**Tier Standard (60% clientes):**
• LTV: R$ 720
• CAC: R$ 115
• Margem: 68%

**Tier Basic (20% clientes):**
• LTV: R$ 340
• CAC: R$ 98
• Margem: 52%

🚀 **Oportunidades de Crescimento:**
1. **Upsell Standard → Premium:** +R$ 280K potencial/ano
2. **Reativação churned:** 18% win-back rate histórico
3. **Referral program:** CPA 65% menor que paid ads

🎯 **Ação recomendada:** Focar em adquirir mais clientes Premium (melhor LTV/CAC)"""
            },

            "conversoes_taxa": {
                "keywords": ["conversão", "taxa", "cvr", "converter", "leads", "vendas"],
                "response": """📊 **Análise Profunda de Conversões**

🎯 **Taxa de Conversão Atual:**
• **Geral:** 8.7% (↑1.2pp vs mês anterior)
• **Landing Pages:** 12.3% (excelente!)
• **Checkout:** 68% (oportunidade de melhoria)

📈 **Performance por Canal:**
1. **Email Marketing:** 15.2% CVR (💎 melhor)
2. **Google Ads:** 9.8% CVR
3. **Meta Ads:** 7.4% CVR
4. **Orgânico:** 11.1% CVR

🔥 **Oportunidades de Otimização:**

**Quick Wins (impacto imediato):**
• Simplificar checkout: +3.5% CVR estimado
• A/B test CTAs: +1.8% CVR histórico
• Otimizar mobile: +4.2% CVR potencial

**Médio Prazo:**
• Implementar social proof: +12% CVR
• Personalização por segmento: +18% CVR
• Urgency triggers: +8% CVR

💰 **Impacto Financeiro:** Melhorar CVR em 3pp = +R$ 95K/mês

🚀 **Prioridade #1:** Otimizar mobile (67% do tráfego!)"""
            },

            "campanhas_marketing": {
                "keywords": ["campanha", "marketing", "anúncio", "ad", "google", "facebook", "meta"],
                "response": """🚀 **Análise de Campanhas de Marketing**

📊 **Performance Atual (Últimos 30 dias):**

**Google Ads:**
• Spend: R$ 45.2K
• ROAS: 4.2x (↑12% vs mês anterior)
• Conversões: 1,248
• **Melhor campanha:** Brand Search (ROAS 8.7x)

**Meta Ads:**
• Spend: R$ 38.5K
• ROAS: 4.6x (↑8%)
• Conversões: 1,089
• **Melhor campanha:** Lookalike 1% (ROAS 6.2x)

🎯 **Recomendações por Canal:**

**Google Ads:**
✓ Escalar Brand Search (+50% budget)
✓ Pausar generic keywords (ROAS <2.5x)
✓ Testar Smart Bidding para Shopping

**Meta Ads:**
✓ Aumentar budget Lookalike audiences
✓ Testar vídeos curtos (15s performing +45%)
✓ Retargeting 30 dias (ROAS 7.8x!)

💡 **Realocação Sugerida:** Mover R$ 8K de low performers para top 3 campanhas

📈 **Ganho esperado:** +R$ 45K revenue extra/mês"""
            },

            "equipe_vendas": {
                "keywords": ["equipe", "vendedor", "time", "vendas", "performance", "colaborador"],
                "response": """👥 **Análise de Performance da Equipe**

🏆 **Top Performers (Últimos 30 dias):**

**1. Ana Silva** - 128% quota
• Receita: R$ 125.4K
• Deals fechados: 18
• Ticket médio: R$ 6,966
• **Segredo:** Excelente follow-up (98% rate)

**2. João Santos** - 108% quota
• Receita: R$ 98.7K
• Deals fechados: 15
• Win rate: 34% (acima da média)

**3. Maria Costa** - 142% quota (⭐ destaque!)
• Receita: R$ 87.2K
• Cycle time: 14 dias (↓35% vs média)

📊 **Métricas da Equipe:**
• **Quota Attainment Médio:** 96.8%
• **Win Rate:** 28.7% (↑3.2pp)
• **Cycle Time Médio:** 18.5 dias
• **Pipeline Health:** 87/100 (bom!)

⚠️ **Áreas de Atenção:**
• 3 vendedores abaixo de 80% quota
• Ciclo de vendas aumentou +2 dias
• Follow-up rate em 76% (meta: 90%)

🎯 **Ações Recomendadas:**
1. Programa de mentoria peer-to-peer
2. Coaching para vendedores <80%
3. Automação de follow-ups
4. Incentivos para reduzir cycle time

💰 **Potencial:** Atingindo 100% quota = +R$ 78K/mês"""
            }
        }

    def _get_default_response(self, user_message):
        """Resposta padrão inteligente quando não identifica categoria"""
        return f"""🤖 **Aurum IA Assistant** - Análise Personalizada

Obrigado pela sua pergunta! Posso fornecer insights específicos sobre diversos aspectos do seu negócio.

📊 **Áreas de Especialidade:**

**Marketing & Vendas:**
• Performance de campanhas (Google Ads, Meta Ads)
• Otimização de ROI e ROAS
• Análise de conversões e funis

**Métricas & Analytics:**
• CAC vs LTV e economics de clientes
• Previsões e tendências futuras
• KPIs e benchmarks do setor

**Operações:**
• Diagnóstico de gargalos
• Performance da equipe
• Otimização de processos

💡 **Perguntas sugeridas:**
• "Como está a performance das campanhas?"
• "Quais são os principais gargalos operacionais?"
• "Qual a previsão de receita para os próximos meses?"
• "Como otimizar o ROI de marketing?"

🎯 **Como posso ajudar você especificamente?**"""

    def get_suggested_questions(self):
        """Retorna lista de perguntas sugeridas contextuais"""
        return [
            {
                "label": "📈 Análise de Tendências",
                "question": "Quais são as principais tendências de crescimento identificadas nos últimos 6 meses?"
            },
            {
                "label": "💰 Otimização de ROI",
                "question": "Como posso otimizar o ROI das campanhas de marketing digital?"
            },
            {
                "label": "🔮 Previsões",
                "question": "Qual é a previsão de receita para os próximos 3 meses?"
            },
            {
                "label": "🔍 Diagnóstico",
                "question": "Quais são os principais gargalos operacionais que devo resolver?"
            },
            {
                "label": "👥 Performance Equipe",
                "question": "Como está a performance da equipe de vendas?"
            },
            {
                "label": "📊 CAC vs LTV",
                "question": "Como interpretar meu CAC de R$ 127 e LTV de R$ 890?"
            }
        ]


def initialize_chat_history():
    """Inicializa o histórico de chat"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def show_ai_chatbot_page(theme, api_key=None, dashboard_data=None):
    """
    Renderiza a página do chatbot com IA

    Args:
        theme: Dicionário com configurações do tema
        api_key: Chave da API DeepSeek (opcional, usa .env se não fornecida)
        dashboard_data: Dados reais do dashboard (dict)
    """

    # Inicializar chatbot (sempre tenta usar API do .env)
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = AurumAIChatbot(
            api_key=api_key,  # Usa .env se None
            use_api=True,
            dashboard_data=dashboard_data
        )
    elif dashboard_data:
        # Atualizar dados do dashboard se mudarem
        st.session_state.chatbot.dashboard_data = dashboard_data

    # Inicializar histórico
    initialize_chat_history()

    # CSS customizado
    st.markdown(f"""
    <style>
    .chatbot-header {{
        background: {theme['gradient_main']};
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid {theme['border']};
        box-shadow: {theme['shadow']};
        text-align: center;
    }}

    .message-user {{
        background: {theme['gradient_accent']};
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0 10px 80px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        word-wrap: break-word;
        animation: slideInRight 0.3s ease;
    }}

    .message-bot {{
        background: {theme['accent']};
        color: {theme['text']};
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 80px 10px 0;
        border: 1px solid {theme['border']};
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        word-wrap: break-word;
        animation: slideInLeft 0.3s ease;
    }}

    .message-timestamp {{
        font-size: 11px;
        opacity: 0.7;
        margin-top: 8px;
        font-style: italic;
    }}

    .api-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: bold;
        margin-left: 10px;
    }}

    .api-badge-real {{
        background: linear-gradient(135deg, #00ff88, #00cc66);
        color: #000;
    }}

    .api-badge-simulated {{
        background: linear-gradient(135deg, #ffd700, #ffaa00);
        color: #000;
    }}

    .bot-status {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        padding: 12px;
        background: {theme['glass_effect']};
        border-radius: 10px;
        border: 1px solid {theme['border']};
    }}

    .status-indicator {{
        width: 10px;
        height: 10px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; box-shadow: 0 0 10px #00ff00; }}
        50% {{ opacity: 0.5; box-shadow: 0 0 20px #00ff00; }}
    }}

    @keyframes slideInRight {{
        from {{ transform: translateX(50px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    @keyframes slideInLeft {{
        from {{ transform: translateX(-50px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    .suggested-questions {{
        background: {theme['glass_effect']};
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid {theme['border']};
    }}

    .typing-indicator {{
        display: flex;
        align-items: center;
        margin: 10px 80px 10px 0;
        color: {theme['primary']};
        font-style: italic;
        padding: 10px;
    }}

    .typing-dot {{
        width: 8px;
        height: 8px;
        background: {theme['primary']};
        border-radius: 50%;
        margin: 0 3px;
        animation: typing 1.4s infinite ease-in-out;
    }}

    .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}

    @keyframes typing {{
        0%, 80%, 100% {{ transform: scale(0); opacity: 0.5; }}
        40% {{ transform: scale(1); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # Header
    api_status = "IA Real Ativa" if st.session_state.chatbot.use_api else "Modo Simulado"
    api_color = "#00ff88" if st.session_state.chatbot.use_api else "#ffd700"

    st.markdown(f"""
    <div class="chatbot-header">
        <h1 style="margin: 0; color: white;">🤖 Aurum IA Assistant</h1>
        <p style="margin: 10px 0 0 0; color: white; opacity: 0.9;">
            Assistente inteligente para análise de dados e insights de negócios
            <span style="background: {api_color}; color: #000; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold; margin-left: 10px;">
                {api_status}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Status do bot
    st.markdown(f"""
    <div class="bot-status">
        <div class="status-indicator"></div>
        <span style="color: {theme['primary']}; font-weight: bold;">
            Aurum IA está online e pronto para ajudar
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Renderizar histórico de mensagens
    for msg in st.session_state.chat_history:
        source_badge = ""
        if msg.get("source"):
            if msg["source"] == "api":
                source_badge = '<span class="api-badge api-badge-real">🤖 IA Real</span>'
            elif msg["source"] == "simulated":
                source_badge = '<span class="api-badge api-badge-simulated">💡 Simulado</span>'

        if msg["type"] == "user":
            st.markdown(f"""
            <div class="message-user">
                {msg['message']}
                <div class="message-timestamp">Você • {msg['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-bot">
                {msg['message']}
                <div class="message-timestamp">Aurum IA • {msg['timestamp']} {source_badge}</div>
            </div>
            """, unsafe_allow_html=True)

    # Mostrar indicador de digitação se necessário
    if st.session_state.get('is_typing', False):
        st.markdown("""
        <div class="typing-indicator">
            <span>Aurum IA está pensando</span>
            <div style="display: flex; margin-left: 10px;">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Perguntas sugeridas
    st.markdown(f"""
    <div class="suggested-questions">
        <h4 style="margin-top: 0; color: {theme['primary']};">💡 Perguntas Sugeridas</h4>
    </div>
    """, unsafe_allow_html=True)

    # Botões de perguntas sugeridas
    suggested = st.session_state.chatbot.get_suggested_questions()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(suggested[0]["label"], use_container_width=True, key="sug_0"):
            handle_user_message(suggested[0]["question"])

        if st.button(suggested[3]["label"], use_container_width=True, key="sug_3"):
            handle_user_message(suggested[3]["question"])

    with col2:
        if st.button(suggested[1]["label"], use_container_width=True, key="sug_1"):
            handle_user_message(suggested[1]["question"])

        if st.button(suggested[4]["label"], use_container_width=True, key="sug_4"):
            handle_user_message(suggested[4]["question"])

    with col3:
        if st.button(suggested[2]["label"], use_container_width=True, key="sug_2"):
            handle_user_message(suggested[2]["question"])

        if st.button(suggested[5]["label"], use_container_width=True, key="sug_5"):
            handle_user_message(suggested[5]["question"])

    # Input de mensagem
    st.markdown("---")

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])

        with col1:
            user_input = st.text_input(
                "",
                placeholder="💬 Digite sua pergunta sobre analytics, métricas ou estratégias...",
                label_visibility="collapsed"
            )

        with col2:
            send_button = st.form_submit_button("Enviar 🚀", use_container_width=True, type="primary")

        if send_button and user_input.strip():
            handle_user_message(user_input.strip())

    # Configurações avançadas (colapsável)
    with st.expander("⚙️ Configurações Avançadas"):
        st.markdown("### 🔧 Configurações do Chatbot")

        # Status da API
        if st.session_state.chatbot.use_api:
            st.success(f"✅ **IA Real Ativa** - DeepSeek ({DEEPSEEK_MODEL})")
            st.info(f"📊 **Dados do Dashboard:** {'✅ Conectado' if dashboard_data else '⚠️ Não disponíveis'}")
        else:
            st.warning("⚠️ **Modo Simulado** - Configure API DeepSeek no arquivo .env")

        # Opção para adicionar/atualizar API key
        new_api_key = st.text_input(
            "🔑 Chave da API DeepSeek",
            value="",
            type="password",
            placeholder="sk-xxxxxxxxxxxxxxxxxx",
            help="Cole sua chave sk-xxx do DeepSeek para ativar IA real"
        )

        if st.button("💾 Atualizar Configuração"):
            if new_api_key and new_api_key.startswith("sk-"):
                st.session_state.chatbot = AurumAIChatbot(
                    api_key=new_api_key,
                    use_api=True,
                    dashboard_data=dashboard_data
                )
                st.success("✅ Configuração atualizada! Recarregue a página.")
                st.rerun()
            else:
                st.error("❌ Chave inválida. Deve começar com 'sk-'")

        # Limpar histórico
        if st.button("🗑️ Limpar Histórico de Chat"):
            st.session_state.chat_history = []
            initialize_chat_history()
            st.success("✅ Histórico limpo!")
            st.rerun()

        # Estatísticas
        st.markdown("---")
        st.markdown("### 📊 Estatísticas da Sessão")

        total_messages = len(st.session_state.chat_history)
        user_messages = len([m for m in st.session_state.chat_history if m["type"] == "user"])
        bot_messages = len([m for m in st.session_state.chat_history if m["type"] == "bot"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Mensagens Totais", total_messages)

        with col2:
            st.metric("Suas Perguntas", user_messages)

        with col3:
            st.metric("Respostas da IA", bot_messages)


def handle_user_message(message):
    """
    Processa mensagem do usuário e obtém resposta da IA

    Args:
        message: Mensagem enviada pelo usuário
    """
    current_time = datetime.now().strftime("%H:%M")

    # Adicionar mensagem do usuário ao histórico
    st.session_state.chat_history.append({
        "type": "user",
        "message": message,
        "timestamp": current_time
    })

    # Indicar que está "digitando"
    st.session_state.is_typing = True

    # Obter resposta da IA
    response = st.session_state.chatbot.get_ai_response(
        message,
        conversation_history=st.session_state.chat_history
    )

    # Adicionar resposta do bot ao histórico
    st.session_state.chat_history.append({
        "type": "bot",
        "message": response["text"],
        "timestamp": current_time,
        "source": response["source"]
    })

    # Remover indicador de digitação
    st.session_state.is_typing = False

    # Recarregar para mostrar nova mensagem
    st.rerun()

