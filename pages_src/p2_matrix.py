import streamlit as st
import pandas as pd
from .utils import load_matrix, page_header, prio_badge, avail_badge

_AVAIL_COLORS = {
    "open":          "background-color:#D9F2E6",
    "internal_only": "background-color:#FFE0E0",
    "restricted":    "background-color:#FFF4CC",
    "unclear":       "background-color:#F0F0F0",
}
_PRIO_COLORS = {
    "Immediate": "background-color:#C6EFCE; font-weight:700",
    "Planned":   "background-color:#FFEB9C; font-weight:600",
    "Optional":  "background-color:#FCE4D6",
}

def style_row(row):
    styles = [""] * len(row)
    pi = row.index.get_loc("priority")     if "priority"     in row.index else None
    ai = row.index.get_loc("availability") if "availability" in row.index else None
    fi = row.index.get_loc("freq")         if "freq"         in row.index else None
    if pi is not None:
        styles[pi] = _PRIO_COLORS.get(row["priority"], "")
    if ai is not None:
        av = str(row["availability"]).split("/")[0].strip()
        styles[ai] = _AVAIL_COLORS.get(av, "")
    if fi is not None:
        styles[fi] = "font-weight:700; color:#1F4E79"
    return styles

def render():
    page_header("📊", "크로스 리포트 매트릭스",
                "271개 고유 데이터 소스 × 보고서 67건 교차 분석")

    mdf = load_matrix()

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🔍 필터 & 검색", expanded=True):
        fc1, fc2, fc3, fc4 = st.columns(4)
        sel_prio = fc1.multiselect(
            "우선순위", ["Immediate","Planned","Optional"],
            default=["Immediate","Planned","Optional"])
        sel_avail = fc2.multiselect(
            "가용성", ["open","internal_only","restricted","unclear"],
            default=["open","internal_only","restricted","unclear"])
        sel_dtype = fc3.multiselect(
            "데이터 유형", sorted(mdf["dtype"].dropna().unique().tolist()),
            default=sorted(mdf["dtype"].dropna().unique().tolist()))
        keyword = fc4.text_input("키워드 검색 (명칭·약어·기관)", placeholder="예: WAMIS, 수질, KMA")

    filtered = mdf[
        mdf["priority"].isin(sel_prio) &
        mdf["availability"].str.split("/").apply(lambda x: any(v.strip() in sel_avail for v in x)) &
        mdf["dtype"].isin(sel_dtype)
    ]
    if keyword:
        kw = keyword.lower()
        filtered = filtered[
            filtered["data_name"].str.lower().str.contains(kw, na=False) |
            filtered["data_name_kr"].str.lower().str.contains(kw, na=False) |
            filtered["acronym"].str.lower().str.contains(kw, na=False) |
            filtered["org"].str.lower().str.contains(kw, na=False) |
            filtered["usage"].str.lower().str.contains(kw, na=False)
        ]

    c1, c2, c3 = st.columns(3)
    c1.metric("🔍 필터 결과", f"{len(filtered)}개")
    c2.metric("🔴 즉시", len(filtered[filtered["priority"]=="Immediate"]))
    c3.metric("🟡 중기", len(filtered[filtered["priority"]=="Planned"]))

    st.markdown("---")

    # ── Display columns selection ─────────────────────────────────────────────
    ALL_COLS = {
        "freq":         "빈도",
        "priority":     "우선순위",
        "availability": "가용성",
        "data_name":    "데이터 명칭",
        "data_name_kr": "한국어 명칭",
        "acronym":      "약어",
        "dtype":        "유형",
        "category":     "분야",
        "org":          "생산기관",
        "access":       "접근방법",
        "spatial":      "공간범위",
        "temporal":     "시간범위",
        "temporal_res": "시간해상도",
        "volume":       "규모",
        "instruments":  "장비/도구",
        "params":       "측정파라미터",
        "fmt":          "포맷",
        "usage":        "활용목적",
        "notes":        "비고",
        "report_list":  "보고서 목록",
    }
    default_show = ["freq","priority","availability","data_name","data_name_kr",
                    "acronym","dtype","category","org","access","spatial","temporal","usage"]

    with st.expander("🗂 표시 컬럼 선택"):
        show_cols = st.multiselect(
            "컬럼 선택", list(ALL_COLS.keys()),
            default=default_show,
            format_func=lambda c: ALL_COLS[c])

    show_cols = [c for c in show_cols if c in filtered.columns]

    disp = filtered[show_cols].copy().reset_index(drop=True)
    disp.columns = [ALL_COLS.get(c, c) for c in show_cols]

    # Apply styling
    styled = disp.style.apply(style_row, axis=1)
    st.dataframe(styled, use_container_width=True, height=520)

    # ── Detail expander ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🔎 소스 상세 조회</div>', unsafe_allow_html=True)
    options = filtered["data_name"].tolist()
    if options:
        sel = st.selectbox("데이터 소스 선택", options,
                           format_func=lambda x: x[:80])
        row = filtered[filtered["data_name"]==sel].iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**약어:** `{row['acronym']}`")
        c1.markdown(f"**한국어:** {row['data_name_kr']}")
        c1.markdown(f"**유형:** {row['dtype']}")
        c1.markdown(f"**분야:** {row['category']}")
        c1.markdown(f"**생산기관:** {row['org']}")
        c2.markdown(f"**공간 범위:** {row['spatial']}")
        c2.markdown(f"**시간 범위:** {row['temporal']}")
        c2.markdown(f"**시간 해상도:** {row['temporal_res']}")
        c2.markdown(f"**데이터 규모:** {row['volume']}")
        c2.markdown(f"**데이터 형식:** {row['fmt']}")
        c3.markdown(f"**가용성:** {row['availability']}")
        c3.markdown(f"**접근 방법:** {row['access']}")
        c3.markdown(f"**활용 보고서 수:** **{row['freq']}건**")
        st.markdown(f"**측정 장비/도구:** {row['instruments']}")
        st.markdown(f"**측정 파라미터:** {row['params']}")
        st.markdown(f"**연구 활용 목적:** {row['usage']}")
        if str(row['notes']) not in ('nan',''):
            st.info(f"📝 노트: {row['notes']}")
        st.markdown(f"**활용 보고서 목록:**")
        for r in str(row["report_list"]).split(" | "):
            st.markdown(f"  - {r}")
    else:
        st.info("필터 조건에 맞는 결과가 없습니다.")

    # ── Download ──────────────────────────────────────────────────────────────
    st.download_button(
        "⬇️  필터링 결과 CSV 다운로드",
        filtered.to_csv(index=False, encoding="utf-8-sig"),
        "kwater_matrix_filtered.csv",
        "text/csv",
    )
