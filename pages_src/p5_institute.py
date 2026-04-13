import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re
from .utils import load_raw, load_matrix, load_refs, page_header

# ── 1. Report → Institute mapping (manual, primary=bold) ─────────────────────
# Format: report_idx → [(institute_code, is_primary)]
REPORT_INST = {
    1:  [("에너지", True),  ("상하수", False)],
    2:  [("수자원환경", True)],
    3:  [("에너지", True),  ("상하수", False)],
    4:  [("수자원환경", True)],
    5:  [("에너지", True)],
    6:  [("수자원환경", True)],
    7:  [("위성", True)],
    8:  [("경영", True)],
    9:  [("상하수", True),  ("에너지", False)],
    10: [("수자원환경", True), ("AI", False)],
    11: [("AI", True),      ("수자원환경", False)],
    12: [("수자원환경", True)],
    13: [("AI", True)],
    14: [("수자원환경", True)],
    15: [("AI", True),      ("상하수", False)],
    16: [("수자원환경", True)],
    17: [("상하수", True),  ("AI", False)],
    18: [("경영", True)],
    19: [("상하수", True),  ("AI", False)],
    20: [("경영", True)],
    21: [("AI", True),      ("상하수", False)],
    22: [("수자원환경", True), ("위성", False)],
    23: [("수자원환경", False)],   # metadata CSV (복수)
    24: [("상하수", True)],
    25: [("수자원환경", True)],
    26: [("수자원환경", True)],
    27: [("경영", True),    ("상하수", False)],
    28: [("수자원환경", True)],
    29: [("경영", True)],
    30: [("수자원환경", True)],
    31: [("인프라안전", True)],
    32: [("수자원환경", True)],
    33: [("수자원환경", True)],
    34: [("수자원환경", True)],
    35: [("수자원환경", True)],
    36: [("경영", True),    ("상하수", False)],
    37: [("AI", True),      ("수자원환경", False)],
    38: [("수자원환경", True)],
    39: [("상하수", True)],
    40: [("에너지", True)],
    41: [("상하수", True)],
    42: [("상하수", True)],
    43: [("위성", True),    ("수자원환경", False)],
    44: [("수자원환경", True)],
    45: [("수자원환경", True)],
    46: [("수자원환경", True)],
    47: [("수자원환경", True)],
    48: [("수자원환경", True)],
    49: [("수자원환경", True), ("경영", False)],
    50: [("수자원환경", True)],
    51: [("상하수", True)],
    52: [("경영", True)],
    53: [("인프라안전", True)],
    54: [("상하수", True)],
    55: [("수자원환경", True)],
    56: [("경영", True)],
    57: [("수자원환경", True)],
    58: [("수자원환경", True)],
    59: [("수자원환경", True)],
    60: [("수자원환경", True)],
    61: [("수자원환경", True)],
    62: [("인프라안전", True), ("상하수", False)],
    63: [("수자원환경", True)],
    64: [("에너지", True)],
    65: [("인프라안전", True)],
    66: [("에너지", True)],
    67: [("인프라안전", True)],
}

