"""
============================================================
Product Sales Dashboard  |  Interactive Streamlit App
============================================================
Run locally:
    pip install streamlit pandas matplotlib seaborn plotly squarify
    streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import squarify
import warnings
import requests
import json
import time
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────
CHART_BG   = "#EAF2F8"   # soft blue-grey chart canvas
PAPER_BG   = "#F4F9FF"   # slightly lighter outer area
GRID_COLOR = "#C5D8E8"   # subtle grid lines
AXIS_COLOR = "#2C3E50"   # axis lines & ticks
TITLE_COLOR= "#0B2545"   # chart title
TICK_FONT  = 11
LABEL_FONT = 12
TITLE_FONT = 15

# Matplotlib global theme
plt.rcParams.update({
    "figure.facecolor": PAPER_BG,
    "axes.facecolor":   CHART_BG,
    "axes.edgecolor":   AXIS_COLOR,
    "axes.labelcolor":  AXIS_COLOR,
    "axes.labelsize":   LABEL_FONT,
    "axes.titlesize":   TITLE_FONT,
    "axes.titlecolor":  TITLE_COLOR,
    "axes.titleweight": "bold",
    "axes.grid":        True,
    "grid.color":       GRID_COLOR,
    "grid.linewidth":   0.7,
    "xtick.color":      AXIS_COLOR,
    "ytick.color":      AXIS_COLOR,
    "xtick.labelsize":  TICK_FONT,
    "ytick.labelsize":  TICK_FONT,
    "font.family":      "DejaVu Sans",
    "legend.fontsize":  10,
    "legend.framealpha": 0.85,
})

PALETTE = [
    "#1A6B8A", "#2ECC9A", "#2563A8", "#F4A261", "#E76F51",
    "#9B59B6", "#16A085", "#D35400", "#2980B9", "#E9C46A",
]

# ─────────────────────────────────────────────────────────────
# SHARED PLOTLY LAYOUT HELPER
# ─────────────────────────────────────────────────────────────
def apply_layout(fig, title="", xlabel="", ylabel="",
                 height=420, xtickformat=None, ytickformat=None,
                 xrange=None, yrange=None, show_legend=True,
                 x_tickangle=0):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=TITLE_FONT, color=TITLE_COLOR, family="Arial Bold"),
            x=0, xanchor="left", pad=dict(l=8, t=4),
        ),
        plot_bgcolor=CHART_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="Arial", size=11, color=AXIS_COLOR),
        height=height,
        margin=dict(t=72, b=64, l=74, r=44),
        showlegend=show_legend,
        legend=dict(bgcolor="rgba(255,255,255,0.85)",
                    bordercolor=GRID_COLOR, borderwidth=1),
        xaxis=dict(
            title=dict(text=xlabel,
                       font=dict(size=LABEL_FONT, color=AXIS_COLOR)),
            tickfont=dict(size=TICK_FONT, color=AXIS_COLOR),
            showline=True, linecolor=AXIS_COLOR, linewidth=1.5,
            showgrid=True, gridcolor=GRID_COLOR, gridwidth=0.8,
            tickangle=x_tickangle, automargin=True,
            **({"tickformat": xtickformat} if xtickformat else {}),
            **({"range": xrange}           if xrange       else {}),
        ),
        yaxis=dict(
            title=dict(text=ylabel,
                       font=dict(size=LABEL_FONT, color=AXIS_COLOR)),
            tickfont=dict(size=TICK_FONT, color=AXIS_COLOR),
            showline=True, linecolor=AXIS_COLOR, linewidth=1.5,
            showgrid=True, gridcolor=GRID_COLOR, gridwidth=0.8,
            automargin=True,
            **({"tickformat": ytickformat} if ytickformat else {}),
            **({"range": yrange}           if yrange       else {}),
        ),
    )
    return fig


def apply_pie_layout(fig, title="", height=420):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=TITLE_FONT, color=TITLE_COLOR, family="Arial Bold"),
            x=0, xanchor="left", pad=dict(l=8, t=4),
        ),
        paper_bgcolor=PAPER_BG,
        font=dict(family="Arial", size=11, color=AXIS_COLOR),
        height=height,
        margin=dict(t=72, b=44, l=22, r=22),
        legend=dict(bgcolor="rgba(255,255,255,0.85)",
                    bordercolor=GRID_COLOR, borderwidth=1),
    )
    return fig


# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #F0F6FB; }
    [data-testid="metric-container"] {
        background: white; border-radius: 12px; padding: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,.10);
        border-left: 5px solid #1A6B8A;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B2545 0%, #134074 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    .section-header {
        background: linear-gradient(90deg, #0B2545, #1A6B8A);
        color: white; padding: 10px 22px; border-radius: 8px;
        margin: 20px 0 12px 0; font-size: 17px; font-weight: 700;
        letter-spacing: .8px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: white; border-radius: 10px; padding: 4px;
    }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 600; }
    h1, h2, h3 { color: #0B2545; }

    /* ── Chat bubble styles ──────────────────────────────── */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 4px 8px;
        margin-bottom: 6px;
    }
    [data-testid="stChatMessage"][data-role="user"] {
        background: #D6EEF8;
        border-left: 4px solid #1A6B8A;
    }
    [data-testid="stChatMessage"][data-role="assistant"] {
        background: #FFFFFF;
        border-left: 4px solid #2ECC9A;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    }
        
    div[data-testid="column"] .stButton > button:hover {
        background: #1A6B8A !important;
        color: white !important;
        border-color: #1A6B8A !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path="product_sales_dataset_final.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    df["Order_Date"]    = pd.to_datetime(df["Order_Date"], format="%m-%d-%y", errors="coerce")
    df["Year"]          = df["Order_Date"].dt.year
    df["Month"]         = df["Order_Date"].dt.month
    df["Month_Name"]    = df["Order_Date"].dt.strftime("%b")
    df["Quarter"]       = df["Order_Date"].dt.to_period("Q").astype(str)
    df["Profit_Margin"] = (df["Profit"] / df["Revenue"] * 100).round(2)
    return df

try:
    df_full      = load_data()
    data_source  = "local"
except FileNotFoundError:
    data_source  = "upload"

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:

    if data_source == "upload":
        uploaded = st.file_uploader("📂 Upload CSV Dataset", type=["csv"])
        if uploaded:
            df_full = load_data(uploaded)
            data_source = "loaded"
        else:
            st.warning("Please upload the dataset to begin.")
            st.stop()

    st.markdown("### 🔧 Filters")
    years       = sorted(df_full["Year"].dropna().unique().astype(int).tolist())
    sel_years   = st.multiselect("📅 Year",     years,      default=years)
    regions     = sorted(df_full["Region"].unique().tolist())
    sel_regions = st.multiselect("🌍 Region",   regions,    default=regions)
    categories  = sorted(df_full["Category"].unique().tolist())
    sel_cats    = st.multiselect("🏷️ Category", categories, default=categories)

    st.markdown("---")
    st.markdown("### 📌 About")
    st.markdown(""" 
