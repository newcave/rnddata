import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="K-water AI 연구소 · 데이터 인벤토리",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

def _svg_b64(path: str) -> str:
    """Return base64-encoded SVG for use in <img> tag."""
    data = Path(path).read_bytes()
    return base64.b64encode(data).decode()

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
    # ── Logo block ──────────────────────────────────────────────────────────
    logo_path = Path(__file__).parent / "kw_logo.png" #"AI_Lab_logo.jpg"
    if logo_path.exists():
        logo_b64 = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(
            f'<div style="text-align:center;padding:16px 12px 6px 12px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" '
            f'style="width:82%;max-width:170px;border-radius:8px;'
            f'box-shadow:0 0 0 3px rgba(255,255,255,0.25);" />'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div style="'
        'background:rgba(255,255,255,0.13);'
        'border-radius:8px;'
        'padding:10px 14px 10px 14px;'
        'margin:6px 8px 0 8px;'
        '">'
        '<div style="font-size:0.78rem;opacity:0.75;letter-spacing:0.04em;'
        'text-transform:uppercase;margin-bottom:2px;">K-water Research Institute</div>'
        '<div style="font-size:1.05rem;font-weight:700;letter-spacing:0.01em;">'
        '💡 연구원 R&D 인벤토리</div>'
        '<div style="font-size:0.78rem;opacity:0.7;margin-top:2px;">'
        'Data Inventory Dashboard</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div style="margin:14px 0 6px 0;border-top:1px solid rgba(255,255,255,0.2)"></div>',
                unsafe_allow_html=True)
    page = st.radio(
        "페이지 선택",
        [
            "🏠  개요 & 핵심 지표",
            "📊  크로스 리포트 매트릭스",
            "🎯  파이프라인 우선순위",
            "🔬  원본 상세 데이터",
            "🏛  연구소별 통계 (案)",
            "📈  분야별 통계",
        ],
        label_visibility="collapsed",
    )
    st.markdown(
        '<div style="margin:14px 0 6px 0;border-top:1px solid rgba(255,255,255,0.2)"></div>',
        unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.75rem;opacity:0.75;padding:0 4px'>"
        "📁 분석 보고서: <b>67건</b><br>"
        "🗂 데이터 레코드: <b>313건</b><br>"
        "🔑 고유 소스: <b>271개</b><br>"
        "🏛 연구소: <b>7개</b>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Page routing ───────────────────────────────────────────────────────────────
if   page.startswith("🏠"):
    from pages_src import p1_overview;    p1_overview.render()
elif page.startswith("📊"):
    from pages_src import p2_matrix;      p2_matrix.render()
elif page.startswith("🎯"):
    from pages_src import p3_priority;    p3_priority.render()
elif page.startswith("🔬"):
    from pages_src import p4_raw;         p4_raw.render()
elif page.startswith("🏛"):
    from pages_src import p5_institute;   p5_institute.render()
elif page.startswith("📈"):
    from pages_src import p5_stats;       p5_stats.render()