# ── 2. Category → Institute mapping (for matrix data) ────────────────────────
CAT_INST = {
    # 경영
    "economics":        ["경영"],
    "finance":          ["경영"],
    "administrative":   ["경영"],
    "social_value":     ["경영"],
    "social_perception":["경영"],
    "management_strategy":["경영"],
    "organizational_structure":["경영"],
    "consumer perception/WTP":["경영"],
    "demographic":      ["경영"],
    "Policy and Standards":["경영"],
    "legal standard":   ["경영"],
    "상수도 보급현황, 시설물 현황, 요금, 재정":["경영","상하수"],
    "water usage fees": ["경영"],
    "분석 가이드라인":  ["경영"],

    # 수자원환경
    "hydrological":     ["수자원환경"],
    "hydrological usage":["수자원환경"],
    "hydrological, water quality":["수자원환경"],
    "hydrological, water_quality":["수자원환경"],
    "streamflow":       ["수자원환경"],
    "streamflow, rainfall, GIS":["수자원환경","위성"],
    "streamflow, rainfall, water level":["수자원환경"],
    "streamflow, water quality":["수자원환경","상하수"],
    "streamflow_and_quality":["수자원환경","상하수"],
    "rainfall":         ["수자원환경"],
    "rainfall, temperature":["수자원환경"],
    "rainfall, temperature, etc.":["수자원환경"],
    "meteorological":   ["수자원환경"],
    "meteorological, hydrological":["수자원환경"],
    "water level":      ["수자원환경"],
    "water level, flow rate":["수자원환경"],
    "water level, water temperature":["수자원환경","에너지"],
    "water_level":      ["수자원환경"],
    "ecology":          ["수자원환경"],
    "biological":       ["수자원환경"],
    "생태":             ["수자원환경"],
    "vegetation":       ["수자원환경"],
    "agricultural water, reservoir":["수자원환경","경영"],
    "irrigation demand":["수자원환경","경영"],
    "sediment":         ["수자원환경"],
    "groundwater":      ["수자원환경"],
    "groundwater level":["수자원환경"],
    "groundwater facility management":["수자원환경","인프라안전"],
    "pollutant_load":   ["수자원환경","상하수"],
    "pollution source": ["수자원환경","상하수"],
    "오염원 부하량":    ["수자원환경","상하수"],
    "natural_disasters":["수자원환경"],
    "수자원":           ["수자원환경"],
    "농업 수문":        ["수자원환경"],
    "산림 및 토지이용": ["수자원환경","위성"],
    "어류폐사 사고 이력 및 위기관리":["수자원환경"],
    "어류폐사 사례 및 매뉴얼":["수자원환경"],
    "기상 및 기후":     ["수자원환경"],
    "water demand, supply forecast":["수자원환경","상하수"],
    "water intake":     ["수자원환경","상하수"],
    "multidisciplinary":["수자원환경"],

    # 상하수
    "water quality":    ["상하수","수자원환경"],
    "water_quality":    ["상하수","수자원환경"],
    "water quality/hydrological":["상하수","수자원환경"],
    "water supply infrastructure":["상하수"],
    "water supply network":["상하수"],
    "water_treatment_facility":["상하수"],
    "seawater desalination":["상하수"],
    "water_use":        ["상하수","경영"],
    "toxicology":       ["상하수"],
    "시설운영관리정보, 상수원관리정보":["상하수"],
    "air_quality":      ["상하수","수자원환경"],

    # 인프라안전
    "displacement":     ["인프라안전"],
    "Vibration data":   ["인프라안전","에너지"],
    "Vibration and pressure pulsation":["인프라안전","에너지"],
    "safety accident":  ["인프라안전"],
    "safety education": ["인프라안전"],
    "engineering standard":["인프라안전"],
    "Standard criteria":["인프라안전"],
    "Hydraulic performance":["인프라안전","에너지"],

    # 에너지
    "energy_efficiency":["에너지"],
    "energy_drivers":   ["에너지"],
    "energy_consumption":["에너지"],
    "operational_efficiency":["에너지"],
    "operation performance":["에너지"],
    "Electricity logs": ["에너지"],
    "greenhouse_gas_emissions":["에너지","수자원환경"],
    "온실가스 배출량":  ["에너지"],
    "온실가스 통계":    ["에너지"],
    "Livestock waste":  ["에너지","수자원환경"],
    "Biomass properties":["에너지"],
    "Floating debris volume":["수자원환경","에너지"],
    "Equipment metadata":["에너지","인프라안전"],

    # 위성
    "satellite imagery":["위성"],
    "soil moisture":    ["위성","수자원환경"],
    "GIS":              ["위성","수자원환경"],
    "GIS 및 지형정보":  ["위성","수자원환경"],
    "GIS, land cover, water quality":["위성","수자원환경","상하수"],
    "GIS, land use":    ["위성","수자원환경"],
    "geospatial":       ["위성","수자원환경"],

    # AI
    "other":            ["AI"],
}

