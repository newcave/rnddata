import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import math
from .utils import page_header

# ── Institute definitions (same as p5) ───────────────────────────────────────
INSTITUTES = {
    "경영":      {"name": "경영연구소",       "icon": "📋", "color": "#7B68EE"},
    "수자원환경":{"name": "수자원환경연구소",  "icon": "🌊", "color": "#2E75B6"},
    "상하수":    {"name": "상하수도연구소",    "icon": "🚰", "color": "#17A589"},
    "인프라안전":{"name": "물인프라안전연구소","icon": "🏗",  "color": "#E67E22"},
    "에너지":    {"name": "물에너지연구소",    "icon": "⚡", "color": "#D4AC0D"},
    "위성":      {"name": "수자원위성연구소",  "icon": "🛰",  "color": "#8E44AD"},
    "AI":        {"name": "AI연구소",          "icon": "🤖", "color": "#1F4E79"},
}

REPORT_INST = {
    1: [("에너지",True),("상하수",False)],
    2: [("수자원환경",True)],
    3: [("에너지",True),("상하수",False)],
    4: [("수자원환경",True)],
    5: [("에너지",True)],
    6: [("수자원환경",True)],
    7: [("위성",True)],
    8: [("경영",True)],
    9: [("상하수",True),("에너지",False)],
    10:[("수자원환경",True),("AI",False)],
    11:[("AI",True),("수자원환경",False)],
    12:[("수자원환경",True)],
    13:[("AI",True)],
    14:[("수자원환경",True)],
    15:[("AI",True),("상하수",False)],
    16:[("수자원환경",True)],
    17:[("상하수",True),("AI",False)],
    18:[("경영",True)],
    19:[("상하수",True),("AI",False)],
    20:[("경영",True)],
    21:[("AI",True),("상하수",False)],
    22:[("수자원환경",True),("위성",False)],
    23:[("수자원환경",False)],
    24:[("상하수",True)],
    25:[("수자원환경",True)],
    26:[("수자원환경",True)],
    27:[("경영",True),("상하수",False)],
    28:[("수자원환경",True)],
    29:[("경영",True)],
    30:[("수자원환경",True)],
    31:[("인프라안전",True)],
    32:[("수자원환경",True)],
    33:[("수자원환경",True)],
    34:[("수자원환경",True)],
    35:[("수자원환경",True)],
    36:[("경영",True),("상하수",False)],
    37:[("AI",True),("수자원환경",False)],
    38:[("수자원환경",True)],
    39:[("상하수",True)],
    40:[("에너지",True)],
    41:[("상하수",True)],
    42:[("상하수",True)],
    43:[("위성",True),("수자원환경",False)],
    44:[("수자원환경",True)],
    45:[("수자원환경",True)],
    46:[("수자원환경",True)],
    47:[("수자원환경",True)],
    48:[("수자원환경",True)],
    49:[("수자원환경",True),("경영",False)],
    50:[("수자원환경",True)],
    51:[("상하수",True)],
    52:[("경영",True)],
    53:[("인프라안전",True)],
    54:[("상하수",True)],
    55:[("수자원환경",True)],
    56:[("경영",True)],
    57:[("수자원환경",True)],
    58:[("수자원환경",True)],
    59:[("수자원환경",True)],
    60:[("수자원환경",True)],
    61:[("수자원환경",True)],
    62:[("인프라안전",True),("상하수",False)],
    63:[("수자원환경",True)],
    64:[("에너지",True)],
    65:[("인프라안전",True)],
    66:[("에너지",True)],
    67:[("인프라안전",True)],
}

def build_collab_matrix():
    keys = list(INSTITUTES.keys())
    n = len(keys)
    idx = {k: i for i, k in enumerate(keys)}
    mat = np.zeros((n, n), dtype=int)
    solo = {k: 0 for k in keys}

    for _, pairs in REPORT_INST.items():
        insts = [i for i, _ in pairs]
        if len(insts) == 1:
            solo[insts[0]] += 1
        for i in range(len(insts)):
            for j in range(i + 1, len(insts)):
                a, b = insts[i], insts[j]
                mat[idx[a]][idx[b]] += 1
                mat[idx[b]][idx[a]] += 1
    return keys, mat, solo

def circle_positions(n, r=1.0):
    """Return (x, y) positions arranged in a circle."""
    angles = [2 * math.pi * i / n - math.pi / 2 for i in range(n)]
    return [(r * math.cos(a), r * math.sin(a)) for a in angles]

