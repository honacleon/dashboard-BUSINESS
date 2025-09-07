import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

class WhatsAppAlertsManager:
    @staticmethod
    def get_alert_types():
        return {
            "Críticos": {
                "Queda Conversões": {"threshold": "20%", "priority": "🔴", "status": "Ativo"},
                "CAC Elevado": {"threshold": "R$ 120", "priority": "🔴", "status": "Ativo"}, 
                "ROAS Baixo": {"threshold": "3.0", "priority": "🔴", "status": "Ativo"},
                "Meta em Risco": {"threshold": "80%", "priority": "🔴", "status": "Ativo"}
            },
            "Informativos": {
                "Relatório Diário": {"frequency": "Diário 09:00", "priority": "🟡", "status": "Ativo"},
                "Resumo Semanal": {"frequency": "Segunda 08:00", "priority": "🟡", "status": "Ativo"},
                "Metas Atingidas": {"trigger": "100% meta", "priority": "🟢", "status": "Ativo"},
                "Updates Campanha": {"frequency": "Real-time", "priority": "🔵", "status": "Ativo"}
            }
        }
    
    @staticmethod
    def generate_alert_history():
        alerts = []
        for i in range(20):
            date = datetime.now() - timedelta(days=random.randint(0, 30))
            alert_types = ["Conversões Baixas", "ROAS Crítico", "Meta Atingida", "CAC Elevado", "Relatório Diário"]
            priorities = ["🔴", "🟡", "🟢", "🔵"]
            
            alerts.append({
                "Data": date.strftime("%d/%m %H:%M"),
                "Tipo": random.choice(alert_types),
                "Prioridade": random.choice(priorities),
                "Mensagem": f"Alert {i+1} - Ação necessária",
                "Status": random.choice(["Enviado", "Pendente", "Erro"])
            })
        
        return pd.DataFrame(alerts)
    
    @staticmethod
    def generate_whatsapp_preview():
        return {
            "critical": """🚨 *AURUM BUSINESS - ALERTA CRÍTICO*
            
📉 *Queda nas Conversões Detectada*
• Redução: -23.5% nas últimas 4 horas
• Canal afetado: Google Ads
• Ação necessária: Revisar palavras-chave

📊 *Dados atuais:*
• Conversões hoje: 87 (-25 vs ontem)
• ROAS atual: 2.8x (meta: 3.2x)
• Budget restante: R$ 12.450

⚡ *Recomendações imediatas:*
1. Pausar campanhas com ROAS < 2.5x
2. Redistribuir budget para top performers
3. Verificar landing pages

🔗 Acesse: dashboard.aurum.com
👨‍💼 Equipe Aurum Analytics""",
            
            "daily": """📊 *AURUM BUSINESS - RELATÓRIO DIÁRIO*
*{date}*

💰 *Performance Geral:*
• Receita: R$ 45.780 (+12.3%)
• Conversões: 234 (+8.7%)  
• ROAS médio: 4.2x
• CAC médio: R$ 95

🎯 *Top Performers:*
1. Meta Ads: R$ 18.500 (ROAS 4.8x)
2. Google Ads: R$ 15.200 (ROAS 4.1x)
3. Orgânico: R$ 12.080 (ROAS 6.2x)

📈 *Destaques:*
• Melhor campanha: "Black Friday 2024"
• Produto top: Aurum Premium (45 vendas)
• Região destaque: São Paulo (+28%)

✅ *Status geral: EXCELENTE*
🔗 Dashboard: dashboard.aurum.com""",
            
            "goal": """🏆 *AURUM BUSINESS - META ATINGIDA!*

🎉 *PARABÉNS TIME!*
Meta mensal de *DEZEMBRO* foi atingida!

💎 *Números finais:*
• Meta: R$ 850.000
• Atingido: R$ 924.580 (108.8%)
• Superação: R$ 74.580

🥇 *Top Vendedores:*
1. Ana Silva: R$ 125.400
2. João Santos: R$ 98.750
3. Maria Costa: R$ 87.200

🚀 *Prêmios liberados:*
• Bônus equipe: R$ 15.000
• Viagem premiada: Confirmada
• Reconhecimento CEO: Agendado

👏 Comemorando juntos este sucesso!
🔗 dashboard.aurum.com"""
        }

