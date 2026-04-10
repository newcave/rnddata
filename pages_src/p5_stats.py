import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from .utils import load_raw, load_matrix, load_refs, page_header

def render():
    page_header("📈", "분야별 통계",
                "데이터 유형·주제·가용성·약어 기반 종합 통계 분석")

    raw = load_raw()
    mdf = load_matrix()
    refs = load_refs()

    # ── Tab layout ────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 유형·분야 분포", "🔒 가용성 분석", "🔠 주요 약어 현황", "📋 보고서 목록"])

    # ────────────────────────────────── TAB 1 ─────────────────────────────────
    with tab1:
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="section-title">데이터 유형별 레코드 수</div>', unsafe_allow_html=True)
            dtype_c = raw["Data_type"].value_counts()
            colors = ["#1F4E79","#2E75B6","#4472C4","#6495CC","#8AB4D8","#A8CAE4",
                      "#C2D9EE","#D6E8F5","#E8F2FA","#F0F7FD","#4472C4","#6495CC","#8AB4D8","#A8CAE4"]
            fig = go.Figure(go.Bar(
                y=dtype_c.index, x=dtype_c.values, orientation="h",
                marker_color=colors[:len(dtype_c)],
                marker_line_color="#1F4E79", marker_line_width=0.8,
                text=dtype_c.values, textposition="outside",
            ))
            fig.update_layout(
                xaxis_title="레코드 수", yaxis=dict(autorange="reversed"),
                margin=dict(t=10,b=20,l=10,r=40), height=340,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,255,0.5)",
                xaxis=dict(gridcolor="#eee"), font=dict(family="Noto Sans KR"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown('<div class="section-title">주제 분야별 레코드 수 (Top 15)</div>', unsafe_allow_html=True)
            cat_c = raw["Data_category"].value_counts().head(15)
            fig2 = go.Figure(go.Bar(
                y=cat_c.index, x=cat_c.values, orientation="h",
                marker=dict(
                    color=cat_c.values,
                    colorscale=[[0,"#D6E4F0"],[1,"#1F4E79"]],
                    showscale=False,
                ),
                marker_line_color="#2E75B6", marker_line_width=0.8,
                text=cat_c.values, textposition="outside",
            ))
            fig2.update_layout(
                xaxis_title="레코드 수", yaxis=dict(autorange="reversed"),
                margin=dict(t=10,b=20,l=10,r=40), height=340,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,255,0.5)",
                xaxis=dict(gridcolor="#eee"), font=dict(family="Noto Sans KR"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Cross-table heatmap
        st.markdown('<div class="section-title">유형 × 가용성 교차표</div>', unsafe_allow_html=True)
        cross = pd.crosstab(raw["Data_type"], raw["Data_availability"]).fillna(0).astype(int)
        fig3 = px.imshow(
            cross,
            color_continuous_scale=[[0,"#EBF3FB"],[0.5,"#4472C4"],[1,"#1F4E79"]],
            text_auto=True,
            labels=dict(x="가용성", y="데이터 유형", color="레코드 수"),
        )
        fig3.update_layout(
            margin=dict(t=10,b=10,l=10,r=10), height=300,
            paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Noto Sans KR", size=11),
            coloraxis_showscale=False,
        )
        fig3.update_traces(textfont_size=12)
        st.plotly_chart(fig3, use_container_width=True)

    # ────────────────────────────────── TAB 2 ─────────────────────────────────
    with tab2:
        av_c = raw["Data_availability"].value_counts()
        av_color_map = {
            "open":"#D9F2E6","internal_only":"#FFE0E0",
            "restricted":"#FFF4CC","unclear":"#E5E5E5","purchased":"#EDE7F6",
        }

        col_a, col_b = st.columns([1,1])
        with col_a:
            st.markdown('<div class="section-title">가용성 분포 (전체 313건)</div>', unsafe_allow_html=True)
            fig4 = go.Figure(go.Pie(
                labels=av_c.index, values=av_c.values,
                marker_colors=[av_color_map.get(k,"#ccc") for k in av_c.index],
                textinfo="label+percent+value",
                textfont_size=12, hole=0.45,
                pull=[0.05 if k=="internal_only" else 0 for k in av_c.index],
            ))
            fig4.update_layout(
                showlegend=True, height=320, margin=dict(t=10,b=10),
                paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Noto Sans KR"),
                legend=dict(orientation="v", x=1.02),
            )
            st.plotly_chart(fig4, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-title">내부 전용 소스 주요 유형</div>', unsafe_allow_html=True)
            int_df = raw[raw["Data_availability"]=="internal_only"]
            int_type = int_df["Data_type"].value_counts()
            fig5 = go.Figure(go.Bar(
                y=int_type.index, x=int_type.values, orientation="h",
                marker_color="#FFE0E0", marker_line_color="#C0392B", marker_line_width=1,
                text=int_type.values, textposition="outside",
            ))
            fig5.update_layout(
                xaxis_title="내부전용 레코드 수", yaxis=dict(autorange="reversed"),
                margin=dict(t=10,b=20,l=10,r=40), height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,248,248,0.5)",
                xaxis=dict(gridcolor="#eee"), font=dict(family="Noto Sans KR"),
            )
            st.plotly_chart(fig5, use_container_width=True)

        # Internal-only table
        st.markdown('<div class="section-title">🔒 내부 전용 주요 소스 목록</div>', unsafe_allow_html=True)
        int_mdf = mdf[mdf["availability"].str.contains("internal_only", na=False)].sort_values("freq", ascending=False)
        disp = int_mdf[["acronym","data_name","category","org","freq","temporal_res"]].head(30).copy()
        disp.columns = ["약어","데이터 명칭","분야","생산기관","빈도","시간해상도"]
        st.dataframe(disp.reset_index(drop=True), use_container_width=True, height=350)

    # ────────────────────────────────── TAB 3 ─────────────────────────────────
    with tab3:
        acr_df = raw[raw["Acronym"] != "Not in source"]["Acronym"].value_counts().reset_index()
        acr_df.columns = ["약어","건수"]

        col_c, col_d = st.columns([1.4, 0.6])
        with col_c:
            st.markdown('<div class="section-title">주요 약어별 레코드 수</div>', unsafe_allow_html=True)
            top_acr = acr_df.head(20)
            fig6 = go.Figure(go.Bar(
                x=top_acr["약어"], y=top_acr["건수"],
                marker=dict(
                    color=top_acr["건수"],
                    colorscale=[[0,"#D6E4F0"],[1,"#1F4E79"]],
                    showscale=False,
                ),
                marker_line_color="#1F4E79", marker_line_width=0.8,
                text=top_acr["건수"], textposition="outside",
            ))
            fig6.update_layout(
                xaxis_title="약어", yaxis_title="레코드 수",
                margin=dict(t=10,b=60,l=10,r=10), height=320,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,250,255,0.5)",
                yaxis=dict(gridcolor="#eee"), font=dict(family="Noto Sans KR"),
                xaxis=dict(tickangle=-35),
            )
            st.plotly_chart(fig6, use_container_width=True)

        with col_d:
            st.markdown('<div class="section-title">약어 전체 목록</div>', unsafe_allow_html=True)
            st.dataframe(acr_df.reset_index(drop=True), use_container_width=True, height=340)

        # Treemap of categories
        st.markdown('<div class="section-title">주제 분야 트리맵</div>', unsafe_allow_html=True)
        cat_all = raw["Data_category"].value_counts().reset_index()
        cat_all.columns = ["분야","건수"]
        fig7 = px.treemap(
            cat_all, path=["분야"], values="건수",
            color="건수",
            color_continuous_scale=[[0,"#D6E4F0"],[0.5,"#4472C4"],[1,"#1F4E79"]],
        )
        fig7.update_layout(
            margin=dict(t=10,b=10,l=10,r=10), height=320,
            paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Noto Sans KR"),
            coloraxis_showscale=False,
        )
        fig7.update_traces(textfont_size=12)
        st.plotly_chart(fig7, use_container_width=True)

    # ────────────────────────────────── TAB 4 ─────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">분석 대상 보고서 67건 목록</div>', unsafe_allow_html=True)
        kw_r = st.text_input("보고서 검색", placeholder="파일명 키워드")
        show_refs = refs.copy()
        if kw_r:
            show_refs = show_refs[show_refs["참조"].str.contains(kw_r, na=False, case=False)]

        for _, r in show_refs.iterrows():
            idx = int(r["색인"])
            title = str(r["참조"])
            # Count records from this report
            cnt = raw[raw["Source"].astype(str).str.contains(str(idx), na=False)].shape[0]
            st.markdown(
                f'<div style="background:{"#EBF3FB" if idx%2==0 else "white"};'
                f'border-radius:8px;padding:10px 16px;margin:3px 0;'
                f'border-left:4px solid #4472C4;">'
                f'<span style="font-weight:700;color:#1F4E79;margin-right:10px">#{idx}</span>'
                f'<span style="font-size:0.88rem;color:#374151">{title[:100]}</span>'
                f'<span style="float:right;background:#1F4E79;color:white;border-radius:5px;'
                f'padding:1px 8px;font-size:0.78rem">{cnt}건</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