def render():
    page_header("🤝", "데이터 기반 협업도 (例示)",
                "보고서 67건 기반 · 7개 연구소 간 공동 연구 데이터 협력 관계 시각화")

    keys, mat, solo = build_collab_matrix()
    n = len(keys)
    pos = circle_positions(n, r=1.0)

    # ── KPI 요약 ──────────────────────────────────────────────────────────────
    total_collab = int(mat.sum() // 2)
    total_solo   = sum(solo.values())
    most_collab  = max(keys, key=lambda k: mat[keys.index(k)].sum())
    most_partner = max(keys, key=lambda k: np.count_nonzero(mat[keys.index(k)]))

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, color in [
        (c1, total_collab,                          "총 협업 연결 수",    "#2E75B6"),
        (c2, total_solo,                            "단독 수행 보고서",   "#8E44AD"),
        (c3, INSTITUTES[most_collab]["name"],       "최다 협업 연구소",   "#17A589"),
        (c4, INSTITUTES[most_partner]["name"],      "최다 파트너 연구소", "#E67E22"),
    ]:
        col.markdown(
            f'<div style="background:white;border-left:5px solid {color};'
            f'border-radius:10px;padding:14px 16px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,0.07);">'
            f'<div style="font-size:1.5rem;font-weight:800;color:{color}">{val}</div>'
            f'<div style="font-size:0.8rem;color:#6b7280;margin-top:2px">{lbl}</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin:18px 0 6px 0'></div>", unsafe_allow_html=True)

    # ── Network diagram ───────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🕸 연구소 협업 네트워크</div>',
                unsafe_allow_html=True)

    fig = go.Figure()
    max_w = max(mat.max(), 1)

    # Draw edges
    for i in range(n):
        for j in range(i + 1, n):
            w = mat[i][j]
            if w == 0:
                continue
            xi, yi = pos[i]
            xj, yj = pos[j]
            # Curved line via midpoint offset
            mx = (xi + xj) / 2 * 0.82
            my = (yi + yj) / 2 * 0.82
            # Bezier-like with 3 points
            lw = 1.5 + (w / max_w) * 7
            opacity = 0.25 + (w / max_w) * 0.55
            fig.add_trace(go.Scatter(
                x=[xi, mx, xj], y=[yi, my, yj],
                mode="lines",
                line=dict(width=lw,
                          color=INSTITUTES[keys[i]]["color"]),
                opacity=opacity,
                hoverinfo="skip",
                showlegend=False,
            ))
            # Edge weight label at midpoint
            fig.add_trace(go.Scatter(
                x=[(xi + xj) / 2], y=[(yi + yj) / 2],
                mode="text",
                text=[f"<b>{w}</b>"],
                textfont=dict(size=11, color="#374151"),
                hoverinfo="skip",
                showlegend=False,
            ))

    # Draw nodes
    node_x   = [p[0] for p in pos]
    node_y   = [p[1] for p in pos]
    node_col = [INSTITUTES[k]["color"] for k in keys]
    node_sz  = [28 + int(mat[i].sum()) * 4 for i in range(n)]
    hover_txt = []
    for i, k in enumerate(keys):
        partners = [(keys[j], mat[i][j]) for j in range(n) if mat[i][j] > 0]
        partners.sort(key=lambda x: -x[1])
        ptxt = "<br>".join(
            f"  {INSTITUTES[p]['icon']} {INSTITUTES[p]['name']}: {w}건"
            for p, w in partners)
        hover_txt.append(
            f"<b>{INSTITUTES[k]['icon']} {INSTITUTES[k]['name']}</b><br>"
            f"총 협업: {int(mat[i].sum())}건 | 단독: {solo[k]}건<br>"
            f"협력 연구소:<br>{ptxt}"
        )

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        marker=dict(
            size=node_sz,
            color=node_col,
            line=dict(width=3, color="white"),
            opacity=0.93,
        ),
        text=[f"{INSTITUTES[k]['icon']}" for k in keys],
        textposition="middle center",
        textfont=dict(size=16),
        hovertext=hover_txt,
        hoverinfo="text",
        hoverlabel=dict(
            bgcolor="white", font_size=12,
            font_family="Noto Sans KR",
            bordercolor="#4472C4",
        ),
        showlegend=False,
    ))

    # Node labels outside circle
    label_r = 1.28
    label_pos = circle_positions(n, r=label_r)
    for i, k in enumerate(keys):
        lx, ly = label_pos[i]
        halign = "left" if lx > 0.1 else ("right" if lx < -0.1 else "center")
        fig.add_annotation(
            x=lx, y=ly,
            text=f"<b>{INSTITUTES[k]['name']}</b>",
            showarrow=False,
            font=dict(size=11, color=INSTITUTES[k]["color"],
                      family="Noto Sans KR"),
            xanchor=halign,
            yanchor="middle",
        )

    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.7, 1.7]),
        yaxis=dict(visible=False, range=[-1.7, 1.7], scaleanchor="x"),
        height=520,
        paper_bgcolor="rgba(248,250,255,0.0)",
        plot_bgcolor="rgba(248,250,255,0.6)",
        margin=dict(t=10, b=10, l=10, r=10),
        font=dict(family="Noto Sans KR"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("※ 노드 크기 = 총 협업 건수 비례 · 선 굵기 = 공동 보고서 수 · 숫자 = 협업 보고서 건수")

    st.markdown("---")

    # ── Per-institute collaboration breakdown ─────────────────────────────────
    st.markdown('<div class="section-title">📊 연구소별 타소 협력 비중</div>',
                unsafe_allow_html=True)

    col_l, col_r = st.columns([1.1, 0.9])

    with col_l:
        # Stacked bar: solo vs each partner
        bar_data = {}
        for i, k in enumerate(keys):
            row = {keys[j]: int(mat[i][j]) for j in range(n) if i != j and mat[i][j] > 0}
            row["단독"] = solo[k]
            bar_data[INSTITUTES[k]["name"]] = row

        partner_keys_all = sorted(
            set(pk for row in bar_data.values() for pk in row if pk != "단독"))
        inst_names = [INSTITUTES[k]["name"] for k in keys]

        fig2 = go.Figure()
        # Solo bar
        fig2.add_trace(go.Bar(
            name="단독 수행",
            x=inst_names,
            y=[bar_data[n].get("단독", 0) for n in inst_names],
            marker_color="rgba(200,200,200,0.6)",
            marker_line_color="#aaa",
            marker_line_width=0.8,
        ))
        # Collaboration bars
        for pk in partner_keys_all:
            fig2.add_trace(go.Bar(
                name=INSTITUTES[pk]["name"],
                x=inst_names,
                y=[bar_data[n].get(pk, 0) for n in inst_names],
                marker_color=INSTITUTES[pk]["color"],
                marker_line_color="white",
                marker_line_width=0.8,
                opacity=0.85,
            ))

        fig2.update_layout(
            barmode="stack",
            xaxis_tickangle=-30,
            yaxis_title="보고서 수",
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,250,255,0.5)",
            font=dict(family="Noto Sans KR", size=10),
            margin=dict(t=10, b=60, l=10, r=10),
            legend=dict(orientation="h", y=1.08, font_size=10),
            xaxis=dict(gridcolor="#eee"),
            yaxis=dict(gridcolor="#eee"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_r:
        # Collaboration ratio card per institute
        st.markdown(
            '<div style="font-size:0.88rem;font-weight:600;color:#1F4E79;'
            'margin-bottom:8px;">협력 비중 (타 연구소 협업 / 전체)</div>',
            unsafe_allow_html=True)

        for i, k in enumerate(keys):
            inst   = INSTITUTES[k]
            total  = int(mat[i].sum()) + solo[k]
            collab = int(mat[i].sum())
            pct    = int(collab / total * 100) if total else 0
            partners = sorted(
                [(keys[j], mat[i][j]) for j in range(n) if mat[i][j] > 0],
                key=lambda x: -x[1])
            partner_txt = " · ".join(
                f"{INSTITUTES[p]['icon']}{mat[i][keys.index(p)]}건"
                for p, _ in partners[:3])

            st.markdown(
                f'<div style="background:white;border-radius:8px;'
                f'padding:9px 14px;margin:4px 0;'
                f'box-shadow:0 1px 5px rgba(0,0,0,0.06);'
                f'border-left:4px solid {inst["color"]};">'
                f'<div style="display:flex;justify-content:space-between;'
                f'align-items:center;margin-bottom:4px;">'
                f'<span style="font-weight:700;font-size:0.88rem;color:{inst["color"]}">'
                f'{inst["icon"]} {inst["name"]}</span>'
                f'<span style="font-size:0.82rem;font-weight:700;color:{inst["color"]}">'
                f'{pct}%</span></div>'
                f'<div style="background:#eee;border-radius:4px;height:7px;margin-bottom:4px;">'
                f'<div style="width:{pct}%;background:{inst["color"]};'
                f'border-radius:4px;height:7px;"></div></div>'
                f'<div style="font-size:0.72rem;color:#9ca3af">'
                f'협업 {collab}건 / 전체 {total}건  |  {partner_txt}</div>'
                f'</div>',
                unsafe_allow_html=True)

    # ── Heatmap ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🗺 협업 매트릭스 히트맵</div>',
                unsafe_allow_html=True)

    inst_labels = [f"{INSTITUTES[k]['icon']} {INSTITUTES[k]['name']}" for k in keys]
    fig3 = go.Figure(go.Heatmap(
        z=mat,
        x=inst_labels,
        y=inst_labels,
        colorscale=[[0, "#F0F7FD"], [0.4, "#4472C4"], [1, "#1F4E79"]],
        text=mat,
        texttemplate="%{text}",
        textfont=dict(size=13, family="Noto Sans KR"),
        hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>협업 보고서: <b>%{z}건</b><extra></extra>",
        showscale=False,
        xgap=3, ygap=3,
    ))
    fig3.update_layout(
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        font=dict(family="Noto Sans KR", size=11),
        xaxis=dict(tickangle=-30),
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("※ 대각선 제외 · 수치 = 공동 수행 보고서 건수 (데이터 기반 例示, 추후 정밀 매핑 필요)")