**Dataset:** Product Sales  
**Records:** 200,000  
**Period:** 2023–2024  
**Tools:** Python · Pandas  
Seaborn · Plotly · Streamlit
    """)

# ─────────────────────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────────────────────
df = df_full[
    df_full["Year"].isin(sel_years) &
    df_full["Region"].isin(sel_regions) &
    df_full["Category"].isin(sel_cats)
].copy()

if df.empty:
    st.error("⚠️ No data matches the selected filters.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(90deg,#0B2545,#1A6B8A);
            padding:24px 30px; border-radius:14px; margin-bottom:24px;'>
  <h1 style='color:white; margin:0; font-size:32px;'>
    🛒 Product Sales — Interactive Dashboard
  </h1>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# KPI TILES
# ─────────────────────────────────────────────────────────────
total_rev    = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)
avg_margin   = df["Profit_Margin"].mean()
total_qty    = df["Quantity"].sum()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Revenue",     f"${total_rev:,.0f}",    f"{total_rev/1e6:.2f}M")
k2.metric("📈 Total Profit",      f"${total_profit:,.0f}", f"{total_profit/1e6:.2f}M")
k3.metric("🛒 Total Orders",      f"{total_orders:,}")
k4.metric("🎯 Avg Profit Margin", f"{avg_margin:.1f}%")
k5.metric("📦 Units Sold",        f"{total_qty:,}")
st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# CHAT SECTION  (between KPIs and tabs)
# ══════════════════════════════════════════════════════════════

# ── Ollama config ─────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "Qwen2.5"  # Change to your model name if different

@st.cache_data
def build_dataset_context(_df):
    import pandas as pd

    df = _df.copy()

    # --- SAFETY CLEANING ---
    df.columns = df.columns.str.strip()
    for col in ["Revenue", "Profit", "Quantity", "Profit_Margin"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- BASIC KPIs ---
    total_rev    = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    total_qty    = df["Quantity"].sum()
    avg_margin   = df["Profit_Margin"].mean()
    avg_order_val = total_rev / total_orders if total_orders else 0

    # --- DATE RANGE ---
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    date_min = df["Order_Date"].min()
    date_max = df["Order_Date"].max()
    date_rng = (
        f"{date_min.strftime('%b %Y')} – {date_max.strftime('%b %Y')}"
        if pd.notna(date_min) else "N/A"
    )

    # --- CATEGORY BREAKDOWN (WITH SHARE %) ---
    cat_tbl = df.groupby("Category").agg(
        Revenue=("Revenue","sum"),
        Profit=("Profit","sum"),
        Orders=("Order_ID","count"),
        Avg_Margin=("Profit_Margin","mean")
    ).sort_values("Revenue", ascending=False)

    cat_tbl["Revenue_Share"] = (cat_tbl["Revenue"] / total_rev) * 100

    cat_lines = "\n".join(
        f"  - {cat}: Revenue=${row.Revenue:,.0f} ({row.Revenue_Share:.1f}%), "
        f"Profit=${row.Profit:,.0f}, Orders={row.Orders:,}, "
        f"AvgMargin={row.Avg_Margin:.1f}%"
        for cat, row in cat_tbl.iterrows()
    )

    # --- SUB-CATEGORY (TOP 10) ---
    subcat_tbl = df.groupby("Sub_Category")["Revenue"].sum().sort_values(ascending=False).head(10)
    subcat_lines = "\n".join(
        f"  - {name}: ${val:,.0f}" for name, val in subcat_tbl.items()
    )

    # --- REGION BREAKDOWN ---
    reg_tbl = df.groupby("Region").agg(
        Revenue=("Revenue","sum"),
        Profit=("Profit","sum"),
        Orders=("Order_ID","count"),
        Avg_Margin=("Profit_Margin","mean")
    ).sort_values("Revenue", ascending=False)

    reg_tbl["Revenue_Share"] = (reg_tbl["Revenue"] / total_rev) * 100

    reg_lines = "\n".join(
        f"  - {reg}: Revenue=${row.Revenue:,.0f} ({row.Revenue_Share:.1f}%), "
        f"Profit=${row.Profit:,.0f}, Orders={row.Orders:,}, "
        f"AvgMargin={row.Avg_Margin:.1f}%"
        for reg, row in reg_tbl.iterrows()
    )

    # --- TOP & BOTTOM PRODUCTS ---
    prod_rev = df.groupby("Product_Name")["Revenue"].sum().sort_values(ascending=False)

    top10 = prod_rev.head(10)
    bottom5 = prod_rev.tail(5)

    top10_lines = "\n".join(
        f"  {i+1}. {name}: ${rev:,.0f}" for i, (name, rev) in enumerate(top10.items())
    )

    bottom5_lines = "\n".join(
        f"  - {name}: ${rev:,.0f}" for name, rev in bottom5.items()
    )

    # --- MONTHLY TREND (IMPORTANT FOR LLM) ---
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month

    monthly = df.groupby(["Year","Month"]).agg(
        Revenue=("Revenue","sum"),
        Profit=("Profit","sum")
    ).reset_index().sort_values(["Year","Month"])

    monthly_lines = "\n".join(
        f"  - {int(row.Year)}-M{int(row.Month)}: Revenue=${row.Revenue:,.0f}, Profit=${row.Profit:,.0f}"
        for _, row in monthly.iterrows()
    )

    # --- BEST / WORST MONTH ---
    if not monthly.empty:
        best  = monthly.loc[monthly["Revenue"].idxmax()]
        worst = monthly.loc[monthly["Revenue"].idxmin()]

        temporal = (
            f"Best month: {int(best.Year)}-M{int(best.Month)} (${best.Revenue:,.0f}) | "
            f"Worst: {int(worst.Year)}-M{int(worst.Month)} (${worst.Revenue:,.0f})"
        )
    else:
        temporal = "No temporal data."

    # --- CORRELATION ---
    corr_rp = df["Revenue"].corr(df["Profit"])

    # --- FINAL CONTEXT ---
    return f"""
=== PRODUCT SALES DATASET CONTEXT ===

[OVERVIEW]
Date Range: {date_rng}
Total Orders: {total_orders:,}
Total Revenue: ${total_rev:,.0f}
Total Profit: ${total_profit:,.0f}
Units Sold: {total_qty:,}
Avg Margin: {avg_margin:.2f}%
Avg Order Value: ${avg_order_val:,.2f}

[CATEGORY PERFORMANCE]
{cat_lines}

[SUB-CATEGORY TOP 10]
{subcat_lines}

[REGIONAL PERFORMANCE]
{reg_lines}

[TOP 10 PRODUCTS]
{top10_lines}

[LOWEST 5 PRODUCTS]
{bottom5_lines}

[MONTHLY TREND]
{monthly_lines}

[KEY STATS]
Revenue–Profit Correlation: {corr_rp:.3f}
Revenue Mean: ${df["Revenue"].mean():,.2f} | Median: ${df["Revenue"].median():,.2f}
Profit Mean: ${df["Profit"].mean():,.2f} | Median: ${df["Profit"].median():,.2f}

[TEMPORAL HIGHLIGHTS]
{temporal}

======================================
""".strip()

dataset_context = build_dataset_context(df)

SYSTEM_PROMPT = f"""
You are a precision-first data analyst for a US retail product sales dashboard.

You must answer using ONLY the data provided in the dataset context below.
Do not use outside knowledge.
Do not guess missing values.
Do not infer trends that are not directly supported by the numbers in the context.

Dataset context:
{dataset_context}

Rules:
- Use only values explicitly present in the context.
- If a metric is not in the context, say it is unavailable.
- If the context does not support a conclusion, say so clearly.
- Be concise, factual, and dashboard-ready.
- Prefer bullet points for insights.
- Use USD format with commas, for example: $1,234,567.
- Keep percentages rounded to 1 decimal place unless exact precision is required.
- Do not invent rankings, averages, totals, or comparisons.
- If asked for a chart, return only valid Python code.
- For charts, use only labels and values that exist in the context.
- For month-based charts, preserve chronological order.
- For category, region, state, or product charts, use the exact breakdown values from the context.
- If there are multiple possible interpretations, state the assumption explicitly and keep it minimal.

Insight rules:
- Base insights on totals, comparisons, shares, and changes that are directly supported by the context.
- Do not overstate causation. Use wording like “highest”, “lowest”, “largest share”, or “shows” instead of “caused by”.
- When summarizing performance, mention revenue, profit, quantity, and margin only if those values are available in the context.
- If the context includes filtered data, always interpret results as “within the current filters”.

Output style:
- Start with the main insight first.
- Then add supporting facts.
- Keep the response short and accurate.

