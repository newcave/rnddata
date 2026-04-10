import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .utils import load_matrix, load_raw, load_refs, page_header, metric_card, prio_badge, avail_badge

def render():
    page_header("🏠", "개요 & 핵심 지표",
                "K-water 연구보고서 67건 기반 데이터 소스 인벤토리 종합 현황")

    mdf = load_matrix()
    raw = load_raw()
    refs = load_refs()

    imm = mdf[mdf["priority"]=="Immediate"]
    pln = mdf[mdf["priority"]=="Planned"]
    opt = mdf[mdf["priority"]=="Optional"]
    int_only = mdf[mdf["availability"].str.contains("internal_only", na=False)]
    open_src = mdf[mdf["availability"]=="open"]

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    metric_card(c1, len(refs),   "분석 대상 보고서",  "#1F4E79")
    metric_card(c2, len(raw),    "데이터 레코드 (건)",  "#2E75B6")
    metric_card(c3, len(mdf),    "고유 데이터 소스",  "#4472C4")
    metric_card(c4, len(int_only),"내부 전용 소스",   "#C0392B")
    metric_card(c5, len(open_src),"공개 데이터 소스", "#1A7A3A")

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── Row 2: Donut charts ────────────────────────────────────────────────────
    col_l, col_m, col_r = st.columns(3)

    with col_l:
        st.markdown('<div class="section-title">파이프라인 우선순위 분포</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=["🔴 즉시 구축","🟡 중기 계획","🟠 검토 단계"],
            values=[len(imm), len(pln), len(opt)],
            marker_colors=["#C6EFCE","#FFEB9C","#FCE4D6"],
            textinfo="label+percent+value",
            hole=0.52,
            textfont_size=12,
        ))
        fig.update_layout(
            showlegend=False, margin=dict(t=10,b=10,l=10,r=10),
            height=240, paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_m:
        st.markdown('<div class="section-title">데이터 가용성 분포</div>', unsafe_allow_html=True)
        av_counts = raw["Data_availability"].value_counts()
        av_colors = {"open":"#D9F2E6","internal_only":"#FFE0E0","restricted":"#FFF4CC","unclear":"#E5E5E5"}
        fig2 = go.Figure(go.Pie(
            labels=av_counts.index.tolist(),
            values=av_counts.values.tolist(),
            marker_colors=[av_colors.get(k,"#ccc") for k in av_counts.index],
            textinfo="label+value",
            hole=0.52,
            textfont_size=12,
        ))
        fig2.update_layout(
            showlegend=False, margin=dict(t=10,b=10,l=10,r=10),
            height=240, paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">데이터 유형 분포</div>', unsafe_allow_html=True)
        dtype_c = raw["Data_type"].value_counts()
        colors_dtype = px.colors.sequential.Blues_r[:len(dtype_c)]
        fig3 = go.Figure(go.Pie(
            labels=dtype_c.index.tolist(),
            values=dtype_c.values.tolist(),
            marker_colors=colors_dtype,
            textinfo="label+value",
            hole=0.52,
            textfont_size=10,
        ))
        fig3.update_layout(
            showlegend=False, margin=dict(t=10,b=10,l=10,r=10),
            height=240, paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── Row 3: Top sources + Category bar ─────────────────────────────────────
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="section-title">🔝 활용 빈도 Top 10 데이터 소스</div>', unsafe_allow_html=True)
        top10 = mdf.nlargest(10, "freq")[["acronym","data_name","freq","priority","availability"]]
        color_map = {"Immediate":"#C6EFCE","Planned":"#FFEB9C","Optional":"#FCE4D6"}
        fig4 = go.Figure(go.Bar(
            x=top10["freq"],
            y=top10["acronym"],
            orientation="h",
            marker_color=[color_map.get(p,"#ccc") for p in top10["priority"]],
            marker_line_color="#1F4E79",
            marker_line_width=1.2,
            text=top10["freq"],
            textposition="outside",
            hovertext=top10["data_name"],
        ))
        fig4.update_layout(
            xaxis_title="활용 보고서 수", yaxis=dict(autorange="reversed"),
            margin=dict(t=10,b=30,l=10,r=40), height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#eee"),
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">📂 주제 분야별 레코드 수 (Top 12)</div>', unsafe_allow_html=True)
        cat_c = raw["Data_category"].value_counts().head(12)
        fig5 = go.Figure(go.Bar(
            x=cat_c.values,
            y=cat_c.index,
            orientation="h",
            marker_color="#4472C4",
            marker_line_color="#1F4E79",
            marker_line_width=0.8,
            text=cat_c.values,
            textposition="outside",
        ))
        fig5.update_layout(
            xaxis_title="레코드 수", yaxis=dict(autorange="reversed"),
            margin=dict(t=10,b=30,l=10,r=40), height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#eee"),
            font=dict(family="Noto Sans KR"),
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # ── 즉시 구축 카드 ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🔴 즉시 구축 대상 소스 상세</div>', unsafe_allow_html=True)
    for _, row in imm.iterrows():
        av = row["availability"].split("/")[0].strip()
        av_icon = {"open":"🟢","internal_only":"🔒","restricted":"⚠️"}.get(av,"❓")
        with st.expander(f"**{row['acronym']}** — {row['data_name']}  ·  활용 {row['freq']}건  ·  {av_icon} {av}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"**한국어 명칭:** {row['data_name_kr']}")
            c1.markdown(f"**주제 분야:** {row['category']}")
            c1.markdown(f"**데이터 유형:** {row['dtype']}")
            c1.markdown(f"**생산기관:** {row['org']}")
            c2.markdown(f"**공간 범위:** {row['spatial']}")
            c2.markdown(f"**시간 범위:** {row['temporal']}")
            c2.markdown(f"**시간 해상도:** {row['temporal_res']}")
            c2.markdown(f"**데이터 형식:** {row['fmt']}")
            st.markdown(f"**연구 활용 목적:** {row['usage']}")
            st.markdown(f"**측정 파라미터:** {row['params']}")
            if row['notes']:
                st.info(f"📝 {row['notes']}")
