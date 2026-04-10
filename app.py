import streamlit as st

st.set_page_config(
    page_title="K-water 데이터 인벤토리",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1F4E79 0%, #2E75B6 60%, #4472C4 100%);
    color: white;
  }
  [data-testid="stSidebar"] * { color: white !important; }
  [data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; padding: 6px 0; }
  [data-testid="stSidebar"] .stRadio div[role=radiogroup] div {
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    margin: 3px 0;
    padding: 4px 8px;
    transition: background 0.2s;
  }
  [data-testid="stSidebar"] .stRadio div[role=radiogroup] div:hover {
    background: rgba(255,255,255,0.18);
  }

  /* Metric cards */
  .kw-card {
    background: white;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 2px 12px rgba(31,78,121,0.10);
    border-left: 5px solid #2E75B6;
    margin-bottom: 10px;
  }
  .kw-card-val { font-size: 2rem; font-weight: 700; color: #1F4E79; line-height: 1.1; }
  .kw-card-lbl { font-size: 0.82rem; color: #6b7280; margin-top: 2px; }

  /* Priority badges */
  .badge-imm  { background:#C6EFCE; color:#1A7A3A; border-radius:6px; padding:2px 10px; font-weight:600; font-size:0.8rem; }
  .badge-pln  { background:#FFEB9C; color:#7A5A00; border-radius:6px; padding:2px 10px; font-weight:600; font-size:0.8rem; }
  .badge-opt  { background:#FCE4D6; color:#7A2A00; border-radius:6px; padding:2px 10px; font-weight:600; font-size:0.8rem; }
  .badge-open { background:#D9F2E6; color:#155724; border-radius:6px; padding:2px 8px; font-size:0.75rem; }
  .badge-int  { background:#FFE0E0; color:#7B1A1A; border-radius:6px; padding:2px 8px; font-size:0.75rem; }
  .badge-res  { background:#FFF4CC; color:#7A5A00; border-radius:6px; padding:2px 8px; font-size:0.75rem; }

  /* Section title */
  .section-title {
    font-size: 1.1rem; font-weight: 700; color: #1F4E79;
    border-bottom: 2px solid #2E75B6; padding-bottom: 6px; margin: 16px 0 10px;
  }

  /* Page header */
  .page-header {
    background: linear-gradient(90deg, #1F4E79, #2E75B6);
    color: white; border-radius: 10px;
    padding: 18px 24px; margin-bottom: 20px;
  }
  .page-header h2 { margin: 0; font-size: 1.4rem; }
  .page-header p  { margin: 4px 0 0; font-size: 0.88rem; opacity: 0.88; }

  /* Dataframe tweaks */
  .stDataFrame { border-radius: 8px; overflow: hidden; }

  /* Divider */
  hr { border: none; border-top: 1px solid #e5e7eb; margin: 16px 0; }

  /* Hide default Streamlit header */
  #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar nav ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💧 K-water\n**데이터 인벤토리**")
    st.markdown("---")
    page = st.radio(
        "페이지 선택",
        [
            "🏠  개요 & 핵심 지표",
            "📊  크로스 리포트 매트릭스",
            "🎯  파이프라인 우선순위",
            "🔬  원본 상세 데이터",
            "📈  분야별 통계",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;opacity:0.75;'>"
        "📁 분석 보고서: <b>67건</b><br>"
        "🗂 데이터 레코드: <b>313건</b><br>"
        "🔑 고유 소스: <b>271개</b>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Page routing ───────────────────────────────────────────────────────────────
if   page.startswith("🏠"):
    from pages_src import p1_overview;     p1_overview.render()
elif page.startswith("📊"):
    from pages_src import p2_matrix;       p2_matrix.render()
elif page.startswith("🎯"):
    from pages_src import p3_priority;     p3_priority.render()
elif page.startswith("🔬"):
    from pages_src import p4_raw;          p4_raw.render()
elif page.startswith("📈"):
    from pages_src import p5_stats;        p5_stats.render()
