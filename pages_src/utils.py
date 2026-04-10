import pandas as pd
import streamlit as st
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

@st.cache_data
def load_matrix():
    df = pd.read_csv(DATA / "matrix.csv")
    df["freq"] = pd.to_numeric(df["freq"], errors="coerce").fillna(0).astype(int)
    return df

@st.cache_data
def load_raw():
    return pd.read_csv(DATA / "raw.csv")

@st.cache_data
def load_refs():
    return pd.read_csv(DATA / "refs.csv")

# ── Shared colour helpers ──────────────────────────────────────────────────────
PRIORITY_COLOR  = {"Immediate": "#C6EFCE", "Planned": "#FFEB9C", "Optional": "#FCE4D6"}
PRIORITY_LABEL  = {"Immediate": "🔴 즉시", "Planned": "🟡 중기", "Optional": "🟠 검토"}
AVAIL_BADGE = {
    "open":         '<span class="badge-open">공개</span>',
    "internal_only":'<span class="badge-int">내부전용</span>',
    "restricted":   '<span class="badge-res">제한</span>',
}

def prio_badge(p):
    cls = {"Immediate":"badge-imm","Planned":"badge-pln","Optional":"badge-opt"}.get(p,"badge-opt")
    lbl = {"Immediate":"🔴 즉시","Planned":"🟡 중기","Optional":"🟠 검토"}.get(p, p)
    return f'<span class="{cls}">{lbl}</span>'

def avail_badge(a):
    return AVAIL_BADGE.get(str(a).strip().split("/")[0].strip(), f'<span style="font-size:.75rem">{a}</span>')

def page_header(icon, title, subtitle=""):
    st.markdown(
        f'<div class="page-header"><h2>{icon}  {title}</h2>'
        + (f'<p>{subtitle}</p>' if subtitle else '')
        + '</div>',
        unsafe_allow_html=True,
    )

def metric_card(col, value, label, color="#2E75B6"):
    col.markdown(
        f'<div class="kw-card" style="border-left-color:{color}">'
        f'<div class="kw-card-val">{value}</div>'
        f'<div class="kw-card-lbl">{label}</div></div>',
        unsafe_allow_html=True,
    )