INSTITUTES = {
    "경영":     {"name":"경영연구소",         "icon":"📋", "color":"#7B68EE", "light":"#EDE8FF"},
    "수자원환경":{"name":"수자원환경연구소",    "icon":"🌊", "color":"#2E75B6", "light":"#D6E4F0"},
    "상하수":   {"name":"상하수도연구소",       "icon":"🚰", "color":"#17A589", "light":"#D1F2EB"},
    "인프라안전":{"name":"물인프라안전연구소",  "icon":"🏗",  "color":"#E67E22", "light":"#FDEBD0"},
    "에너지":   {"name":"물에너지연구소",       "icon":"⚡", "color":"#F4D03F", "light":"#FEF9E7"},
    "위성":     {"name":"수자원위성연구소",     "icon":"🛰",  "color":"#8E44AD", "light":"#F5EEF8"},
    "AI":       {"name":"AI연구소",             "icon":"🤖", "color":"#1F4E79", "light":"#EBF3FB"},
}

def get_insts_for_source(row_category):
    return CAT_INST.get(str(row_category).strip(), ["기타"])

def parse_source_idxs(val):
    return [int(s.strip()) for s in re.split(r'[,;/]+', str(val)) if s.strip().isdigit()]

def render():
    page_header("🏛", "연구소별 데이터 현황 (案)",
                "7개 연구소별 데이터 소스 매핑 · 복수 연구소 중복 표기 · 주관연구소 볼드 표시")

    raw = load_raw()
    refs = load_refs()

    # ── Build report-level institute map ──────────────────────────────────────
    src_map = {str(int(r["색인"])): str(r["참조"]) for _, r in refs.iterrows()}

    # ── Build per-record institute tags ───────────────────────────────────────
    def get_record_insts(row):
        """Return list of (inst_code, is_primary) for a record."""
        cat_insts = [(i, False) for i in get_insts_for_source(row["Data_category"])]
        # Override with report-level primary if available
        src_idxs = parse_source_idxs(row["Source"])
        result = []
        primary_set = set()
        for idx in src_idxs:
            if idx in REPORT_INST:
                for inst, is_prim in REPORT_INST[idx]:
                    if inst not in primary_set:
                        result.append((inst, is_prim))
                        if is_prim:
                            primary_set.add(inst)
        if not result:
            result = cat_insts
        # Deduplicate keeping primary status
        seen = {}
        for inst, prim in result:
            if inst not in seen:
                seen[inst] = prim
            else:
                seen[inst] = seen[inst] or prim
        return [(k, v) for k, v in seen.items()]

    raw["_insts"] = raw.apply(get_record_insts, axis=1)

    # ── Tab per institute ─────────────────────────────────────────────────────
    inst_keys = list(INSTITUTES.keys())
    tab_labels = [f'{INSTITUTES[k]["icon"]} {INSTITUTES[k]["name"]}' for k in inst_keys]
    tabs = st.tabs(tab_labels)

    for tab, inst_key in zip(tabs, inst_keys):
        inst_info = INSTITUTES[inst_key]
        with tab:
            # Filter records belonging to this institute
            mask = raw["_insts"].apply(lambda lst: any(i == inst_key for i, _ in lst))
            inst_df = raw[mask].copy()
            inst_df["_is_primary"] = inst_df["_insts"].apply(
                lambda lst: any(i == inst_key and p for i, p in lst))

            # Count related reports
            related_reports = set()
            for idx, pairs in REPORT_INST.items():
                if any(i == inst_key for i, _ in pairs):
                    related_reports.add(idx)
            primary_reports = set(
                idx for idx, pairs in REPORT_INST.items()
                if any(i == inst_key and p for i, p in pairs))

            # ── KPI row ───────────────────────────────────────────────────────
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(
                f'<div style="background:{inst_info["light"]};border-left:5px solid '
                f'{inst_info["color"]};border-radius:10px;padding:14px 18px;">'
                f'<div style="font-size:1.8rem;font-weight:800;color:{inst_info["color"]}">'
                f'{len(inst_df)}</div>'
                f'<div style="font-size:0.82rem;color:#6b7280">데이터 레코드 수</div></div>',
                unsafe_allow_html=True)
            c2.markdown(
                f'<div style="background:{inst_info["light"]};border-left:5px solid '
                f'{inst_info["color"]};border-radius:10px;padding:14px 18px;">'
                f'<div style="font-size:1.8rem;font-weight:800;color:{inst_info["color"]}">'
                f'{len(related_reports)}</div>'
                f'<div style="font-size:0.82rem;color:#6b7280">관련 보고서 수</div></div>',
                unsafe_allow_html=True)
            c3.markdown(
                f'<div style="background:{inst_info["light"]};border-left:5px solid '
                f'{inst_info["color"]};border-radius:10px;padding:14px 18px;">'
                f'<div style="font-size:1.8rem;font-weight:800;color:{inst_info["color"]}">'
                f'{len(primary_reports)}</div>'
                f'<div style="font-size:0.82rem;color:#6b7280">주관 보고서 (볼드)</div></div>',
                unsafe_allow_html=True)
            c4.markdown(
                f'<div style="background:{inst_info["light"]};border-left:5px solid '
                f'{inst_info["color"]};border-radius:10px;padding:14px 18px;">'
                f'<div style="font-size:1.8rem;font-weight:800;color:{inst_info["color"]}">'
                f'{len(inst_df[inst_df["Data_availability"]=="internal_only"])}</div>'
                f'<div style="font-size:0.82rem;color:#6b7280">내부 전용 소스</div></div>',
                unsafe_allow_html=True)

            st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

            col_l, col_r = st.columns([1.2, 0.8])

            # ── Left: data category bar chart ─────────────────────────────────
            with col_l:
                st.markdown(
                    f'<div class="section-title" style="color:{inst_info["color"]}">'
                    f'주제 분야별 데이터 소스 분포</div>',
                    unsafe_allow_html=True)
                cat_c = inst_df["Data_category"].value_counts().head(12)
                fig = go.Figure(go.Bar(
                    y=cat_c.index, x=cat_c.values, orientation="h",
                    marker_color=inst_info["color"],
                    marker_line_color=inst_info["color"], marker_line_width=0.8,
                    opacity=0.85,
                    text=cat_c.values, textposition="outside",
                ))
                fig.update_layout(
                    xaxis_title="레코드 수", yaxis=dict(autorange="reversed"),
                    margin=dict(t=4, b=20, l=10, r=40), height=min(320, 28*len(cat_c)+60),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=f"rgba(0,0,0,0)",
                    xaxis=dict(gridcolor="#eee"), font=dict(family="Noto Sans KR", size=11),
                )
                st.plotly_chart(fig, use_container_width=True)

            # ── Right: availability donut ──────────────────────────────────────
            with col_r:
                st.markdown(
                    f'<div class="section-title" style="color:{inst_info["color"]}">'
                    f'데이터 가용성 분포</div>',
                    unsafe_allow_html=True)
                av_c = inst_df["Data_availability"].value_counts()
                av_colors = {
                    "open":"#D9F2E6","internal_only":"#FFE0E0",
                    "restricted":"#FFF4CC","unclear":"#E5E5E5"}
                fig2 = go.Figure(go.Pie(
                    labels=av_c.index, values=av_c.values,
                    marker_colors=[av_colors.get(k,"#ccc") for k in av_c.index],
                    hole=0.50, textinfo="label+percent+value", textfont_size=11,
                ))
                fig2.update_layout(
                    showlegend=False, margin=dict(t=4,b=10,l=10,r=10),
                    height=220, paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Noto Sans KR"),
                )
                st.plotly_chart(fig2, use_container_width=True)

                # Type mini counts
                dtype_c = inst_df["Data_type"].value_counts().head(5)
                st.markdown(
                    f'<div class="section-title" style="color:{inst_info["color"]};margin-top:0">'
                    f'데이터 유형 Top 5</div>', unsafe_allow_html=True)
                for dtype, cnt in dtype_c.items():
                    pct = int(cnt / len(inst_df) * 100)
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0;">'
                        f'<span style="font-size:0.82rem;width:140px;color:#374151">{dtype}</span>'
                        f'<div style="flex:1;background:#eee;border-radius:4px;height:10px;">'
                        f'<div style="width:{pct}%;background:{inst_info["color"]};'
                        f'border-radius:4px;height:10px;"></div></div>'
                        f'<span style="font-size:0.8rem;font-weight:700;color:{inst_info["color"]};'
                        f'width:32px;text-align:right">{cnt}</span>'
                        f'</div>',
                        unsafe_allow_html=True)

            # ── Report list ───────────────────────────────────────────────────
            st.markdown(
                f'<div class="section-title" style="color:{inst_info["color"]}">'
                f'관련 보고서 목록 (🔵 주관 · ⚪ 협력)</div>',
                unsafe_allow_html=True)

            rpt_rows = []
            for idx in sorted(related_reports):
                pairs = REPORT_INST.get(idx, [])
                is_primary = any(i == inst_key and p for i, p in pairs)
                collab = [INSTITUTES[i]["name"] for i, _ in pairs if i != inst_key]
                title = src_map.get(str(idx), f"Report #{idx}")
                # Clean filename
                title_clean = title.split("_")[0].strip() if "_" in title else title[:70]
                rpt_rows.append((idx, is_primary, title_clean, collab))

            # Sort: primary first
            rpt_rows.sort(key=lambda x: (not x[1], x[0]))

            for idx, is_prim, title, collab in rpt_rows:
                dot    = "🔵" if is_prim else "⚪"
                weight = "font-weight:700" if is_prim else "font-weight:400"
                collab_html = "".join(
                    f'<span style="background:{INSTITUTES[c]["color"] if c in INSTITUTES else "#ccc"};'
                    f'color:white;border-radius:4px;padding:1px 7px;font-size:0.72rem;margin-left:4px">'
                    f'{INSTITUTES[c]["icon"] if c in INSTITUTES else ""} {c}</span>'
                    for c in collab
                ) if collab else ""
                bg = inst_info["light"] if is_prim else "white"
                st.markdown(
                    f'<div style="background:{bg};border-radius:7px;padding:8px 14px;'
                    f'margin:3px 0;border-left:3px solid '
                    f'{"" + inst_info["color"] if is_prim else "#ddd"};">'
                    f'<span style="font-size:0.78rem;color:#9ca3af;margin-right:6px">#{idx}</span>'
                    f'<span style="{weight};font-size:0.88rem;color:#1F4E79">{dot} {title}</span>'
                    f'{collab_html}'
                    f'</div>',
                    unsafe_allow_html=True)

            # ── Data records table ─────────────────────────────────────────────
            st.markdown("<div style='margin:10px 0'></div>", unsafe_allow_html=True)
            with st.expander(f"📋 데이터 레코드 전체 보기 ({len(inst_df)}건)"):
                disp = inst_df[["Data_name","Acronym","Data_type","Data_category",
                                "Source_organization","Data_availability",
                                "Temporal_coverage","Parameters_measured"]].copy()
                disp.columns = ["데이터명","약어","유형","분야","생산기관","가용성","시간범위","파라미터"]
                # Highlight primary records
                def highlight_primary(row_):
                    src_idxs = []  # can't easily get back — style uniformly
                    return [""] * len(row_)
                st.dataframe(disp.reset_index(drop=True), use_container_width=True, height=350)

    # ── Cross-institute overview ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📊 연구소 간 데이터 현황 비교</div>',
                unsafe_allow_html=True)

    summary_rows = []
    for inst_key, inst_info in INSTITUTES.items():
        mask = raw["_insts"].apply(lambda lst: any(i == inst_key for i, _ in lst))
        inst_sub = raw[mask]
        n_reports = sum(1 for idx, pairs in REPORT_INST.items()
                        if any(i == inst_key for i, _ in pairs))
        n_prim    = sum(1 for idx, pairs in REPORT_INST.items()
                        if any(i == inst_key and p for i, p in pairs))
        n_internal = len(inst_sub[inst_sub["Data_availability"] == "internal_only"])
        summary_rows.append({
            "inst": inst_key,
            "name": inst_info["name"],
            "icon": inst_info["icon"],
            "records": len(inst_sub),
            "reports": n_reports,
            "primary": n_prim,
            "internal": n_internal,
            "color": inst_info["color"],
        })

    summary_rows.sort(key=lambda x: -x["records"])

    # Radar chart
    cats_radar = [r["icon"] + " " + r["name"] for r in summary_rows]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[r["records"] for r in summary_rows] + [summary_rows[0]["records"]],
        theta=cats_radar + [cats_radar[0]],
        fill="toself",
        fillcolor="rgba(46,117,182,0.15)",
        line=dict(color="#2E75B6", width=2),
        name="데이터 레코드 수",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[r["reports"]*3 for r in summary_rows] + [summary_rows[0]["reports"]*3],
        theta=cats_radar + [cats_radar[0]],
        fill="toself",
        fillcolor="rgba(198,239,206,0.3)",
        line=dict(color="#1A7A3A", width=2, dash="dot"),
        name="관련 보고서 수 (×3)",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, gridcolor="#eee")),
        showlegend=True, height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Noto Sans KR"),
        margin=dict(t=20, b=20, l=40, r=40),
        legend=dict(orientation="h", y=-0.12),
    )

    col_rad, col_bar = st.columns([1, 1])
    with col_rad:
        st.plotly_chart(fig_radar, use_container_width=True)
    with col_bar:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="레코드 수",
            x=[r["icon"]+" "+r["name"] for r in summary_rows],
            y=[r["records"] for r in summary_rows],
            marker_color=[r["color"] for r in summary_rows],
            text=[r["records"] for r in summary_rows],
            textposition="outside",
        ))
        fig_bar.add_trace(go.Bar(
            name="주관 보고서 수",
            x=[r["icon"]+" "+r["name"] for r in summary_rows],
            y=[r["primary"] for r in summary_rows],
            marker_color=[r["color"] for r in summary_rows],
            marker_pattern_shape="/",
            opacity=0.5,
            text=[r["primary"] for r in summary_rows],
            textposition="outside",
        ))
        fig_bar.update_layout(
            barmode="group", xaxis_tickangle=-30,
            height=360, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#eee"),
            yaxis=dict(gridcolor="#eee"),
            font=dict(family="Noto Sans KR", size=10),
            margin=dict(t=10, b=80, l=10, r=10),
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Summary table
    st.markdown('<div class="section-title">연구소별 요약 테이블</div>', unsafe_allow_html=True)
    for r in summary_rows:
        pct_internal = int(r["internal"] / r["records"] * 100) if r["records"] else 0
        st.markdown(
            f'<div style="display:grid;grid-template-columns:220px 80px 80px 80px 1fr;'
            f'gap:8px;align-items:center;background:white;border-radius:8px;'
            f'padding:10px 16px;margin:3px 0;'
            f'box-shadow:0 1px 6px rgba(0,0,0,0.06);'
            f'border-left:5px solid {r["color"]};">'
            f'<div style="font-weight:700;font-size:0.95rem;color:{r["color"]}">'
            f'{r["icon"]} {r["name"]}</div>'
            f'<div style="text-align:center"><div style="font-size:1.1rem;font-weight:700;color:{r["color"]}">'
            f'{r["records"]}</div><div style="font-size:0.72rem;color:#9ca3af">레코드</div></div>'
            f'<div style="text-align:center"><div style="font-size:1.1rem;font-weight:700;color:{r["color"]}">'
            f'{r["reports"]}</div><div style="font-size:0.72rem;color:#9ca3af">보고서</div></div>'
            f'<div style="text-align:center"><div style="font-size:1.1rem;font-weight:700;color:{r["color"]}">'
            f'{r["primary"]}</div><div style="font-size:0.72rem;color:#9ca3af">주관</div></div>'
            f'<div>'
            f'<div style="display:flex;align-items:center;gap:6px;">'
            f'<div style="flex:1;background:#eee;border-radius:4px;height:8px;">'
            f'<div style="width:{pct_internal}%;background:#E74C3C;border-radius:4px;height:8px;"></div></div>'
            f'<span style="font-size:0.75rem;color:#E74C3C">{pct_internal}% 내부전용</span>'
            f'</div></div>'
            f'</div>',
            unsafe_allow_html=True)
