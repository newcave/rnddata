import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from .utils import load_matrix, page_header

_AVAIL_ICON = {
    "open":          "🟢 공개",
    "internal_only": "🔒 내부전용",
    "restricted":    "⚠️ 제한",
    "unclear":       "❓ 불명",
}
_AVAIL_BG = {
    "open": "#D9F2E6", "internal_only": "#FFE0E0",
    "restricted": "#FFF4CC", "unclear": "#F0F0F0",
}

def _avail_label(a):
    k = str(a).split("/")[0].strip()
    return _AVAIL_ICON.get(k, a)

def render():
    page_header("🎯", "파이프라인 우선순위",
                "AI 데이터 실증랩 파이프라인 구축 우선순위별 데이터 소스 상세")

    mdf = load_matrix()
    imm = mdf[mdf["priority"]=="Immediate"].sort_values("freq", ascending=False)
    pln = mdf[mdf["priority"]=="Planned"].sort_values("freq", ascending=False)
    opt = mdf[mdf["priority"]=="Optional"].sort_values("freq", ascending=False)

    # ── Summary metric row ────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 즉시 구축", f"{len(imm)}개", help="5개 이상 보고서 활용")
    c2.metric("🟡 중기 계획", f"{len(pln)}개", help="2-4개 보고서 활용")
    c3.metric("🟠 검토 단계", f"{len(opt)}개", help="1개 보고서 활용")
    c4.metric("🔒 내부 전용 전체",
              f"{len(mdf[mdf['availability'].str.contains('internal_only', na=False)])}개")
    st.markdown("---")

    # ── Bubble chart: freq vs availability ────────────────────────────────────
    st.markdown('<div class="section-title">📍 소스 우선순위 버블 차트 (빈도 × 접근성)</div>',
                unsafe_allow_html=True)

    top40 = mdf.nlargest(40, "freq")
    fig = go.Figure()
    color_p = {"Immediate":"#1A7A3A","Planned":"#7A5A00","Optional":"#7A2A00"}
    fill_p  = {"Immediate":"#C6EFCE","Planned":"#FFEB9C","Optional":"#FCE4D6"}

    for priority in ["Immediate","Planned","Optional"]:
        sub = top40[top40["priority"]==priority]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub["freq"],
            y=sub["availability"].apply(lambda a: str(a).split("/")[0].strip()),
            mode="markers+text",
            text=sub["acronym"],
            textposition="top center",
            textfont=dict(size=9, color=color_p[priority]),
            marker=dict(
                size=sub["freq"]*6+12,
                color=fill_p[priority],
                line=dict(width=1.5, color=color_p[priority]),
                opacity=0.85,
            ),
            name=priority,
            hovertemplate="<b>%{text}</b><br>빈도: %{x}<br>가용성: %{y}<extra></extra>",
        ))
    fig.update_layout(
        xaxis_title="활용 보고서 수", yaxis_title="데이터 가용성",
        height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,255,0.6)",
        margin=dict(t=10,b=40,l=60,r=20), font=dict(family="Noto Sans KR"),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0),
        xaxis=dict(gridcolor="#eee"), yaxis=dict(gridcolor="#eee"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # ── Section cards per priority ─────────────────────────────────────────────
    for prio_label, subset, header_bg, txt_color, border_color in [
        ("🔴 즉시 구축 필요 — 5건 이상 보고서 활용", imm, "#C6EFCE", "#1A7A3A", "#1A7A3A"),
        ("🟡 중기 계획 — 2~4건 보고서 활용",         pln, "#FFEB9C", "#7A5A00", "#E6A817"),
        ("🟠 검토 단계 — 1건 보고서 활용",            opt, "#FCE4D6", "#7A2A00", "#E65C00"),
    ]:
        st.markdown(
            f'<div style="background:{header_bg};border-left:5px solid {border_color};'
            f'border-radius:8px;padding:10px 16px;margin:14px 0 6px;">'
            f'<span style="font-weight:700;font-size:1.05rem;color:{txt_color}">'
            f'{prio_label}  <span style="opacity:.7">({len(subset)}개)</span></span></div>',
            unsafe_allow_html=True,
        )

        if len(subset) <= 20:
            # Show all as cards
            cols = st.columns(min(3, len(subset)))
            for i, (_, row) in enumerate(subset.iterrows()):
                av = str(row["availability"]).split("/")[0].strip()
                av_icon = _AVAIL_ICON.get(av, av)
                av_bg   = _AVAIL_BG.get(av, "#fff")
                with cols[i % 3]:
                    st.markdown(
                        f'<div style="background:white;border-radius:10px;padding:14px 16px;'
                        f'margin:5px 0;box-shadow:0 1px 8px rgba(0,0,0,0.08);'
                        f'border-top:3px solid {border_color};">'
                        f'<div style="font-weight:700;font-size:1rem;color:#1F4E79">{row["acronym"]}</div>'
                        f'<div style="font-size:0.82rem;color:#374151;margin:3px 0 6px">{row["data_name"][:55]}</div>'
                        f'<div style="display:flex;gap:6px;flex-wrap:wrap;">'
                        f'<span style="background:#EBF3FB;border-radius:5px;padding:1px 8px;font-size:0.75rem;color:#1F4E79">📋 {row["category"]}</span>'
                        f'<span style="background:{av_bg};border-radius:5px;padding:1px 8px;font-size:0.75rem">{av_icon}</span>'
                        f'<span style="background:#1F4E79;color:white;border-radius:5px;padding:1px 8px;font-size:0.75rem">📌 {row["freq"]}건</span>'
                        f'</div>'
                        f'<div style="font-size:0.78rem;color:#6b7280;margin-top:8px">{str(row["usage"])[:80]}…</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
        else:
            # Show as collapsed table for optional (254 items)
            with st.expander(f"전체 {len(subset)}개 보기"):
                disp = subset[["acronym","data_name","category","org","freq","availability"]].copy()
                disp.columns = ["약어","데이터 명칭","분야","생산기관","빈도","가용성"]
                st.dataframe(disp.reset_index(drop=True), use_container_width=True, height=400)

    # ── Pipeline roadmap visual ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🗺 파이프라인 구축 로드맵</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:10px;">
      <div style="background:#C6EFCE;border-radius:10px;padding:16px;border:1px solid #1A7A3A">
        <div style="font-weight:700;color:#1A7A3A;font-size:1rem">🔴 Phase 1 — 즉시 (0-6개월)</div>
        <ul style="font-size:0.85rem;color:#374151;margin-top:8px;padding-left:18px">
          <li>WAMIS API 연동 레이어 구축</li>
          <li>KMA 기상 데이터 수집 파이프라인</li>
          <li>RWIS 실시간 수위 스트리밍</li>
          <li>WEIS 수질 DB 통합 연계</li>
        </ul>
      </div>
      <div style="background:#FFEB9C;border-radius:10px;padding:16px;border:1px solid #E6A817">
        <div style="font-weight:700;color:#7A5A00;font-size:1rem">🟡 Phase 2 — 중기 (6-18개월)</div>
        <ul style="font-size:0.85rem;color:#374151;margin-top:8px;padding-left:18px">
          <li>ASOS / Sentinel 위성 파이프라인</li>
          <li>COSFIM 댐 운영 데이터 연동</li>
          <li>KRM 위기관리 DB 통합</li>
          <li>SWM 스마트 계량 데이터 연계</li>
        </ul>
      </div>
      <div style="background:#EBF3FB;border-radius:10px;padding:16px;border:1px solid #4472C4">
        <div style="font-weight:700;color:#1F4E79;font-size:1rem">🔵 Phase 3 — 장기 (18개월+)</div>
        <ul style="font-size:0.85rem;color:#374151;margin-top:8px;padding-left:18px">
          <li>현장 계측 IoT 스트리밍 허브</li>
          <li>AI 학습 데이터 레이블링 파이프라인</li>
          <li>연구소별 전용 데이터 포털</li>
          <li>데이터 거버넌스 체계 수립</li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)
