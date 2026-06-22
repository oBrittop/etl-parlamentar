
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.metrics import (
    deputados_unique,
    expense_partido,
    expense_uf,
    ranking_expense_deputado,
    ranking_fornecedores,
    total_expenses,
    values_category,
    values_data,
    calculate_weekend_expenses, 
    calculate_benford_law
)

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

expense_total = total_expenses(filtered_df)
parliamentarians_total = deputados_unique(filtered_df)
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
        monthly_df = values_data(filtered_df)
        st.pyplot(line_chart(monthly_df))

    with right:
        category_df = values_category(filtered_df).head(top_n)
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
        ranking_df = ranking_expense_deputado(filtered_df, limit=top_n)
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
        party_df = expense_partido(filtered_df).head(top_n)
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
    state_df = expense_uf(filtered_df).head(top_n)
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
    supplier_df = ranking_fornecedores(filtered_df, limit=top_n)
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
    
with tab_alerts:
    st.subheader("Análise de Inconsistências e Padrões Atípicos")
    st.caption("Esta seção utiliza técnicas de auditoria estatística e temporal para identificar anomalias nos gastos.")
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.write("### Teste Lei de Benford")
        st.info("A Lei de Benford prevê a frequência natural de primeiros dígitos em dados financeiros estruturados. Desvios acentuados podem indicar acúmulo artificial de notas com valores específicos.")
        
        benford_df = calculate_benford_law(filtered_df)
        
        if not benford_df.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            
            
            ax.bar(benford_df["Digito"] - 0.2, benford_df["Frequencia_Real"], width=0.4, label="Frequência Real", color="#0284c7")
            ax.plot(benford_df["Digito"], benford_df["Frequencia_Teorica"], marker="o", color="#dc2626", linewidth=2, label="Lei de Benford (Esperado)")
            
            ax.set_xticks(range(1, 10))
            style_axes(ax, "Distribuição do Primeiro Dígito vs. Lei de Benford", "Dígito Inicial", "% do Total de Registros")
            ax.legend()
            
            st.pyplot(fig, clear_figure=True)
        else:
            st.warning("Dados insuficientes para calcular a Lei de Benford.")

    with right_col:
        st.write("### Emissões em Finais de Semana")
        
        weekend_data = calculate_weekend_expenses(filtered_df)
        
        c1, c2 = st.columns(2)
        c1.metric("Gastos no Fim de Semana", format_short_currency(weekend_data["weekend_val"]))
        c2.metric("Proporção do Total", f"{weekend_data["percentage_weekend"]:.2f}%")
        
        
        if weekend_data["weekend_val"] > 0 or weekend_data["weekday_val"] > 0:
            fig2, ax2 = plt.subplots(figsize=(8, 4.5))
            labels = ['Dias Úteis', 'Fim de Semana']
            valores = [weekend_data["weekday_val"], weekend_data["weekend_val"]]
            
            ax2.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#475569", "#f97316"], wedgeprops={'edgecolor': 'w'})
            ax2.set_title("Distribuição Financeira: Emissão Cronológica", fontsize=11, fontweight="bold")
            
            st.pyplot(fig2, clear_figure=True)
            st.warning(
            "⚠️ **Nota Metodológica (Faca de Dois Gumes):** Alta concentração de despesas emitidas no "
            "sábado ou domingo pode apontar serviços executados fora do período de atividade parlamentar comum. "
            "Contudo, bilhetes aéreos ou hospedagens compradas anteriormente podem ser faturados ou processados "
            "automaticamente pelo sistema em dias não úteis, gerando falsos positivos. Recomenda-se auditar por categoria (ex: Alimentação e Combustíveis)."
        )

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
