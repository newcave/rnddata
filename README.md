# 💧 K-water 연구보고서 데이터 소스 인벤토리 대시보드

> K-water 연구보고서 67건을 PDF 파싱·분석하여 도출한 **313개 데이터 레코드**, **271개 고유 데이터 소스**를 시각화하는 Streamlit 대시보드입니다.  
> AI 데이터 실증랩 / 데이터 통합 관리 사업 파이프라인 설계 기초 자료로 활용됩니다.

---

## 📋 페이지 구성

| 페이지 | 설명 |
|---|---|
| 🏠 개요 & 핵심 지표 | KPI 요약, 도넛차트, 우선순위 Top 소스 |
| 📊 크로스 리포트 매트릭스 | 271개 소스 × 21개 필드 전체 (필터·검색·상세조회) |
| 🎯 파이프라인 우선순위 | Immediate/Planned/Optional 3단계 우선순위 + 로드맵 |
| 🔬 원본 상세 데이터 | 313개 레코드 원본 (컬럼 그룹 선택, CSV 다운로드) |
| 📈 분야별 통계 | 유형·분야·가용성·약어 통계 + 트리맵·히트맵 |

---

## 🚀 실행 방법

### 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud 배포
1. 이 리포지토리를 GitHub에 Push
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. **New app** → 리포지토리 선택 → Main file: `app.py`
4. Deploy 클릭

---

## 📁 파일 구조

```
kwater_dashboard/
├── app.py                    # 메인 진입점 (사이드바 네비게이션)
├── requirements.txt          # Streamlit Cloud 의존성
├── data/
│   ├── matrix.csv            # 271개 집계 소스 (크로스 매트릭스)
│   ├── raw.csv               # 313개 원본 레코드
│   └── refs.csv              # 67개 보고서 참조 목록
└── pages_src/
    ├── __init__.py
    ├── utils.py              # 공통 데이터 로더 & 스타일 헬퍼
    ├── p1_overview.py        # 🏠 개요 & 핵심 지표
    ├── p2_matrix.py          # 📊 크로스 리포트 매트릭스
    ├── p3_priority.py        # 🎯 파이프라인 우선순위
    ├── p4_raw.py             # 🔬 원본 상세 데이터
    └── p5_stats.py           # 📈 분야별 통계
```

---

## 🎨 색상 팔레트

| 색상 | 용도 |
|---|---|
| `#1F4E79` Navy | 헤더, 주요 강조 |
| `#2E75B6` Blue | 페이지 헤더, 차트 |
| `#C6EFCE` Green | 즉시 구축 (Immediate) |
| `#FFEB9C` Yellow | 중기 계획 (Planned) |
| `#FCE4D6` Orange | 검토 단계 (Optional) |
| `#FFE0E0` Red-tint | 내부 전용 데이터 |
| `#D9F2E6` Green-tint | 공개 데이터 |

---

## 📊 데이터 출처

- **원천**: K-water 연구보고서 PDF (보고서 번호 67~120)
- **파싱**: Claude AI 기반 구조화 추출 (21개 필드)
- **집계**: 약어/데이터명 기반 중복 제거 후 크로스 리포트 매트릭스 생성
