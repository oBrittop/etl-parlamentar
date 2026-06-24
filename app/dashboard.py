
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import src.metrics

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "despesas_ceap_2025.csv"
PAGE_TITLE = "Observatorio da Cota Parlamentar"

MONTH_NAMES = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    numeric_columns = ["vlrLiquido", "numMes", "numAno", "ideCadastro"]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_short_currency(value: float) -> str:
    if value >= 1_000_000_000:
        return f"R$ {value / 1_000_000_000:.2f} bi".replace(".", ",")
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f} mi".replace(".", ",")
    if value >= 1_000:
        return f"R$ {value / 1_000:.2f} mil".replace(".", ",")
    return format_currency(value)


def apply_filters(df: pd.DataFrame, parties: list[str], states: list[str], categories: list[str], months: list[int]) -> pd.DataFrame:
    filtered_df = df.copy()

    if parties:
        filtered_df = filtered_df[filtered_df["sgPartido"].isin(parties)]
    if states:
        filtered_df = filtered_df[filtered_df["sgUF"].isin(states)]
    if categories:
        filtered_df = filtered_df[filtered_df["txtDescricao"].isin(categories)]
    if months:
        filtered_df = filtered_df[filtered_df["numMes"].isin(months)]

    return filtered_df


def style_axes(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def horizontal_bar_chart(
    df: pd.DataFrame,
    label_column: str,
    value_column: str,
    title: str,
    xlabel: str,
    color: str,
):
    plot_df = df.copy().sort_values(value_column, ascending=True)
    fig_height = max(4, len(plot_df) * 0.45)
    fig, ax = plt.subplots(figsize=(11, fig_height))

    bars = ax.barh(plot_df[label_column].astype(str), plot_df[value_column], color=color)
    style_axes(ax, title, xlabel, "")

    for bar in bars:
        value = bar.get_width()
        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f" {format_short_currency(value)}",
            va="center",
            fontsize=9,
        )

    fig.tight_layout()  
    return fig