def show_whatsapp_alerts_page(theme):
    st.markdown(f"""
    <div class="gold-header">
        <h1>WHATSAPP BUSINESS API - SISTEMA DE ALERTAS</h1>
        <h4>Alertas Inteligentes + Automação Premium</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Configuração", "📜 Histórico", "👀 Preview Mensagens", "📊 Analytics"])
    
    with tab1:
        st.markdown("### ⚙️ Configuração de Alertas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔴 Alertas Críticos")
            alert_types = WhatsAppAlertsManager.get_alert_types()
            
            for alert, config in alert_types["Críticos"].items():
                with st.expander(f"{config['priority']} {alert}"):
                    st.write(f"**Threshold:** {config['threshold']}")
                    st.write(f"**Status:** {config['status']}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.button(f"✅ Ativar", key=f"activate_{alert}")
                    with col_b:
                        st.button(f"⏸️ Pausar", key=f"pause_{alert}")
        
        with col2:
            st.markdown("#### 🟡 Alertas Informativos")
            
            for alert, config in alert_types["Informativos"].items():
                with st.expander(f"{config['priority']} {alert}"):
                    freq_key = "frequency" if "frequency" in config else "trigger"
                    st.write(f"**{freq_key.title()}:** {config[freq_key]}")
                    st.write(f"**Status:** {config['status']}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.button(f"✅ Ativar", key=f"activate_info_{alert}")
                    with col_b:
                        st.button(f"⏸️ Pausar", key=f"pause_info_{alert}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📞 Contatos de Emergência")
            st.text_input("Número Principal", value="+55 11 99999-8888")
            st.text_input("Backup Manager", value="+55 11 88888-9999")
        
        with col2:
            st.markdown("#### ⏰ Horários de Envio")
            st.time_input("Início", value=datetime.strptime("08:00", "%H:%M").time())
            st.time_input("Fim", value=datetime.strptime("22:00", "%H:%M").time())
        
        with col3:
            st.markdown("#### 🔄 Teste Manual")
            if st.button("📤 Enviar Teste", use_container_width=True):
                st.success("✅ Mensagem teste enviada!")
            if st.button("🔍 Verificar Status", use_container_width=True):
                st.info("🟢 WhatsApp API: Conectado")
    
    with tab2:
        st.markdown("### 📜 Histórico de Alertas")
        
        history_data = WhatsAppAlertsManager.generate_alert_history()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Enviados", "1,247", "↗️ 23")
        with col2:
            st.metric("Taxa Sucesso", "98.7%", "↗️ 0.3%")
        with col3:
            st.metric("Alertas Hoje", "15", "↗️ 5")
        with col4:
            st.metric("Críticos Hoje", "3", "↘️ 2")
        
        st.markdown("---")
        
        st.dataframe(
            history_data,
            use_container_width=True,
            column_config={
                "Prioridade": st.column_config.TextColumn("🚨 Prioridade"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Enviado", "Pendente", "Erro"]
                )
            }
        )
        
        # Gráfico de alertas por dia
        daily_alerts = history_data.groupby(history_data['Data'].str[:5]).size().reset_index()
        daily_alerts.columns = ['Dia', 'Quantidade']
        
        fig = go.Figure(data=[
            go.Bar(x=daily_alerts['Dia'], y=daily_alerts['Quantidade'],
                  marker_color=theme['primary'])
        ])
        fig.update_layout(
            title="📊 Alertas por Dia - Últimos 30 dias",
            template=theme['plotly_template'],
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 👀 Preview das Mensagens WhatsApp")
        
        preview_msgs = WhatsAppAlertsManager.generate_whatsapp_preview()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🔴 Alerta Crítico")
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; 
                       border-left: 5px solid #ff4444; font-family: monospace; color: white;">
            {preview_msgs['critical']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🟡 Relatório Diário")
            daily_msg = preview_msgs['daily'].format(date=datetime.now().strftime("%d/%m/%Y"))
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; 
                       border-left: 5px solid #ffbb33; font-family: monospace; color: white;">
            {daily_msg}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("#### 🟢 Meta Atingida")
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; 
                       border-left: 5px solid #00cc44; font-family: monospace; color: white;">
            {preview_msgs['goal']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Enviar Preview - Crítico", use_container_width=True):
                st.success("✅ Preview do alerta crítico enviado!")
        
        with col2:
            if st.button("📤 Enviar Preview - Diário", use_container_width=True):
                st.success("✅ Preview do relatório diário enviado!")
    
    with tab4:
        st.markdown("### 📊 Analytics de Alertas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza - Tipos de alerta
            alert_types_data = pd.DataFrame({
                'Tipo': ['Críticos', 'Informativos', 'Metas', 'Relatórios'],
                'Quantidade': [45, 120, 25, 85]
            })
            
            fig = go.Figure(data=[go.Pie(
                labels=alert_types_data['Tipo'],
                values=alert_types_data['Quantidade'],
                hole=0.4,
                marker_colors=[theme['primary'], theme['secondary'], theme['accent'], '#FFA500']
            )])
            fig.update_layout(title="📊 Distribuição por Tipo de Alerta")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de linha - Evolução dos alertas
            evolution_data = pd.DataFrame({
                'Dia': [f"Dia {i}" for i in range(1, 8)],
                'Críticos': [2, 5, 3, 8, 4, 6, 3],
                'Informativos': [15, 18, 12, 20, 16, 22, 19]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=evolution_data['Dia'], y=evolution_data['Críticos'],
                                   mode='lines+markers', name='Críticos', 
                                   line=dict(color='red', width=3)))
            fig.add_trace(go.Scatter(x=evolution_data['Dia'], y=evolution_data['Informativos'],
                                   mode='lines+markers', name='Informativos',
                                   line=dict(color=theme['secondary'], width=3)))
            fig.update_layout(title="📈 Evolução de Alertas - Última Semana")
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de performance
        st.markdown("#### 🎯 Performance dos Alertas")
        
        performance_data = pd.DataFrame({
            'Tipo de Alerta': ['Queda Conversões', 'ROAS Baixo', 'CAC Elevado', 'Meta Atingida', 'Relatório Diário'],
            'Enviados': [45, 32, 28, 12, 85],
            'Entregues': [44, 32, 27, 12, 84],
            'Taxa Entrega': ['97.8%', '100%', '96.4%', '100%', '98.8%'],
            'Ação Tomada': [38, 29, 24, 12, 68],
            'Taxa Ação': ['84.4%', '90.6%', '85.7%', '100%', '80.0%']
        })
        
        st.dataframe(
            performance_data,
            use_container_width=True,
            column_config={
                "Taxa Entrega": st.column_config.ProgressColumn("Taxa Entrega", max_value=100),
                "Taxa Ação": st.column_config.ProgressColumn("Taxa Ação", max_value=100)
            }
        )