import streamlit as st
from fpdf import FPDF
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import base64
import io
import pandas as pd
import random

class AurumReportPDF(FPDF):
    def __init__(self, report_type="Executivo"):
        super().__init__()
        self.report_type = report_type
        
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(25, 25, 112)
        self.cell(0, 10, f'AURUM BUSINESS - RELATÓRIO {self.report_type.upper()}', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()} | Aurum Business Dashboard | Confidencial', 0, 0, 'C')
    
    def add_executive_summary(self, kpis):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'RESUMO EXECUTIVO', 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 11)
        
        # KPIs em grid 2x4
        kpi_items = list(kpis.items())
        for i in range(0, len(kpi_items), 2):
            if i < len(kpi_items):
                self.cell(95, 8, f"> {kpi_items[i][0]}: {kpi_items[i][1]}", 1, 0, 'L')
            if i+1 < len(kpi_items):
                self.cell(95, 8, f"> {kpi_items[i+1][0]}: {kpi_items[i+1][1]}", 1, 1, 'L')
            else:
                self.ln()
        
        self.ln(10)
    
    def add_analysis_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(25, 25, 112)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(3)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        
        # Quebra o texto em linhas
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                self.cell(0, 6, line.strip(), 0, 1, 'L')
        
        self.ln(8)
    
    def add_recommendations(self, recommendations):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(25, 25, 112)
        self.cell(0, 10, 'RECOMENDACOES ESTRATEGICAS', 0, 1, 'L')
        self.ln(5)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        
        for i, rec in enumerate(recommendations, 1):
            self.cell(0, 6, f"{i}. {rec}", 0, 1, 'L')
        
        self.ln(10)