def line_chart(df: pd.DataFrame):
    plot_df = df.copy()
    plot_df["mes_nome"] = plot_df["numMes"].map(MONTH_NAMES)

    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(
        plot_df["mes_nome"],
        plot_df["vlrLiquido"],
        marker="o",
        linewidth=2.5,
        color="#2563eb",
        label="Gasto mensal",
    )
    ax.fill_between(plot_df["mes_nome"], plot_df["vlrLiquido"], alpha=0.12, color="#2563eb")

    ax.set_title("Evolucao mensal dos gastos", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Mes", fontsize=10)
    ax.set_ylabel("Valor liquido", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.legend(loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig

def show_dataframe(df: pd.DataFrame, value_column: str = "vlrLiquido") -> None:
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            value_column: st.column_config.NumberColumn(
                "Valor Líquido",
                format="R$ %.2f"
            )
        }
    )


st.markdown(
    """
    <style>
        .main .block-container {
            padding-top: 1.6rem;
            padding-bottom: 2rem;
        }
        .hero {
            padding: 1.2rem 0 0.4rem 0;
            border-bottom: 1px solid rgba(120, 120, 120, 0.25);
            margin-bottom: 1.2rem;
        }
        .hero h1 {
            font-size: 2.1rem;
            margin-bottom: 0.2rem;
            letter-spacing: 0;
        }
        .hero p {
            color: #64748b;
            font-size: 1rem;
            margin-top: 0;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(120, 120, 120, 0.22);
            border-radius: 8px;
            padding: 0.8rem 1rem;
            background: rgba(248, 250, 252, 0.7);
        }
        section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Observatorio da Cota Parlamentar</h1>
        <p>Analise interativa das despesas CEAP 2025 com filtros, rankings e visualizacoes em Matplotlib.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not DATA_PATH.exists():
    st.error("Base tratada nao encontrada. Execute primeiro: python main.py")
    st.stop()

try:
    df = load_data(DATA_PATH)
except Exception as error:
    st.error(f"Erro ao carregar a base tratada: {error}")
    st.stop()

with st.sidebar:
    st.header("Filtros")
    st.caption("Use os filtros para comparar partidos, estados, categorias e meses.")

    top_n = st.slider("Quantidade nos rankings", min_value=5, max_value=27, value=10, step=1)

    party_options = sorted(df["sgPartido"].dropna().unique().tolist())
    state_options = sorted(df["sgUF"].dropna().unique().tolist())
    category_options = sorted(df["txtDescricao"].dropna().unique().tolist())
    month_options = sorted(df["numMes"].dropna().astype(int).unique().tolist())

    selected_parties = st.multiselect("Partidos", party_options)
    selected_states = st.multiselect("UFs", state_options)
    selected_categories = st.multiselect("Categorias de despesa", category_options)
    selected_months = st.multiselect(
        "Meses",
        month_options,
        format_func=lambda month: MONTH_NAMES.get(int(month), str(month)),
    )

filtered_df = apply_filters(df, selected_parties, selected_states, selected_categories, selected_months)

if filtered_df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

expense_total = src.metrics.total_expenses(filtered_df)
parliamentarians_total = src.metrics.deputados_unique(filtered_df)
documents_total = len(filtered_df)
average_expense = filtered_df["vlrLiquido"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gasto total", format_short_currency(expense_total))
col2.metric("Parlamentares", f"{parliamentarians_total:,}".replace(",", "."))
col3.metric("Registros", f"{documents_total:,}".replace(",", "."))
col4.metric("Media por registro", format_short_currency(average_expense))

st.divider()

tab_overview, tab_rankings, tab_suppliers,tab_alerts, tab_data = st.tabs(
    ["Visao geral", "Deputados e partidos", "Fornecedores","Alertas", "Dados"]
)


with tab_overview:
    left, right = st.columns([1.2, 1])

    with left:
        monthly_df = src.metrics.values_data(filtered_df)
        st.pyplot(line_chart(monthly_df))

    with right:
        category_df = src.metrics.values_category(filtered_df).head(top_n)
        fig = horizontal_bar_chart(
            category_df,
            "txtDescricao",
            "vlrLiquido",
            "Categorias com maior gasto",
            "Valor liquido",
            "#0f766e",
        )
        st.pyplot(fig, clear_figure=True)

    st.subheader("Gastos por categoria")
    show_dataframe(category_df)

with tab_rankings:
    left, right = st.columns(2)

    with left:
        ranking_df = src.metrics.ranking_expense_deputado(filtered_df, limit=top_n)
        ranking_df["deputado_label"] = (
            ranking_df["txNomeParlamentar"]
            + " ("
            + ranking_df["sgPartido"]
            + "-"
            + ranking_df["sgUF"]
            + ")"
        )
        fig = horizontal_bar_chart(
            ranking_df,
            "deputado_label",
            "vlrLiquido",
            "Deputados com maior gasto",
            "Valor liquido",
            "#1d4ed8",
        )
        st.pyplot(fig, clear_figure=True)
        show_dataframe(ranking_df.drop(columns="deputado_label"))

    with right:
        party_df = src.metrics.expense_partido(filtered_df).head(top_n)
        fig = horizontal_bar_chart(
            party_df,
            "sgPartido",
            "vlrLiquido",
            "Partidos com maior gasto",
            "Valor liquido",
            "#7c3aed",
        )
        st.pyplot(fig)
        show_dataframe(party_df)

    st.subheader("Gastos por unidade federativa")
    state_df = src.metrics.expense_uf(filtered_df).head(top_n)
    fig = horizontal_bar_chart(
        state_df,
        "sgUF",
        "vlrLiquido",
        "UFs com maior gasto",
        "Valor liquido",
        "#b45309",
    )
    st.pyplot(fig, clear_figure=True)
    show_dataframe(state_df)

with tab_suppliers:
    supplier_df = src.metrics.ranking_fornecedores(filtered_df, limit=top_n)
    fig = horizontal_bar_chart(
        supplier_df,
        "txtFornecedor",
        "vlrLiquido",
        "Fornecedores que mais receberam",
        "Valor liquido",
        "#be123c",
    )
    st.pyplot(fig, clear_figure=True)

    st.subheader("Ranking de fornecedores")
    show_dataframe(supplier_df)
    st.divider()
    
    st.write("### Malha Fina de Fornecedores (Possíveis Redes de Laranjas)")
    st.caption("Esta análise inverte a ótica: em vez de investigar o parlamentar, investiga o recebedor. Empresas com altos valores glosados por múltiplos deputados são fortes indicativos de escritórios de 'notas frias'.")
    df_forn_glosa = src.metrics.fornecedores_glosados(filtered_df)
    
    if not df_forn_glosa.empty:
        col_chart, col_table = st.columns([1, 1.4]) # Tabela maior porque os nomes dos deputados ocupam espaço
        
        with col_chart:
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            
            labels = df_forn_glosa["txtFornecedor"].apply(lambda x: (str(x)[:22] + '..') if len(str(x)) > 22 else str(x))
            valores = df_forn_glosa["total_glosa"]
            
            bars = ax5.barh(labels, valores, color="#ea580c") # Laranja escuro
            ax5.invert_yaxis()
            
            ax5.set_title("Fornecedores com Mais Glosas", fontsize=11, fontweight="bold", pad=12)
            ax5.spines["top"].set_visible(False)
            ax5.spines["right"].set_visible(False)
            
            for bar in bars:
                width = bar.get_width()
                ax5.text(
                    width, 
                    bar.get_y() + bar.get_height() / 2, 
                    f" R$ {width:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                    ha='left', 
                    va='center', 
                    fontsize=9,
                    fontweight='bold',
                    color="#9a3412"
                )
                
            fig5.tight_layout()
            st.pyplot(fig5, clear_figure=True)
            
        with col_table:
            st.write("**Quem tentou usar essa empresa?**")
            st.dataframe(
                df_forn_glosa,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "txtFornecedor": "Fornecedor",
                    "total_glosa": st.column_config.NumberColumn("Total Bloqueado", format="R$ %.2f"),
                    "qtd_tentativas": st.column_config.NumberColumn("Nº Notas", format="%d"),
                    "deputados_envolvidos": "Parlamentares Envolvidos"
                }
            )
    else:
        st.success("Nenhum fornecedor apresentou retenção/glosa nos filtros atuais.")

with tab_alerts:
    st.subheader("Análise de Inconsistências e Padrões Atípicos")
    st.caption("Esta seção utiliza técnicas de auditoria estatística e temporal para identificar anomalias nos gastos.")
    
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.write("###  Teste da Lei de Benford")
        st.info("A Lei de Benford prevê a frequência natural de primeiros dígitos. Desvios indicam acúmulo artificial de notas.")
        
        benford_df = src.metrics.calculate_benford_law(filtered_df)
        
        if not benford_df.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(benford_df["Digito"] - 0.2, benford_df["Frequencia_Real"], width=0.4, label="Frequência Real", color="#0284c7")
            ax.plot(benford_df["Digito"], benford_df["Frequencia_Teorica"], marker="o", color="#dc2626", linewidth=2, label="Lei de Benford (Esperado)")
            
            ax.set_xticks(range(1, 10))
            style_axes(ax, "Distribuição do 1º Dígito vs. Benford", "Dígito Inicial", "% do Total")
            ax.legend()
            
            st.pyplot(fig, clear_figure=True)
        else:
            st.warning("Dados insuficientes para calcular a Lei de Benford.")

    with right_col:
        st.write("###  Emissões em Finais de Semana")
        
        weekend_data = src.metrics.calculate_weekend_expenses(filtered_df)
        
        c1, c2 = st.columns(2)
        c1.metric("Gastos no Fim de Semana", format_short_currency(weekend_data["weekend_val"]))
        c2.metric("Proporção do Total", f"{weekend_data['percentage_weekend']:.2f}%")
        
        if weekend_data["weekend_val"] > 0 or weekend_data["weekday_val"] > 0:
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            labels = ['Dias Úteis', 'Fim de Semana']
            valores = [weekend_data["weekday_val"], weekend_data["weekend_val"]]
            
            bars = ax2.bar(labels, valores, color=["#475569", "#f97316"], width=0.5)
            
            ax2.set_title("Comparativo: Dias Úteis vs Finais de Semana", fontsize=11, fontweight="bold", pad=15)
            
            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            ax2.spines["left"].set_visible(False)
            ax2.get_yaxis().set_visible(False)
            
            ax2.set_ylim(0, max(valores) * 1.3)
            
            total = sum(valores)
            for bar in bars:
                altura = bar.get_height()
                percentual = (altura / total) * 100
                texto_label = f"{percentual:.1f}%\n({format_short_currency(altura)})"
                
                ax2.text(
                    bar.get_x() + bar.get_width() / 2, 
                    altura + (max(valores) * 0.05), 
                    texto_label, 
                    ha='center', 
                    va='bottom', 
                    fontsize=10,
                    fontweight='bold',
                    color="#334155"
                )
            st.pyplot(fig2, clear_figure=True)

    
    st.divider() 
    
    st.write("### Anomalia Logística: O Padrão do 'Tanque Infinito'")
    st.info("Veículos de passeio possuem tanques com capacidade média de 45 a 60 litros. Notas de combustível que ultrapassam esse volume em um único recibo sugerem o abastecimento de múltiplos veículos ou frotas de terceiros.")
    
    df_fuel_anomalies = src.metrics.tanque_infinito(filtered_df)
    
    if not df_fuel_anomalies.empty:
        
        col_scatter, col_table = st.columns([1.8, 1])
        
        with col_scatter:
            import matplotlib.dates as mdates
            
            plot_data = df_fuel_anomalies.copy()
            
            plot_data['datEmissao'] = pd.to_datetime(plot_data['datEmissao'], errors='coerce')
            plot_data = plot_data.dropna(subset=['datEmissao'])
            
            fig3, ax3 = plt.subplots(figsize=(10, 4.5))
            
            
            ax3.scatter(plot_data['datEmissao'], plot_data['litros_estimados'], color="#dc2626", alpha=0.6, edgecolors="black", s=70)
            
            ax3.axhline(y=60, color='black', linestyle='--', linewidth=2, label="Limite Físico (60 Litros)")
            
            ax3.set_title("Abastecimentos Suspeitos (Acima de 60 Litros)", fontsize=12, fontweight="bold", pad=12)
            ax3.set_ylabel("Volume Estimado (Litros)", fontsize=10)
            ax3.legend()
            ax3.grid(True, linestyle="--", alpha=0.3)
            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            plt.xticks(rotation=45)
            fig3.tight_layout()
            
            st.pyplot(fig3, clear_figure=True)
            
        with col_table:
            st.write("**O Efeito 'Teto da Cota' (Recibos no Limite)**")
            st.caption(
                "🚨 **Alerta de Comportamento:** O valor de R$ 9.392,00 é o limite máximo mensal de combustível. "
                "Concentrar esse volume em uma única nota fiscal indica abastecimento de frotas ou fechamento de "
                "conta corporativa (mensalista), dificultando a auditoria de qual veículo foi realmente abastecido dia a dia."
            )
            
      
            display_anomalies = plot_data[
                ['txNomeParlamentar', 'sgUF', 'datEmissao', 'litros_estimados', 'vlrLiquido']
            ].sort_values('vlrLiquido', ascending=False).head(10)
            
            st.dataframe(
                display_anomalies,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "txNomeParlamentar": "Parlamentar",
                    "sgUF": "UF",
                    "datEmissao": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                    "litros_estimados": st.column_config.NumberColumn("Vol.", format="%.1f L"),
                    "vlrLiquido": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                }
            )
    else:
        st.success("Nenhuma anomalia de abastecimento encontrada com os filtros atuais ou na categoria de combustíveis.")
        
        st.divider()
    
    col_glosa, col_exterior = st.columns(2)
    
    with col_glosa:
        st.write("### 🛑 Top Rejeições (Glosas)")
        st.info("A **Glosa** ocorre quando a auditoria da Câmara nega o reembolso. Parlamentares no topo desta lista apresentam alto volume de tentativas de gastos irregulares.")
        
        df_glosa = src.metrics.ranking_glosa(filtered_df)
        if not df_glosa.empty:
            st.dataframe(
                df_glosa,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "txNomeParlamentar": "Parlamentar",
                    "sgPartido": "Partido",
                    "sgUF": None, 
                    "qtd_tentativas": st.column_config.NumberColumn("Nº Bloqueios", format="%d"),
                    "total_barrado": st.column_config.NumberColumn("Valor Barrado", format="R$ %.2f")
                }
            )
        else:
            st.success("Nenhum registro de glosa encontrado para estes filtros.")

    with col_exterior:
        st.write("### ✈️ Gastos no Exterior")
        st.info("Despesas efetivamente pagos e ressarcidos por uso fora do território nacional (identificadas pelo Tipo de Documento 2 no sistema da CEAP).")
        
        df_ext = src.metrics.gastos_exterior(filtered_df)
        if not df_ext.empty:
            st.dataframe(
                df_ext,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "txNomeParlamentar": "Parlamentar",
                    "sgPartido": None, 
                    "txtDescricao": "Categoria",
                    "qtd_despesas": st.column_config.NumberColumn("Qtd.", format="%d"),
                    "total_gasto": st.column_config.NumberColumn("Total Gasto", format="R$ %.2f")
                }
            )
        else:
            st.success("Nenhum gasto no exterior encontrado nos filtros atuais.")
            
    st.divider()    
    st.write("### 🚨 Cruzamento de Risco: Tentativas de Irregularidade no Exterior")
    st.caption("Esta análise expõe parlamentares que tiveram despesas realizadas fora do país bloqueadas/rejeitadas pela auditoria. É o nível mais alto de alerta no uso da CEAP.")
    
    df_cross = src.metrics.glosa_no_exterior(filtered_df)
    
    if not df_cross.empty:
        df_cross["deputado_label"] = df_cross["txNomeParlamentar"] + " (" + df_cross["sgPartido"] + ")"
        
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        
        bars = ax4.barh(df_cross["deputado_label"].astype(str), df_cross["total_barrado"], color="#9f1239")
        
        ax4.set_title("Valores Barrados em Despesas Internacionais", fontsize=12, fontweight="bold", pad=12)
        ax4.set_xlabel("Valor Glosado (R$)", fontsize=10)
        
        ax4.spines["top"].set_visible(False)
        ax4.spines["right"].set_visible(False)
        ax4.grid(axis="x", linestyle="--", alpha=0.3)
        ax4.invert_yaxis()
        

        for bar in bars:
            width = bar.get_width()
            ax4.text(
                width, 
                bar.get_y() + bar.get_height() / 2, 
                f" R$ {width:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                ha='left', 
                va='center', 
                fontsize=9,
                fontweight='bold',
                color="#7f1d1d"
            )
            
        fig4.tight_layout()
        st.pyplot(fig4, clear_figure=True)
    else:
        st.success("Nenhuma tentativa de gasto irregular no exterior foi detectada neste período.")

with tab_data:
    st.subheader("Base filtrada")
    st.caption("A tabela abaixo mostra os registros depois da aplicacao dos filtros laterais.")

    selected_columns = [
        "txNomeParlamentar",
        "sgPartido",
        "sgUF",
        "txtDescricao",
        "txtFornecedor",
        "vlrLiquido",
        "numMes",
        "numAno",
        "tem_documento",
    ]
    available_columns = [column for column in selected_columns if column in filtered_df.columns]
    show_dataframe(filtered_df[available_columns].head(500))

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Baixar base filtrada",
        data=csv,
        file_name="despesas_ceap_2025_filtradas.csv",
        mime="text/csv",
    )
