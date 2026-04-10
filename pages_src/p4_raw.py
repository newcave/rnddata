import streamlit as st
import pandas as pd
from .utils import load_raw, load_refs, page_header

_AVAIL_COLORS = {
    "open":          "background-color:#D9F2E6",
    "internal_only": "background-color:#FFE0E0",
    "restricted":    "background-color:#FFF4CC",
    "unclear":       "background-color:#F0F0F0",
}

def render():
    page_header("🔬", "원본 상세 데이터",
                "PDF 파싱 기반 313개 데이터 레코드 전체 — 21개 필드 완전 수록")

    raw = load_raw()
    refs = load_refs()

    # ── Filters ───────────────────────────────────────────────────────────────
    with st.expander("🔍 필터 & 검색", expanded=True):
        r1c1, r1c2, r1c3 = st.columns(3)
        sel_dtype = r1c1.multiselect(
            "데이터 유형",
            sorted(raw["Data_type"].dropna().unique()),
            default=sorted(raw["Data_type"].dropna().unique()),
        )
        sel_avail = r1c2.multiselect(
            "가용성",
            sorted(raw["Data_availability"].dropna().unique()),
            default=sorted(raw["Data_availability"].dropna().unique()),
        )
        sel_cat = r1c3.multiselect(
            "주제 분야 (Top 10)",
            raw["Data_category"].value_counts().head(10).index.tolist(),
            default=raw["Data_category"].value_counts().head(10).index.tolist(),
        )
        kw = st.text_input("키워드 검색", placeholder="예: 수질, WAMIS, rainfall, K-water")

    filtered = raw[
        raw["Data_type"].isin(sel_dtype) &
        raw["Data_availability"].isin(sel_avail)
    ]
    # category filter — include rows that match OR categories not in top10
    top10_cats = raw["Data_category"].value_counts().head(10).index.tolist()
    not_top10 = ~raw["Data_category"].isin(top10_cats)
    filtered = filtered[
        filtered["Data_category"].isin(sel_cat) |
        (filtered.index.isin(raw[not_top10].index))
    ]
    if kw:
        kw_l = kw.lower()
        mask = (
            filtered["Data_name"].str.lower().str.contains(kw_l, na=False) |
            filtered["Data_name_kr"].str.lower().str.contains(kw_l, na=False) |
            filtered["Acronym"].str.lower().str.contains(kw_l, na=False) |
            filtered["Source_organization"].str.lower().str.contains(kw_l, na=False) |
            filtered["Parameters_measured"].str.lower().str.contains(kw_l, na=False) |
            filtered["Usage_in_study"].str.lower().str.contains(kw_l, na=False)
        )
        filtered = filtered[mask]

    c1, c2, c3 = st.columns(3)
    c1.metric("검색 결과", f"{len(filtered)}건")
    c2.metric("공개 데이터", len(filtered[filtered["Data_availability"]=="open"]))
    c3.metric("내부 전용", len(filtered[filtered["Data_availability"]=="internal_only"]))
    st.markdown("---")

    # ── Column groups ──────────────────────────────────────────────────────────
    COL_GROUPS = {
        "핵심 정보": ["Data_name","Data_name_kr","Acronym","Data_type","Data_category","Source_organization","Data_availability","Source"],
        "공간·시간": ["Data_name","Acronym","Spatial_coverage","Spatial_resolution","Temporal_coverage","Temporal_resolution"],
        "수집·계측": ["Data_name","Acronym","Collection_method","Instruments_or_tools","Data_format","Data_volume_or_scale"],
        "파라미터·활용": ["Data_name","Acronym","Parameters_measured","Usage_in_study","Notes"],
        "전체 21개 컬럼": list(raw.columns),
    }
    selected_group = st.radio("컬럼 그룹 선택", list(COL_GROUPS.keys()), horizontal=True)
    show_cols = [c for c in COL_GROUPS[selected_group] if c in filtered.columns]

    disp = filtered[show_cols].copy().reset_index(drop=True)

    # Rename columns to Korean
    KR_COLS = {
        "Data_name":"데이터 명칭","Data_name_kr":"한국어 명칭","Acronym":"약어",
        "Data_type":"유형","Data_category":"분야","Source_organization":"생산기관",
        "Access_method":"접근방법","Portal_or_system_url":"포털/URL",
        "Spatial_coverage":"공간범위","Spatial_resolution":"공간해상도",
        "Temporal_coverage":"시간범위","Temporal_resolution":"시간해상도",
        "Data_volume_or_scale":"데이터 규모","Collection_method":"수집방법",
        "Instruments_or_tools":"장비/도구","Data_format":"형식",
        "Parameters_measured":"측정파라미터","Usage_in_study":"활용목적",
        "Data_availability":"가용성","Notes":"비고","Source":"출처번호",
    }
    disp.columns = [KR_COLS.get(c, c) for c in show_cols]

    # Style availability column if present
    def style_df(df):
        styled = df.copy()
        styles = pd.DataFrame("", index=df.index, columns=df.columns)
        if "가용성" in df.columns:
            ci = df.columns.get_loc("가용성")
            for ri in range(len(df)):
                av = str(df.iloc[ri, ci]).split("/")[0].strip()
                styles.iloc[ri, ci] = _AVAIL_COLORS.get(av, "")
        return styles

    st.dataframe(
        disp.style.apply(style_df, axis=None),
        use_container_width=True,
        height=480,
    )

    # ── Record detail ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">📄 레코드 상세 조회</div>', unsafe_allow_html=True)
    sel_name = st.selectbox("레코드 선택", filtered["Data_name"].tolist(),
                            format_func=lambda x: str(x)[:90])
    if sel_name:
        row = filtered[filtered["Data_name"]==sel_name].iloc[0]
        # Source report lookup
        src_idx = str(row["Source"]).strip()
        ref_row = refs[refs["색인"].astype(str)==src_idx]
        report_title = ref_row["참조"].values[0] if len(ref_row) else f"Report #{src_idx}"

        av = str(row["Data_availability"])
        av_color = {"open":"#D9F2E6","internal_only":"#FFE0E0","restricted":"#FFF4CC"}.get(av,"#eee")

        st.markdown(
            f'<div style="background:{av_color};border-radius:10px;padding:14px 20px;margin:8px 0">'
            f'<b style="font-size:1.05rem;color:#1F4E79">{row["Data_name"]}</b>'
            f'<span style="margin-left:12px;font-size:0.85rem;color:#6b7280">{row.get("Data_name_kr","")}</span>'
            f'</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        fields_l = [("약어",row["Acronym"]),("데이터 유형",row["Data_type"]),
                    ("주제 분야",row["Data_category"]),("생산기관",row["Source_organization"]),
                    ("접근 방법",row["Access_method"])]
        fields_m = [("공간 범위",row["Spatial_coverage"]),("공간 해상도",row["Spatial_resolution"]),
                    ("시간 범위",row["Temporal_coverage"]),("시간 해상도",row["Temporal_resolution"]),
                    ("데이터 규모",row["Data_volume_or_scale"])]
        fields_r = [("수집 방법",row["Collection_method"]),("장비/도구",row["Instruments_or_tools"]),
                    ("데이터 형식",row["Data_format"]),("가용성",row["Data_availability"]),
                    ("출처 보고서 번호",row["Source"])]
        for k, v in fields_l:
            c1.markdown(f"**{k}:** {v}")
        for k, v in fields_m:
            c2.markdown(f"**{k}:** {v}")
        for k, v in fields_r:
            c3.markdown(f"**{k}:** {v}")

        st.markdown(f"**측정 파라미터:** {row['Parameters_measured']}")
        st.markdown(f"**연구 활용 목적:** {row['Usage_in_study']}")
        if str(row.get("Notes","")) not in ("nan",""):
            st.info(f"📝 노트: {row['Notes']}")
        st.markdown(f"**출처 보고서:** `{report_title}`")

    # ── Download ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.download_button(
        "⬇️  필터링 결과 전체 CSV 다운로드",
        filtered.to_csv(index=False, encoding="utf-8-sig"),
        "kwater_raw_filtered.csv", "text/csv",
    )