class PDFReportManager:
    @staticmethod
    def generate_executive_report():
        kpis = {
            "Receita Total": f"R$ {random.uniform(2500000, 5000000):,.0f}",
            "Crescimento": f"+{random.uniform(8, 25):.1f}%", 
            "ROI Médio": f"{random.uniform(3.2, 4.8):.1f}x",
            "Conversões": f"{random.randint(1200, 3500):,}",
            "CAC": f"R$ {random.uniform(85, 120):.0f}",
            "LTV": f"R$ {random.uniform(850, 1200):.0f}",
            "Ticket Médio": f"R$ {random.uniform(340, 520):.0f}",
            "NPS": f"{random.randint(65, 85)}"
        }
        
        pdf = AurumReportPDF("Executivo Mensal")
        pdf.add_page()
        
        pdf.add_executive_summary(kpis)
        
        analysis = """Performance excepcional no mes de dezembro, com crescimento consistente em todos os KPIs principais.
Destaque para o aumento de 18% nas conversoes organicas e otimizacao do CAC em 12%.
O investimento em Meta Ads apresentou ROAS superior a 4.2x, superando a meta estabelecida.
Regiao Sul apresentou crescimento de 25%, impulsionada pela campanha de fim de ano."""
        
        pdf.add_analysis_section("ANALISE DE PERFORMANCE", analysis)
        
        recommendations = [
            "Aumentar budget em campanhas com ROAS acima de 4.0x",
            "Implementar automacao avancada para lead scoring",
            "Expandir atuacao na regiao Sul devido ao alto crescimento",
            "Testar novos criativos para audiencia 25-34 anos",
            "Revisar jornada do cliente para reduzir CAC em 8%"
        ]
        
        pdf.add_recommendations(recommendations)
        
        return bytes(pdf.output(dest='S'))
    
    @staticmethod
    def generate_marketing_report():
        pdf = AurumReportPDF("Marketing Semanal")
        pdf.add_page()
        
        marketing_kpis = {
            "Spend Total": "R$ 125.400",
            "Impressões": "2.8M",
            "Clicks": "84.750",
            "CTR Médio": "3.02%",
            "ROAS Google": "4.1x",
            "ROAS Meta": "4.6x"
        }
        
        pdf.add_executive_summary(marketing_kpis)
        
        google_analysis = """Google Ads Performance:
> Campanhas de marca apresentaram CTR de 4.8%
> Palavras-chave long-tail geraram 32% das conversoes
> Smart Bidding otimizou CPAs em 15%
> Audiencias similares aumentaram reach em 28%"""
        
        pdf.add_analysis_section("GOOGLE ADS INSIGHTS", google_analysis)
        
        meta_analysis = """Meta Ads Performance:
> Criativos em video superaram imagens em 45%
> Lookalike 1% apresentou melhor ROAS (5.2x)
> Campaign Budget Optimization reduziu CPC em 18%
> Stories ads geraram 22% mais engajamento"""
        
        pdf.add_analysis_section("META ADS INSIGHTS", meta_analysis)
        
        recommendations = [
            "Realocar 20% do budget para campanhas de video",
            "Expandir audiencias lookalike para 2% e 3%",
            "Implementar retargeting baseado em eventos personalizados",
            "Testar Facebook Shops para produtos premium"
        ]
        
        pdf.add_recommendations(recommendations)
        
        return bytes(pdf.output(dest='S'))
    
    @staticmethod
    def generate_operational_report():
        pdf = AurumReportPDF("Operacional")
        pdf.add_page()
        
        operational_kpis = {
            "Pipeline": "R$ 1.24M",
            "Win Rate": "28.7%",
            "Ciclo Médio": "18.5 dias",
            "Vendedores Ativos": "12",
            "Meta Mensal": "96.8%",
            "Produtividade": "+14.2%"
        }
        
        pdf.add_executive_summary(operational_kpis)
        
        sales_analysis = """Analise do Pipeline de Vendas:
> 45% das oportunidades estao em negociacao avancada
> Produtos premium representam 62% do pipeline
> Regiao Sudeste concentra 55% das oportunidades
> Taxa de conversao aumentou 8% comparado ao mes anterior
> Vendedores seniores mantem cycle time 25% menor"""
        
        pdf.add_analysis_section("ANALISE DE VENDAS", sales_analysis)
        
        team_analysis = """Performance da Equipe:
> Ana Silva lidera com 108% da meta mensal
> Equipe SP superou meta em 12%
> 3 vendedores necessitam coaching adicional
> NPS interno da equipe: 82 pontos
> Turnover reduzido em 30% vs ano anterior"""
        
        pdf.add_analysis_section("PERFORMANCE DA EQUIPE", team_analysis)
        
        recommendations = [
            "Intensificar follow-up em oportunidades >R$ 50k",
            "Implementar programa de mentoria peer-to-peer",
            "Criar incentivos para cross-selling",
            "Automatizar relatorios de produtividade individual"
        ]
        
        pdf.add_recommendations(recommendations)
        
        return bytes(pdf.output(dest='S'))