For charts:
- Return Python code only.
- Use matplotlib.
- Build the plot from the exact labels and values in the context.
- Do not fabricate missing categories or time periods.
"""
def check_ollama_running():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def list_ollama_models():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return []

def chat_with_ollama(messages, model=OLLAMA_MODEL):
    payload = {
        "model": model, "messages": messages, "stream": True,
        "options": {"temperature": 0.3, "top_p": 0.9, "num_ctx": 4096},
    }
    with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                chunk = json.loads(line)
                delta = chunk.get("message", {}).get("content", "")
                if delta:
                    yield delta
                if chunk.get("done"):
                    break

ollama_ok   = check_ollama_running()
model_ready = any(OLLAMA_MODEL in m for m in list_ollama_models())

# ── Compact header bar ────────────────────────────────────────────────────
if ollama_ok and model_ready:
    _badge = "<span style='background:#1d6b3a;color:#5ef59a;border:1px solid #5ef59a;border-radius:20px;padding:2px 10px;font-size:10px;font-weight:700;'>● ONLINE</span>"
elif ollama_ok:
    _badge = "<span style='background:#7a5200;color:#ffd966;border:1px solid #ffd966;border-radius:20px;padding:2px 10px;font-size:10px;font-weight:700;'>● MODEL MISSING</span>"
else:
    _badge = "<span style='background:#6b1d1d;color:#ff8080;border:1px solid #ff8080;border-radius:20px;padding:2px 10px;font-size:10px;font-weight:700;'>● OFFLINE</span>"

st.markdown(f"""
<div style='
    background: linear-gradient(90deg, #0B2545 0%, #1A6B8A 100%);
    border-radius: 12px 12px 0 0;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 0;
'>
  <span style='font-size:22px;'>🤖</span>
  <span style='color:white; font-size:16px; font-weight:700; flex:1;'>
    AI Sales Assistant
    <span style='color:#9AECDB; font-size:11px; font-weight:400; margin-left:8px;'>
      Powered by Ollama · {OLLAMA_MODEL} · 100% Local
    </span>
  </span>
  {_badge}
</div>
<div style='
    background: #F4F9FF;
    border: 1px solid #C5D8E8;
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 0;
    margin-bottom: 8px;
'>
""", unsafe_allow_html=True)


# ── Init session state ────────────────────────────────────────────────────
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if not st.session_state["chat_messages"]:
    st.session_state["chat_messages"].append({
        "role": "assistant",
        "content": (
            "👋 Hello! I'm your **Product Sales AI Assistant**.\n\n"
            "I have full access to your filtered dataset — ask me anything about "
            "**revenue, profit, regions, products, trends, or correlations**."
        ),
    })

# ── Chat history (fixed height scrollable box) ────────────────────────────
st.markdown("""
<div style='padding: 0 16px;'>
<style>
  .chat-scroll-box {
    max-height: 320px;
    overflow-y: auto;
    padding: 8px 4px;
    border-radius: 8px;
    background: transparent;
  }
  .chat-scroll-box::-webkit-scrollbar { width: 5px; }
  .chat-scroll-box::-webkit-scrollbar-thumb {
    background: #C5D8E8; border-radius: 4px;
  }
</style>
</div>
""", unsafe_allow_html=True)

with st.container():
    for _msg in st.session_state["chat_messages"]:
        _av = "🤖" if _msg["role"] == "assistant" else "🧑‍💻"
        with st.chat_message(_msg["role"], avatar=_av):
            st.markdown(_msg["content"])

# ── Handle chip click ─────────────────────────────────────────────────────
if "pending_question" in st.session_state:
    _question = st.session_state.pop("pending_question")
    st.session_state["chat_messages"].append({"role": "user", "content": _question})
    st.rerun()

# ── Input row ─────────────────────────────────────────────────────────────
_inp_col, _btn_col = st.columns([5, 1])
with _inp_col:
    user_input = st.chat_input(
        "Ask anything about the dataset…  e.g.  'Which product has the best margin?'"
    )
with _btn_col:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Delete History", key="clr_chat", use_container_width=True):
        st.session_state["chat_messages"] = []
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close inner padding div
st.markdown("</div>", unsafe_allow_html=True)  # close F4F9FF container div

# ── Parse chart JSON from AI reply ───────────────────────────────────────
import re as _re

def _render_chart_from_reply(reply_text):
    """Extract <chart_json>...</chart_json> from AI reply and render a Plotly chart."""
    match = _re.search(r"<chart_json>(.*?)</chart_json>", reply_text, _re.DOTALL)
    if not match:
        return None, reply_text
    raw_json = match.group(1).strip()
    # Strip the chart block from the displayed text
    clean_text = reply_text[:match.start()].strip() + "\n\n" + reply_text[match.end():].strip()
    clean_text = clean_text.strip()
    try:
        spec = json.loads(raw_json)
    except Exception:
        return None, clean_text

    ctype  = spec.get("type", "bar")
    title  = spec.get("title", "Chart")
    labels = spec.get("labels", [])
    values = spec.get("values", [])
    xlabel = spec.get("x_label", "")
    ylabel = spec.get("y_label", "")

    _PAL = ["#1A6B8A","#2ECC9A","#2563A8","#F4A261","#E76F51",
            "#9B59B6","#16A085","#D35400","#2980B9","#E9C46A"]

    if ctype == "bar":
        _fig = px.bar(x=labels, y=values, color=labels,
                      color_discrete_sequence=_PAL,
                      labels={"x": xlabel, "y": ylabel})
        _fig.update_traces(texttemplate="%{y:,.0f}", textposition="outside",
                           textfont_size=10)
        _fig.update_layout(showlegend=False)
    elif ctype == "line":
        _fig = px.line(x=labels, y=values, markers=True,
                       color_discrete_sequence=["#1A6B8A"],
                       labels={"x": xlabel, "y": ylabel})
        _fig.update_traces(line_width=2.5)
    elif ctype == "pie":
        _fig = px.pie(names=labels, values=values,
                      color_discrete_sequence=_PAL, hole=0.45)
        _fig.update_traces(textinfo="percent+label", textfont_size=12,
                           marker=dict(line=dict(color="white", width=2)))
    elif ctype == "scatter":
        _fig = px.scatter(x=labels, y=values,
                          color_discrete_sequence=["#1A6B8A"],
                          labels={"x": xlabel, "y": ylabel})
        _fig.update_traces(marker_size=9)
    elif ctype == "histogram":
        _fig = px.bar(x=labels, y=values, color_discrete_sequence=["#1A6B8A"],
                      labels={"x": xlabel, "y": ylabel})
    else:
        return None, clean_text

    _fig.update_layout(
        title=dict(text=f"🤖 AI-Generated: {title}",
                   font=dict(size=14, color="#0B2545")),
        plot_bgcolor="#EAF2F8", paper_bgcolor="#F4F9FF",
        height=340,
        margin=dict(t=60, b=50, l=60, r=30),
        xaxis=dict(showline=True, linecolor="#2C3E50", gridcolor="#C5D8E8",
                   title=xlabel, tickfont_size=10),
        yaxis=dict(showline=True, linecolor="#2C3E50", gridcolor="#C5D8E8",
                   title=ylabel, tickfont_size=10),
        font=dict(family="Arial", color="#2C3E50"),
    )
    return _fig, clean_text


# ── Handle user message ───────────────────────────────────────────────────
if user_input:
    st.session_state["chat_messages"].append({"role": "user", "content": user_input})
    _ollama_msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for _m in st.session_state["chat_messages"]:
        _ollama_msgs.append({"role": _m["role"], "content": _m["content"]})
    with st.chat_message("assistant", avatar="🤖"):
        if not ollama_ok:
            _reply = "⚠️ Ollama not running. Start Ollama and refresh."
            st.markdown(_reply)
        elif not model_ready:
            _reply = f"⚠️ Run `ollama pull {OLLAMA_MODEL}` then refresh."
            st.markdown(_reply)
        else:
            _placeholder = st.empty()
            _full = ""
            try:
                for _chunk in chat_with_ollama(_ollama_msgs):
                    _full += _chunk
                    _placeholder.markdown(_full + "▌")
                _placeholder.markdown(_full)
                _reply = _full
            except requests.exceptions.ConnectionError:
                _reply = "❌ Lost connection to Ollama."
                _placeholder.markdown(_reply)
            except Exception as _e:
                _reply = f"❌ Error: {str(_e)}"
                _placeholder.markdown(_reply)

        # Attempt to extract & render AI chart
        _chart_fig, _clean_reply = _render_chart_from_reply(_reply)
        if _chart_fig is not None:
            _placeholder.markdown(_clean_reply)
            st.plotly_chart(_chart_fig, use_container_width=True)
            # Store clean reply (without json block) in history
            _reply = _clean_reply + "\n\n📊 *Chart generated above*"

    st.session_state["chat_messages"].append({"role": "assistant", "content": _reply})
    st.rerun()

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]

# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📦 Category Analysis",
    "🌍 Regional Analysis",
    "📈 Time Series",
    "🏆 Product Rankings",
    "📊 Distributions",
    "🔗 Correlations",
    "📉 Forecast",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 – CATEGORY ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">📦 Category &amp; Sub-Category Analysis</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # Chart 1.1
    with c1:
        cat_rev = (df.groupby("Category")["Revenue"]
                     .sum().reset_index()
                     .sort_values("Revenue", ascending=False))
        fig = px.bar(cat_rev, x="Category", y="Revenue",
                     color="Category", color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate="$%{y:,.0f}", textposition="outside",
                          textfont_size=11, marker_line_width=0)
        apply_layout(fig,
                     title="Chart 1.1 — Total Revenue by Category",
                     xlabel="Product Category",
                     ylabel="Total Revenue (USD)",
                     ytickformat="$,.0f",
                     show_legend=False)
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # Chart 1.2
    with c2:
        fig2 = px.pie(cat_rev, values="Revenue", names="Category",
                      hole=0.52, color_discrete_sequence=PALETTE)
        fig2.update_traces(textposition="inside",
                           textinfo="percent+label",
                           textfont_size=12,
                           marker=dict(line=dict(color="white", width=2)))
        apply_pie_layout(fig2, title="Chart 1.2 — Revenue Share by Category (Donut)")
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 1.3
    sub_rev = (df.groupby("Sub_Category")["Revenue"]
                 .sum().reset_index()
                 .sort_values("Revenue", ascending=False))
    fig3 = px.bar(sub_rev, x="Revenue", y="Sub_Category",
                  orientation="h",
                  color="Revenue", color_continuous_scale="Teal")
    fig3.update_traces(texttemplate="$%{x:,.0f}", textposition="outside",
                       textfont_size=10)
    apply_layout(fig3,
                 title="Chart 1.3 — Revenue by Sub-Category",
                 xlabel="Total Revenue (USD)",
                 ylabel="Sub-Category",
                 xtickformat="$,.0f",
                 height=540,
                 show_legend=False)
    fig3.update_yaxes(autorange="reversed", tickfont_size=11)
    fig3.update_xaxes(rangemode="tozero")
    st.plotly_chart(fig3, use_container_width=True)

    # Chart 1.4
    cat_multi = df.groupby("Category")[["Revenue","Profit","Quantity"]].sum().reset_index()
    cat_melt  = cat_multi.melt(id_vars="Category", var_name="Metric", value_name="Value")
    fig4 = px.bar(cat_melt, x="Category", y="Value", color="Metric",
                  barmode="group", color_discrete_sequence=PALETTE)
    apply_layout(fig4,
                 title="Chart 1.4 — Revenue vs Profit vs Quantity by Category",
                 xlabel="Product Category",
                 ylabel="Value (USD / Units)",
                 ytickformat=",.0f")
    st.plotly_chart(fig4, use_container_width=True)

    # Chart 1.5
    tree_data = df.groupby(["Category","Sub_Category"])["Revenue"].sum().reset_index()
    fig5 = px.treemap(tree_data, path=["Category","Sub_Category"], values="Revenue",
                      color="Revenue", color_continuous_scale="Teal",
                      hover_data={"Revenue": ":$,.0f"})
    fig5.update_traces(textfont_size=13,
                       texttemplate="<b>%{label}</b><br>$%{value:,.0f}")
    apply_pie_layout(fig5,
                     title="Chart 1.5 — Treemap: Revenue by Category & Sub-Category",
                     height=500)
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 2 – REGIONAL ANALYSIS
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">🌍 Regional Performance Analysis</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # Chart 2.1
    with c1:
        reg_rev = (df.groupby("Region")["Revenue"]
                     .sum().reset_index()
                     .sort_values("Revenue", ascending=False))
        fig = px.bar(reg_rev, x="Region", y="Revenue",
                     color="Region", color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate="$%{y:,.0f}", textposition="outside",
                          textfont_size=11, marker_line_width=0)
        apply_layout(fig,
                     title="Chart 2.1 — Total Revenue by Region",
                     xlabel="Sales Region",
                     ylabel="Total Revenue (USD)",
                     ytickformat="$,.0f",
                     show_legend=False)
        fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # Chart 2.2
    with c2:
        reg_cnt = df["Region"].value_counts().reset_index()
        reg_cnt.columns = ["Region", "Orders"]
        fig2 = px.pie(reg_cnt, values="Orders", names="Region",
                      color_discrete_sequence=PALETTE)
        fig2.update_traces(textposition="inside",
                           textinfo="percent+label+value",
                           textfont_size=11,
                           marker=dict(line=dict(color="white", width=2)))
        apply_pie_layout(fig2, title="Chart 2.2 — Order Distribution by Region")
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 2.3
    reg_multi = df.groupby("Region")[["Revenue","Profit","Unit_Price"]].sum().reset_index()
    reg_melt  = reg_multi.melt(id_vars="Region", var_name="Metric", value_name="Value")
    fig3 = px.bar(reg_melt, x="Region", y="Value", color="Metric",
                  barmode="group", color_discrete_sequence=PALETTE)
    apply_layout(fig3,
                 title="Chart 2.3 — Region-wise Revenue, Profit & Unit Price",
                 xlabel="Sales Region",
                 ylabel="Value (USD)",
                 ytickformat="$,.0f")
    st.plotly_chart(fig3, use_container_width=True)

    # Chart 2.4
    pivot      = df.pivot_table(values="Revenue", index="Region",
                                columns="Category", aggfunc="sum").reset_index()
    pivot_melt = pivot.melt(id_vars="Region", var_name="Category", value_name="Revenue")
    fig4 = px.bar(pivot_melt, x="Region", y="Revenue", color="Category",
                  color_discrete_sequence=PALETTE)
    apply_layout(fig4,
                 title="Chart 2.4 — Stacked Revenue by Region & Category",
                 xlabel="Sales Region",
                 ylabel="Total Revenue (USD)",
                 ytickformat="$,.0f")
    st.plotly_chart(fig4, use_container_width=True)

    c3, c4 = st.columns(2)

    # Chart 2.5
    with c3:
        reg_profit = df.groupby("Region")["Profit"].sum().reset_index()
        fig5 = px.pie(reg_profit, values="Profit", names="Region",
                      hole=0.42, color_discrete_sequence=PALETTE)
        fig5.update_traces(textposition="outside",
                           textinfo="percent+label",
                           textfont_size=11,
                           marker=dict(line=dict(color="white", width=2)))
        apply_pie_layout(fig5, title="Chart 2.5 — Profit Contribution by Region")
        st.plotly_chart(fig5, use_container_width=True)

    # Chart 2.6
    with c4:
        reg_qty = df.groupby("Region")["Quantity"].sum().reset_index()
        fig6 = px.bar(reg_qty, x="Region", y="Quantity",
                      color="Region", color_discrete_sequence=PALETTE)
        fig6.update_traces(texttemplate="%{y:,.0f}", textposition="outside",
                           textfont_size=11, marker_line_width=0)
        apply_layout(fig6,
                     title="Chart 2.6 — Total Units Sold by Region",
                     xlabel="Sales Region",
                     ylabel="Total Units Sold",
                     ytickformat=",.0f",
                     show_legend=False)
        fig6.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig6, use_container_width=True)

    # Chart 2.7
    fig7 = px.sunburst(df, path=["Region","Category","Sub_Category"],
                       values="Revenue",
                       color_discrete_sequence=PALETTE)
    apply_pie_layout(fig7,
                     title="Chart 2.7 — Sunburst: Revenue Hierarchy  Region → Category → Sub-Category",
                     height=640)
    st.plotly_chart(fig7, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 – TIME SERIES
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">📈 Time-Series &amp; Trend Analysis</div>',
                unsafe_allow_html=True)

    # Chart 3.1
    daily = df.groupby("Order_Date")["Revenue"].sum().reset_index()
    fig = px.line(daily, x="Order_Date", y="Revenue",
                  color_discrete_sequence=["#1A6B8A"])
    fig.update_traces(line_width=2)
    apply_layout(fig,
                 title="Chart 3.1 — Daily Revenue Trend Over Time",
                 xlabel="Order Date",
                 ylabel="Daily Revenue (USD)",
                 ytickformat="$,.0f")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    # Chart 3.2
    with c1:
        monthly = df.groupby(["Year","Month","Month_Name"])["Revenue"].sum().reset_index()
        monthly = monthly.sort_values(["Year","Month"])
        monthly["Period"] = monthly["Month_Name"] + " " + monthly["Year"].astype(str)
        fig2 = px.bar(monthly, x="Period", y="Revenue", color="Year",
                      color_discrete_sequence=["#1A6B8A","#F4A261"])
        fig2.update_traces(texttemplate="$%{y:,.0f}", textposition="outside",
                           textfont_size=9)
        apply_layout(fig2,
                     title="Chart 3.2 — Monthly Revenue by Year",
                     xlabel="Month",
                     ylabel="Revenue (USD)",
                     ytickformat="$,.0f",
                     x_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 3.3
    with c2:
        quarterly = df.groupby("Quarter")["Revenue"].sum().reset_index()
        fig3 = px.bar(quarterly, x="Quarter", y="Revenue",
                      color="Revenue", color_continuous_scale="Teal")
        fig3.update_traces(texttemplate="$%{y:,.0f}", textposition="outside",
                           textfont_size=9)
        apply_layout(fig3,
                     title="Chart 3.3 — Quarterly Revenue",
                     xlabel="Quarter",
                     ylabel="Revenue (USD)",
                     ytickformat="$,.0f",
                     show_legend=False,
                     x_tickangle=-30)
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 3.4
    monthly_cat = df.groupby(["Month","Category"])["Revenue"].sum().reset_index()
    fig4 = px.line(monthly_cat, x="Month", y="Revenue", color="Category",
                   color_discrete_sequence=PALETTE, markers=True)
    apply_layout(fig4,
                 title="Chart 3.4 — Monthly Revenue Trend by Category",
                 xlabel="Month",
                 ylabel="Monthly Revenue (USD)",
                 ytickformat="$,.0f",
                 xrange=[0.5, 12.5])
    fig4.update_xaxes(tickvals=list(range(1,13)), ticktext=MONTH_LABELS)
    st.plotly_chart(fig4, use_container_width=True)

    # Chart 3.5
    yoy = df.groupby(["Month","Year"])["Revenue"].sum().reset_index()
    yoy["Year"] = yoy["Year"].astype(str)
    fig5 = px.line(yoy, x="Month", y="Revenue", color="Year",
                   color_discrete_sequence=["#0B2545","#F4A261"],
                   markers=True)
    apply_layout(fig5,
                 title="Chart 3.5 — Year-over-Year Monthly Revenue (2023 vs 2024)",
                 xlabel="Month",
                 ylabel="Monthly Revenue (USD)",
                 ytickformat="$,.0f",
                 xrange=[0.5, 12.5])
    fig5.update_xaxes(tickvals=list(range(1,13)), ticktext=MONTH_LABELS)
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 4 – PRODUCT RANKINGS
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🏆 Top Products &amp; Rankings</div>',
                unsafe_allow_html=True)

    n = st.slider("Number of products to display", 5, 20, 10)

    c1, c2 = st.columns(2)

    # Chart 4.1
    with c1:
        top_rev = (df.groupby("Product_Name")["Revenue"]
                     .sum().sort_values(ascending=False).head(n).reset_index())
        fig = px.bar(top_rev, x="Revenue", y="Product_Name",
                     orientation="h",
                     color="Revenue", color_continuous_scale="Teal")
        fig.update_traces(texttemplate="$%{x:,.0f}", textposition="outside",
                          textfont_size=9)
        apply_layout(fig,
                     title=f"Chart 4.1 — Top {n} Products by Revenue",
                     xlabel="Total Revenue (USD)",
                     ylabel="",
                     xtickformat="$,.0f",
                     height=440,
                     show_legend=False)
        fig.update_yaxes(autorange="reversed", tickfont_size=10)
        fig.update_xaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # Chart 4.2
    with c2:
        top_prof = (df.groupby("Product_Name")["Profit"]
                      .sum().sort_values(ascending=False).head(n).reset_index())
        fig2 = px.bar(top_prof, x="Profit", y="Product_Name",
                      orientation="h",
                      color="Profit", color_continuous_scale="Oranges")
        fig2.update_traces(texttemplate="$%{x:,.0f}", textposition="outside",
                           textfont_size=9)
        apply_layout(fig2,
                     title=f"Chart 4.2 — Top {n} Products by Profit",
                     xlabel="Total Profit (USD)",
                     ylabel="",
                     xtickformat="$,.0f",
                     height=440,
                     show_legend=False)
        fig2.update_yaxes(autorange="reversed", tickfont_size=10)
        fig2.update_xaxes(rangemode="tozero")
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 4.3
    top_margin = (df.groupby("Product_Name")["Profit_Margin"]
                    .mean().sort_values(ascending=False).head(n).reset_index())
    fig3 = px.bar(top_margin, x="Profit_Margin", y="Product_Name",
                  orientation="h",
                  color="Profit_Margin", color_continuous_scale="Viridis")
    fig3.update_traces(texttemplate="%{x:.1f}%", textposition="outside",
                       textfont_size=9)
    apply_layout(fig3,
                 title=f"Chart 4.3 — Top {n} Products by Average Profit Margin",
                 xlabel="Average Profit Margin (%)",
                 ylabel="",
                 height=420,
                 show_legend=False)
    fig3.update_xaxes(ticksuffix="%", rangemode="tozero")
    fig3.update_yaxes(autorange="reversed", tickfont_size=10)
    st.plotly_chart(fig3, use_container_width=True)

    # Chart 4.4
    bottom_rev = (df.groupby("Product_Name")["Revenue"]
                    .sum().sort_values().head(n).reset_index())
    fig4 = px.bar(bottom_rev, x="Revenue", y="Product_Name",
                  orientation="h",
                  color="Revenue", color_continuous_scale="Reds")
    fig4.update_traces(texttemplate="$%{x:,.0f}", textposition="outside",
                       textfont_size=9)
    apply_layout(fig4,
                 title=f"Chart 4.4 — Bottom {n} Products by Revenue (Under-Performers)",
                 xlabel="Total Revenue (USD)",
                 ylabel="",
                 xtickformat="$,.0f",
                 height=420,
                 show_legend=False)
    fig4.update_xaxes(rangemode="tozero")
    fig4.update_yaxes(tickfont_size=10)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 5 – DISTRIBUTIONS
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">📊 Statistical Distribution Analysis</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # Chart 5.1
    with c1:
        mean_r, median_r = df["Revenue"].mean(), df["Revenue"].median()
        fig = px.histogram(df, x="Revenue", nbins=60,
                           color_discrete_sequence=["#1A6B8A"], opacity=0.88)
        fig.add_vline(x=mean_r,   line_dash="dash",  line_color="#E76F51",
                      annotation_text=f"Mean  ${mean_r:,.0f}",
                      annotation_font_size=10, annotation_position="top right")
        fig.add_vline(x=median_r, line_dash="dot",   line_color="#2ECC9A",
                      annotation_text=f"Median ${median_r:,.0f}",
                      annotation_font_size=10, annotation_position="top left")
        apply_layout(fig,
                     title="Chart 5.1 — Revenue Distribution (Histogram)",
                     xlabel="Revenue per Order (USD)",
                     ylabel="Number of Orders (Frequency)",
                     xtickformat="$,.0f",
                     show_legend=False)
        fig.update_xaxes(rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)

    # Chart 5.2
    with c2:
        mean_p, median_p = df["Profit"].mean(), df["Profit"].median()
        fig2 = px.histogram(df, x="Profit", nbins=60,
                            color_discrete_sequence=["#2ECC9A"], opacity=0.88)
        fig2.add_vline(x=mean_p,   line_dash="dash",  line_color="#E76F51",
                       annotation_text=f"Mean  ${mean_p:,.0f}",
                       annotation_font_size=10, annotation_position="top right")
        fig2.add_vline(x=median_p, line_dash="dot",   line_color="#1A6B8A",
                       annotation_text=f"Median ${median_p:,.0f}",
                       annotation_font_size=10, annotation_position="top left")
        apply_layout(fig2,
                     title="Chart 5.2 — Profit Distribution (Histogram)",
                     xlabel="Profit per Order (USD)",
                     ylabel="Number of Orders (Frequency)",
                     xtickformat="$,.0f",
                     show_legend=False)
        fig2.update_xaxes(rangemode="tozero")
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 5.3
    fig3 = px.box(df, x="Category", y="Profit", color="Category",
                  color_discrete_sequence=PALETTE, points=False)
    apply_layout(fig3,
                 title="Chart 5.3 — Profit Distribution by Category (Box Plot)",
                 xlabel="Product Category",
                 ylabel="Profit per Order (USD)",
                 ytickformat="$,.0f",
                 show_legend=False)
    st.plotly_chart(fig3, use_container_width=True)

    c3, c4 = st.columns(2)

    # Chart 5.4
    with c3:
        fig4 = px.violin(df, x="Region", y="Revenue", color="Region",
                         color_discrete_sequence=PALETTE, box=True, points=False)
        apply_layout(fig4,
                     title="Chart 5.4 — Revenue Distribution by Region (Violin)",
                     xlabel="Sales Region",
                     ylabel="Revenue per Order (USD)",
                     ytickformat="$,.0f",
                     show_legend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # Chart 5.5 – Seaborn KDE
    with c4:
        fig5, ax5 = plt.subplots(figsize=(7, 4.3))
        for cat, color in zip(df["Category"].unique(), PALETTE):
            sns.kdeplot(df[df["Category"] == cat]["Revenue"],
                        ax=ax5, label=cat, fill=True, alpha=0.32, color=color)
        ax5.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax5.set_xlabel("Revenue per Order (USD)", fontsize=LABEL_FONT)
        ax5.set_ylabel("Density", fontsize=LABEL_FONT)
        ax5.set_title("Chart 5.5 — Revenue Density by Category (KDE)",
                      fontsize=TITLE_FONT, fontweight="bold",
                      color=TITLE_COLOR, pad=10)
        ax5.tick_params(axis="both", labelsize=TICK_FONT)
        ax5.set_xlim(left=0)
        ax5.legend(title="Category", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

    # Chart 5.6
    sample_df = df.sample(min(3000, len(df)), random_state=42)
    fig6 = px.strip(sample_df, x="Category", y="Profit", color="Category",
                    color_discrete_sequence=PALETTE)
    apply_layout(fig6,
                 title="Chart 5.6 — Profit Strip Plot by Category (3,000 sample)",
                 xlabel="Product Category",
                 ylabel="Profit per Order (USD)",
                 ytickformat="$,.0f",
                 show_legend=False)
    st.plotly_chart(fig6, use_container_width=True)

    # Chart 5.7
    fig7 = px.histogram(df, x="Quantity", nbins=11,
                        color_discrete_sequence=["#2563A8"],
                        opacity=0.88, text_auto=True)
    apply_layout(fig7,
                 title="Chart 5.7 — Order Quantity Distribution",
                 xlabel="Quantity Ordered",
                 ylabel="Number of Orders (Frequency)",
                 ytickformat=",.0f",
                 show_legend=False)
    fig7.update_xaxes(tickvals=list(range(1,12)),
                      ticktext=[str(i) for i in range(1,12)],
                      range=[0.5, 11.5])
    st.plotly_chart(fig7, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 6 – CORRELATIONS
# ══════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-header">🔗 Correlation &amp; Relationship Analysis</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    sample_sc = df.sample(min(5000, len(df)), random_state=42)

    # Chart 6.1
    with c1:
        fig = px.scatter(sample_sc, x="Revenue", y="Profit",
                         color="Category",
                         color_discrete_sequence=PALETTE, opacity=0.50)
        apply_layout(fig,
                     title="Chart 6.1 — Revenue vs Profit Scatter (5,000 sample)",
                     xlabel="Revenue per Order (USD)",
                     ylabel="Profit per Order (USD)",
                     xtickformat="$,.0f",
                     ytickformat="$,.0f")
        st.plotly_chart(fig, use_container_width=True)

    # Chart 6.2 – Seaborn heatmap
    with c2:
        num_cols = ["Quantity","Unit_Price","Revenue","Profit","Profit_Margin"]
        corr_mat = df[num_cols].corr()
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr_mat, annot=True, fmt=".2f", cmap="coolwarm",
                    linewidths=0.6, ax=ax2,
                    annot_kws={"size": 11, "weight": "bold"},
                    square=True, cbar_kws={"shrink": 0.82})
        ax2.set_title("Chart 6.2 — Correlation Heatmap (Pearson r)",
                      fontsize=TITLE_FONT, fontweight="bold",
                      color=TITLE_COLOR, pad=10)
        ax2.tick_params(axis="both", labelsize=TICK_FONT)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # Chart 6.3
    fig3 = px.scatter(sample_sc, x="Quantity", y="Revenue",
                      color="Region", size="Profit", size_max=16,
                      color_discrete_sequence=PALETTE, opacity=0.60)
    apply_layout(fig3,
                 title="Chart 6.3 — Quantity vs Revenue by Region (Bubble size = Profit)",
                 xlabel="Quantity Ordered",
                 ylabel="Revenue per Order (USD)",
                 ytickformat="$,.0f",
                 xrange=[0.5, 11.5])
    fig3.update_xaxes(tickvals=list(range(1,12)),
                      ticktext=[str(i) for i in range(1,12)])
    st.plotly_chart(fig3, use_container_width=True)

    # Chart 6.4 – Seaborn Pairplot
    st.markdown("#### Chart 6.4 — Pairplot: Quantity · Unit Price · Revenue · Profit")
    pair_sample = df[["Quantity","Unit_Price","Revenue","Profit","Category"]].sample(
        min(2000, len(df)), random_state=42)
    cat_palette = dict(zip(df["Category"].unique(), PALETTE[:df["Category"].nunique()]))
    pair_fig = sns.pairplot(pair_sample, hue="Category",
                            palette=cat_palette,
                            diag_kind="kde",
                            plot_kws={"alpha": 0.35, "s": 12})
    pair_fig.fig.patch.set_facecolor(PAPER_BG)
    for ax in pair_fig.axes.flatten():
        if ax:
            ax.set_facecolor(CHART_BG)
            ax.tick_params(labelsize=9)
    pair_fig.fig.suptitle("Chart 6.4 — Pairplot: Numeric Variables by Category",
                          y=1.02, fontsize=TITLE_FONT,
                          fontweight="bold", color=TITLE_COLOR)
    st.pyplot(pair_fig.fig)
    plt.close()

    # Chart 6.5
    prod_bubble = df.groupby("Product_Name").agg(
        Avg_Price  =("Unit_Price",    "mean"),
        Avg_Margin =("Profit_Margin", "mean"),
        Total_Rev  =("Revenue",       "sum"),
    ).reset_index()
    fig4 = px.scatter(prod_bubble, x="Avg_Price", y="Avg_Margin",
                      size="Total_Rev", hover_name="Product_Name",
                      color="Avg_Margin", color_continuous_scale="Viridis",
                      size_max=45)
    apply_layout(fig4,
                 title="Chart 6.5 — Unit Price vs Profit Margin (Bubble size = Revenue)",
                 xlabel="Average Unit Price (USD)",
                 ylabel="Average Profit Margin (%)",
                 xtickformat="$,.0f",
                 height=500)
    fig4.update_yaxes(ticksuffix="%")
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# TAB 7 – FORECAST
# ══════════════════════════════════════════════════════════════
with tab7:
    st.markdown('''<div class="section-header">📉 Revenue Forecast — ARIMA & Trend Models</div>''',
                unsafe_allow_html=True)

    import warnings as _warn
    _warn.filterwarnings("ignore")

    # ── helpers ───────────────────────────────────────────────
    def _make_monthly(data):
        m = data.groupby(["Year","Month"])["Revenue"].sum().reset_index()
        m["ds"] = pd.to_datetime(m[["Year","Month"]].assign(day=1)
                                   .rename(columns={"Year":"year","Month":"month","day":"day"}))
        m = m.sort_values("ds").rename(columns={"Revenue":"y"})
        return m[["ds","y"]]

    def _arima_forecast(series_df, periods):
        """Simple differencing-based ARIMA(1,1,1)-style forecast."""
        y = series_df["y"].values.astype(float)
        # First-order differencing
        d = np.diff(y)
        # AR(1) on differenced series
        if len(d) > 1:
            ar_coef = np.corrcoef(d[:-1], d[1:])[0,1]
        else:
            ar_coef = 0.0
        ar_coef = np.clip(ar_coef, -0.95, 0.95)
        # Forecast
        last_val  = y[-1]
        last_diff = d[-1] if len(d) > 0 else 0
        preds = []
        cur_val  = last_val
        cur_diff = last_diff
        for _ in range(periods):
            next_diff = ar_coef * cur_diff
            next_val  = cur_val + next_diff
            preds.append(max(next_val, 0))
            cur_diff = next_diff
            cur_val  = next_val
        # Confidence interval ±1 std of residuals
        residuals = d - ar_coef * np.roll(d, 1)
        sigma     = np.std(residuals) if len(residuals) > 1 else np.std(y) * 0.1
        lo = [max(v - 1.5 * sigma, 0) for v in preds]
        hi = [v + 1.5 * sigma           for v in preds]
        return preds, lo, hi

    def _future_dates(last_date, periods):
        return [last_date + pd.DateOffset(months=i+1) for i in range(periods)]

    def _growth_badge(pct):
        if pct > 0:
            return f"<span style='background:#1d6b3a;color:#5ef59a;border-radius:6px;padding:2px 8px;font-size:12px;'>▲ +{pct:.1f}%</span>"
        return f"<span style='background:#6b1d1d;color:#ff8080;border-radius:6px;padding:2px 8px;font-size:12px;'>▼ {pct:.1f}%</span>"

    CHART_BG_F  = "#EAF2F8"
    PAPER_BG_F  = "#F4F9FF"
    GRID_F      = "#C5D8E8"
    AXIS_F      = "#2C3E50"
    TITLE_F     = "#0B2545"

    def _base_layout(fig, title, xlabel, ylabel, height=420):
        fig.update_layout(
            title=dict(text=title, font=dict(size=15, color=TITLE_F, family="Arial Bold"), x=0),
            plot_bgcolor=CHART_BG_F, paper_bgcolor=PAPER_BG_F,
            height=height, margin=dict(t=70, b=60, l=74, r=44),
            legend=dict(bgcolor="rgba(255,255,255,0.85)", bordercolor=GRID_F, borderwidth=1),
            xaxis=dict(title=xlabel, showline=True, linecolor=AXIS_F, linewidth=1.5,
                       gridcolor=GRID_F, gridwidth=0.8, tickfont_size=11,
                       title_font=dict(size=12, color=AXIS_F)),
            yaxis=dict(title=ylabel, showline=True, linecolor=AXIS_F, linewidth=1.5,
                       gridcolor=GRID_F, gridwidth=0.8, tickfont_size=11,
                       tickformat="$,.0f", title_font=dict(size=12, color=AXIS_F)),
            font=dict(family="Arial", color=AXIS_F),
        )
        return fig

    # ── Forecast controls ─────────────────────────────────────
    _fc1, _fc2, _fc3 = st.columns([1, 1, 2])
    with _fc1:
        forecast_months = st.slider("⏱️ Forecast horizon (months)", 1, 12, 6)
    with _fc2:
        forecast_cat = st.selectbox("🏷️ Category to forecast",
                                    ["All Categories"] + sorted(df["Category"].unique().tolist()))
    with _fc3:
        st.markdown(
            "<div style='background:#EAF2F8;border-radius:10px;padding:10px 16px;"
            "border-left:4px solid #1A6B8A;font-size:12px;color:#0B2545;'>"
            "ℹ️ <b>Method:</b> ARIMA(1,1,1) — uses historical monthly revenue to forecast future months. "
            "Confidence band = ±1.5 std of model residuals.</div>",
            unsafe_allow_html=True,
        )

    # Filter by category if needed
    _fdf = df if forecast_cat == "All Categories" else df[df["Category"] == forecast_cat]
    _monthly = _make_monthly(_fdf)

    if len(_monthly) < 4:
        st.warning("⚠️ Not enough data to forecast. Select more years or a broader category.")
        st.stop()

    preds, lo, hi = _arima_forecast(_monthly, forecast_months)
    fut_dates     = _future_dates(_monthly["ds"].iloc[-1], forecast_months)

    # ── KPI strip ─────────────────────────────────────────────
    _k1, _k2, _k3, _k4 = st.columns(4)
    last_actual = _monthly["y"].iloc[-1]
    first_pred  = preds[0]
    total_pred  = sum(preds)
    growth_pct  = (preds[-1] - last_actual) / last_actual * 100 if last_actual else 0

    _k1.metric("📅 Last Actual Month",  f"${last_actual:,.0f}")
    _k2.metric("🔮 Next Month Forecast", f"${first_pred:,.0f}",
               f"{(first_pred-last_actual)/last_actual*100:+.1f}%")
    _k3.metric(f"💰 Total {forecast_months}-Month Forecast", f"${total_pred:,.0f}")
    _k4.metric("📈 End-Period vs Now",
               f"${preds[-1]:,.0f}", f"{growth_pct:+.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # Chart F.1 – Historical + Forecast line with CI band
    # ════════════════════════════════════════════════════════
    _hist_trace = go.Scatter(
        x=_monthly["ds"], y=_monthly["y"],
        mode="lines+markers", name="Historical Revenue",
        line=dict(color="#1A6B8A", width=2.5),
        marker=dict(size=5, color="#1A6B8A"),
    )
    _pred_trace = go.Scatter(
        x=fut_dates, y=preds,
        mode="lines+markers", name="Forecast",
        line=dict(color="#F4A261", width=2.5, dash="dash"),
        marker=dict(size=7, color="#F4A261", symbol="diamond"),
    )
    _band_upper = go.Scatter(
        x=fut_dates, y=hi, mode="lines",
        line=dict(width=0), showlegend=False,
        name="Upper CI",
    )
    _band_lower = go.Scatter(
        x=fut_dates, y=lo, mode="lines",
        fill="tonexty",
        fillcolor="rgba(244,162,97,0.18)",
        line=dict(width=0), showlegend=True,
        name="95% Confidence Band",
    )
    _fig_f1 = go.Figure(data=[_hist_trace, _band_upper, _band_lower, _pred_trace])
    _base_layout(_fig_f1,
                 f"Chart F.1 — Revenue Forecast: Next {forecast_months} Months ({forecast_cat})",
                 "Date", "Monthly Revenue (USD)", height=450)
    # vertical divider at forecast start
    _vline_x1 = _monthly["ds"].iloc[-1].strftime("%Y-%m-%d")
    _fig_f1.add_shape(type="line", xref="x", yref="paper",
                      x0=_vline_x1, x1=_vline_x1, y0=0, y1=1,
                      line=dict(color="#E76F51", width=1.5, dash="dot"))
    _fig_f1.add_annotation(x=_vline_x1, yref="paper", y=0.98,
                            text="Forecast Start", showarrow=False,
                            font=dict(color="#E76F51", size=11),
                            xanchor="left", bgcolor="rgba(255,255,255,0.7)",
                            bordercolor="#E76F51", borderwidth=1)
    st.plotly_chart(_fig_f1, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # Chart F.2 – Forecast bar chart (future only)
    # ════════════════════════════════════════════════════════
    _pred_labels = [d.strftime("%b %Y") for d in fut_dates]
    _fig_f2 = go.Figure()
    _fig_f2.add_trace(go.Bar(
        x=_pred_labels, y=preds,
        name="Forecasted Revenue",
        marker_color="#F4A261",
        error_y=dict(
            type="data", symmetric=False,
            array=[h - p for h, p in zip(hi, preds)],
            arrayminus=[p - l for p, l in zip(preds, lo)],
            color="#E76F51", thickness=1.5, width=5,
        ),
        text=[f"${v:,.0f}" for v in preds],
        textposition="outside", textfont_size=10,
    ))
    _base_layout(_fig_f2,
                 f"Chart F.2 — Monthly Forecasted Revenue with Confidence Intervals",
                 "Month", "Forecasted Revenue (USD)", height=420)
    _fig_f2.update_layout(showlegend=False)
    st.plotly_chart(_fig_f2, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # Chart F.3 – Category-wise forecast comparison
    # ════════════════════════════════════════════════════════
    st.markdown(
        '<div class="section-header">📊 Category-wise Forecast Comparison</div>',
        unsafe_allow_html=True,
    )
    _cats  = sorted(df["Category"].unique().tolist())
    _fdata = []
    for _cat in _cats:
        _cdf = _make_monthly(df[df["Category"] == _cat])
        if len(_cdf) < 4:
            continue
        _cp, _, _ = _arima_forecast(_cdf, forecast_months)
        _fdata.append({
            "Category": _cat,
            "Forecast_Total": sum(_cp),
            "Last_Actual":    _cdf["y"].iloc[-1],
            "Next_Month":     _cp[0],
            "Growth_Pct":     (_cp[-1] - _cdf["y"].iloc[-1]) / _cdf["y"].iloc[-1] * 100
                              if _cdf["y"].iloc[-1] else 0,
        })
    _fdf2 = pd.DataFrame(_fdata)

    _c1f, _c2f = st.columns(2)

    with _c1f:
        _fig_f3 = px.bar(
            _fdf2, x="Category", y="Forecast_Total",
            color="Category", color_discrete_sequence=PALETTE,
            text="Forecast_Total",
        )
        _fig_f3.update_traces(
            texttemplate="$%{text:,.0f}", textposition="outside", textfont_size=10,
            marker_line_width=0,
        )
        _base_layout(_fig_f3,
                     f"Chart F.3 — Total {forecast_months}-Month Forecast by Category",
                     "Category", "Forecasted Revenue (USD)")
        _fig_f3.update_layout(showlegend=False)
        _fig_f3.update_yaxes(rangemode="tozero")
        st.plotly_chart(_fig_f3, use_container_width=True)

    with _c2f:
        _fig_f4 = px.bar(
            _fdf2, x="Category", y="Growth_Pct",
            color="Growth_Pct",
            color_continuous_scale=["#E76F51","#F4A261","#2ECC9A"],
            text="Growth_Pct",
        )
        _fig_f4.update_traces(
            texttemplate="%{text:.1f}%", textposition="outside", textfont_size=10,
        )
        _base_layout(_fig_f4,
                     f"Chart F.4 — Forecast Growth % by Category (vs Last Actual)",
                     "Category", "Growth Rate (%)")
        _fig_f4.update_yaxes(ticksuffix="%")
        _fig_f4.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(_fig_f4, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # Chart F.5 – Region-wise forecast
    # ════════════════════════════════════════════════════════
    st.markdown(
        '<div class="section-header">🌍 Region-wise Forecast Comparison</div>',
        unsafe_allow_html=True,
    )
    _regs   = sorted(df["Region"].unique().tolist())
    _rdata  = []
    for _reg in _regs:
        _rdf = _make_monthly(df[df["Region"] == _reg])
        if len(_rdf) < 4:
            continue
        _rp, _rl, _rh = _arima_forecast(_rdf, forecast_months)
        _rdata.append({
            "Region": _reg,
            "Forecast_Total": sum(_rp),
            "Last_Actual":    _rdf["y"].iloc[-1],
            "Next_Month":     _rp[0],
            "Growth_Pct":     (_rp[-1] - _rdf["y"].iloc[-1]) / _rdf["y"].iloc[-1] * 100
                              if _rdf["y"].iloc[-1] else 0,
        })
    _rdf2 = pd.DataFrame(_rdata)

    _c3f, _c4f = st.columns(2)

    with _c3f:
        _fig_f5 = px.bar(
            _rdf2, x="Region", y="Forecast_Total",
            color="Region", color_discrete_sequence=PALETTE,
            text="Forecast_Total",
        )
        _fig_f5.update_traces(
            texttemplate="$%{text:,.0f}", textposition="outside", textfont_size=10,
            marker_line_width=0,
        )
        _base_layout(_fig_f5,
                     f"Chart F.5 — Total {forecast_months}-Month Forecast by Region",
                     "Region", "Forecasted Revenue (USD)")
        _fig_f5.update_layout(showlegend=False)
        _fig_f5.update_yaxes(rangemode="tozero")
        st.plotly_chart(_fig_f5, use_container_width=True)

    with _c4f:
        _fig_f6 = px.pie(
            _rdf2, names="Region", values="Forecast_Total",
            hole=0.50, color_discrete_sequence=PALETTE,
        )
        _fig_f6.update_traces(
            textinfo="percent+label", textfont_size=12,
            marker=dict(line=dict(color="white", width=2)),
        )
        _fig_f6.update_layout(
            title=dict(text=f"Chart F.6 — Forecast Revenue Share by Region",
                       font=dict(size=15, color=TITLE_F), x=0),
            paper_bgcolor=PAPER_BG_F, height=420,
            margin=dict(t=70, b=44, l=22, r=22),
            legend=dict(bgcolor="rgba(255,255,255,0.85)"),
        )
        st.plotly_chart(_fig_f6, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # Chart F.7 – Multi-category forecast lines over time
    # ════════════════════════════════════════════════════════
    st.markdown(
        '<div class="section-header">📈 Multi-Category Revenue Forecast Trends</div>',
        unsafe_allow_html=True,
    )
    _fig_f7 = go.Figure()
    for _ci, _cat in enumerate(_cats):
        _cdf = _make_monthly(df[df["Category"] == _cat])
        if len(_cdf) < 4:
            continue
        _cp, _cl, _ch = _arima_forecast(_cdf, forecast_months)
        _fd = _future_dates(_cdf["ds"].iloc[-1], forecast_months)
        # historical
        _fig_f7.add_trace(go.Scatter(
            x=_cdf["ds"], y=_cdf["y"], mode="lines",
            name=f"{_cat} (Historical)",
            line=dict(color=PALETTE[_ci % len(PALETTE)], width=1.8),
            opacity=0.6, legendgroup=_cat,
        ))
        # forecast
        _fig_f7.add_trace(go.Scatter(
            x=_fd, y=_cp, mode="lines+markers",
            name=f"{_cat} (Forecast)",
            line=dict(color=PALETTE[_ci % len(PALETTE)], width=2.5, dash="dash"),
            marker=dict(size=7, symbol="diamond"),
            legendgroup=_cat,
        ))
    _base_layout(_fig_f7,
                 f"Chart F.7 — Revenue Forecast Trends by Category (Next {forecast_months} Months)",
                 "Date", "Monthly Revenue (USD)", height=500)
    _vline_x7 = _monthly["ds"].iloc[-1].strftime("%Y-%m-%d")
    _fig_f7.add_shape(type="line", xref="x", yref="paper",
                      x0=_vline_x7, x1=_vline_x7, y0=0, y1=1,
                      line=dict(color="#E76F51", width=1.5, dash="dot"))
    _fig_f7.add_annotation(x=_vline_x7, yref="paper", y=0.98,
                            text="Forecast Start →", showarrow=False,
                            font=dict(color="#E76F51", size=11),
                            xanchor="left", bgcolor="rgba(255,255,255,0.7)",
                            bordercolor="#E76F51", borderwidth=1)
    st.plotly_chart(_fig_f7, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # Chart F.8 – Cumulative forecast
    # ════════════════════════════════════════════════════════
    _cumulative = np.cumsum(preds)
    _fig_f8 = go.Figure()
    _fig_f8.add_trace(go.Scatter(
        x=_pred_labels, y=_cumulative,
        mode="lines+markers+text",
        line=dict(color="#2ECC9A", width=2.5),
        marker=dict(size=9, color="#2ECC9A"),
        text=[f"${v:,.0f}" for v in _cumulative],
        textposition="top center", textfont_size=10,
        fill="tozeroy", fillcolor="rgba(46,204,154,0.12)",
        name="Cumulative Revenue",
    ))
    _base_layout(_fig_f8,
                 f"Chart F.8 — Cumulative Forecasted Revenue Over {forecast_months} Months ({forecast_cat})",
                 "Month", "Cumulative Revenue (USD)", height=400)
    st.plotly_chart(_fig_f8, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # Forecast data table
    # ════════════════════════════════════════════════════════
    st.markdown("#### 📋 Forecast Data Table")
    _tbl = pd.DataFrame({
        "Month":            _pred_labels,
        "Forecasted Revenue": [f"${v:,.0f}" for v in preds],
        "Lower Bound (95%)":  [f"${v:,.0f}" for v in lo],
        "Upper Bound (95%)":  [f"${v:,.0f}" for v in hi],
        "vs Last Actual":     [f"{(v-last_actual)/last_actual*100:+.1f}%" for v in preds],
    })
    st.dataframe(_tbl, use_container_width=True, hide_index=True)

    # Download button
    _csv_fc = pd.DataFrame({
        "Month": _pred_labels, "Forecast": preds, "Lower": lo, "Upper": hi
    }).to_csv(index=False)
    st.download_button(
        "⬇️ Download Forecast CSV", _csv_fc,
        f"forecast_{forecast_months}months.csv", "text/csv",
        use_container_width=False,
    )


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#5A7FA0; padding:12px 0; font-size:13px;'>
    Product Sales Dataset &nbsp;|&nbsp;
    Built with Python · Pandas · Seaborn · Plotly · Streamlit &nbsp;|&nbsp;
    🤖 AI powered by Ollama Qwen2.5 (local)
</div>
""", unsafe_allow_html=True)