def show_pdf_reports_page(theme):
    st.markdown(f"""
    <div class="gold-header">
        <h1>RELATÓRIOS PDF AUTOMATIZADOS</h1>
        <h4>Geração Premium + Templates Personalizáveis</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Geração", "📅 Agendamentos", "🎨 Templates", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 📊 Geração de Relatórios")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 📈 Relatório Executivo Mensal
            **Conteúdo:**
            - Capa personalizada Aurum
            - Resumo executivo (1 página) 
            - KPIs principais com gráficos
            - Análise de performance
            - Recomendações estratégicas
            - Próximos passos
            """)
            
            if st.button("📥 Gerar Executivo", use_container_width=True):
                with st.spinner("Gerando relatório executivo..."):
                    pdf_bytes = PDFReportManager.generate_executive_report()
                    st.success("✅ Relatório executivo gerado!")
                    
                    st.download_button(
                        label="📄 Download PDF Executivo",
                        data=pdf_bytes,
                        file_name=f"Aurum_Business_Executivo_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col2:
            st.markdown("""
            #### 📱 Relatório Marketing Semanal
            **Conteúdo:**
            - Performance Google Ads
            - Performance Meta Ads
            - ROI por canal
            - Insights e otimizações
            - Comparativos semanais
            - Recomendações táticas
            """)
            
            if st.button("📥 Gerar Marketing", use_container_width=True):
                with st.spinner("Gerando relatório de marketing..."):
                    pdf_bytes = PDFReportManager.generate_marketing_report()
                    st.success("✅ Relatório de marketing gerado!")
                    
                    st.download_button(
                        label="📄 Download PDF Marketing", 
                        data=pdf_bytes,
                        file_name=f"Aurum_Business_Marketing_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col3:
            st.markdown("""
            #### ⚙️ Relatório Operacional
            **Conteúdo:**
            - Performance equipe vendas
            - Pipeline detalhado
            - Previsões mensais
            - Produtividade individual
            - Ações necessárias
            - Metas vs realizados
            """)
            
            if st.button("📥 Gerar Operacional", use_container_width=True):
                with st.spinner("Gerando relatório operacional..."):
                    pdf_bytes = PDFReportManager.generate_operational_report()
                    st.success("✅ Relatório operacional gerado!")
                    
                    st.download_button(
                        label="📄 Download PDF Operacional",
                        data=pdf_bytes, 
                        file_name=f"Aurum_Business_Operacional_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📧 Envio Automático (Simulado)")
            st.text_input("Email CEO", value="ceo@aurumcompany.com")
            st.text_input("Email Diretoria", value="diretoria@aurumcompany.com") 
            st.text_input("Email Marketing", value="marketing@aurumcompany.com")
            
            if st.button("📤 Enviar Todos", use_container_width=True):
                st.success("✅ Relatórios enviados por email!")
        
        with col2:
            st.markdown("### ⚡ Geração em Lote")
            
            report_types = st.multiselect(
                "Selecionar Relatórios",
                ["Executivo", "Marketing", "Operacional"],
                default=["Executivo", "Marketing"]
            )
            
            period = st.selectbox("Período", ["Última Semana", "Último Mês", "Personalizado"])
            
            if st.button("🚀 Gerar Lote", use_container_width=True):
                st.success(f"✅ {len(report_types)} relatórios gerados em lote!")
    
    with tab2:
        st.markdown("### 📅 Agendamentos Automáticos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚙️ Configurar Agendamentos")
            
            schedule_type = st.selectbox("Tipo de Relatório", ["Executivo", "Marketing", "Operacional"])
            frequency = st.selectbox("Frequência", ["Diário", "Semanal", "Mensal", "Trimestral"])
            day_time = st.time_input("Horário", value=datetime.strptime("09:00", "%H:%M").time())
            
            recipients = st.text_area("Destinatários (separados por vírgula)", 
                                    "ceo@aurumcompany.com, manager@aurumcompany.com")
            
            if st.button("💾 Salvar Agendamento", use_container_width=True):
                st.success("✅ Agendamento salvo com sucesso!")
        
        with col2:
            st.markdown("#### 📋 Agendamentos Ativos")
            
            active_schedules = pd.DataFrame({
                'Relatório': ['Executivo Mensal', 'Marketing Semanal', 'Operacional Mensal'],
                'Frequência': ['Todo dia 1º', 'Toda segunda 9h', 'Todo dia 30'],
                'Destinatários': ['3 pessoas', '5 pessoas', '8 pessoas'],
                'Status': ['🟢 Ativo', '🟢 Ativo', '🟡 Pausado'],
                'Próximo Envio': ['01/01/2025', '06/01/2025', 'N/A']
            })
            
            st.dataframe(active_schedules, use_container_width=True)
            
            st.markdown("#### 🎛️ Controles")
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("⏸️ Pausar Todos"):
                    st.warning("⏸️ Agendamentos pausados")
            
            with col_b:
                if st.button("▶️ Reativar Todos"):
                    st.success("▶️ Agendamentos reativados")
    
    with tab3:
        st.markdown("### 🎨 Templates e Personalização")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎨 Customização Visual")
            
            logo_upload = st.file_uploader("📷 Logo da Empresa", type=['png', 'jpg'])
            primary_color = st.color_picker("🎨 Cor Primária", value="#1E40AF")
            secondary_color = st.color_picker("🎨 Cor Secundária", value="#10B981")
            
            st.markdown("#### 📝 Textos Padrão")
            company_name = st.text_input("Nome da Empresa", value="Aurum Business")
            report_footer = st.text_area("Rodapé dos Relatórios", 
                                        "Este relatório é confidencial e destinado exclusivamente ao uso interno.")
        
        with col2:
            st.markdown("#### 📊 Elementos dos Relatórios")
            
            include_charts = st.checkbox("Incluir Gráficos", value=True)
            include_executive = st.checkbox("Resumo Executivo", value=True)
            include_recommendations = st.checkbox("Recomendações", value=True)
            include_appendix = st.checkbox("Anexos Técnicos", value=False)
            
            st.markdown("#### 💾 Templates Salvos")
            
            templates = ["Template Padrão Aurum", "Template Executivo", "Template Técnico"]
            selected_template = st.selectbox("Selecionar Template", templates)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("💾 Salvar Template"):
                    st.success("✅ Template salvo!")
            
            with col_b:
                if st.button("🔄 Restaurar Padrão"):
                    st.info("🔄 Configuração restaurada!")
        
        st.markdown("---")
        
        if st.button("👁️ Visualizar Preview", use_container_width=True):
            st.success("✅ Preview gerado com as configurações atuais!")
    
    with tab4:
        st.markdown("### 📈 Analytics de Relatórios")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Relatórios Gerados", "1,247", "↗️ 23 este mês")
        with col2:
            st.metric("Emails Enviados", "3,891", "↗️ 12% taxa abertura")
        with col3:
            st.metric("Downloads", "987", "↗️ 34 esta semana")
        with col4:
            st.metric("Templates Ativos", "12", "↗️ 3 novos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de relatórios por tipo
            reports_data = pd.DataFrame({
                'Tipo': ['Executivo', 'Marketing', 'Operacional', 'Ad-hoc'],
                'Quantidade': [245, 387, 298, 317]
            })
            
            fig = go.Figure(data=[go.Bar(
                x=reports_data['Tipo'],
                y=reports_data['Quantidade'],
                marker_color=[theme['primary'], theme['secondary'], theme['accent'], '#FFA500']
            )])
            fig.update_layout(
                title="📊 Relatórios por Tipo - Últimos 30 dias",
                template=theme['plotly_template']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de linha - Evolução mensal
            evolution_data = pd.DataFrame({
                'Mês': ['Ago', 'Set', 'Out', 'Nov', 'Dez', 'Jan'],
                'Gerados': [89, 134, 156, 198, 247, 298],
                'Enviados': [72, 118, 142, 185, 234, 287]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=evolution_data['Mês'], y=evolution_data['Gerados'],
                                   mode='lines+markers', name='Gerados',
                                   line=dict(color=theme['primary'], width=3)))
            fig.add_trace(go.Scatter(x=evolution_data['Mês'], y=evolution_data['Enviados'],
                                   mode='lines+markers', name='Enviados',
                                   line=dict(color=theme['secondary'], width=3)))
            fig.update_layout(title="📈 Evolução Mensal de Relatórios")
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de performance
        st.markdown("#### 🎯 Performance por Template")
        
        template_performance = pd.DataFrame({
            'Template': ['Aurum Executivo', 'Marketing Premium', 'Operacional Pro', 'Análise Técnica'],
            'Uso': [89, 67, 54, 23],
            'Satisfação': [4.8, 4.6, 4.7, 4.2],
            'Tempo Médio Geração': ['2.3s', '1.8s', '2.1s', '3.4s'],
            'Taxa Download': ['94%', '87%', '91%', '76%']
        })
        
        st.dataframe(
            template_performance,
            use_container_width=True,
            column_config={
                "Satisfação": st.column_config.NumberColumn("⭐ Satisfação", format="%.1f"),
                "Taxa Download": st.column_config.ProgressColumn("📥 Taxa Download", max_value=100)
            }
        )