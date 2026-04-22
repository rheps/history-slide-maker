---
name: history-slide-maker
description: "고등학교 한국사/동양사/서양사 교과서 내용을 웹 슬라이드 프레젠테이션으로 변환하는 스킬. 교과서 PDF 또는 텍스트를 받아서 단원 구조에 맞춰 HTML 슬라이드로 재구성한다. 다음 상황에서 반드시 사용: 사용자가 '역사 수업', '교과서 슬라이드', '한국사 PT', '동양사 발표', '서양사 수업자료', '단원 슬라이드', '교과서 내용으로 슬라이드' 등을 언급할 때. 교과서 텍스트를 쪼개고 분석해서 그래프, 표, 카드, 타임라인 등으로 시각적 재구성이 필요한 경우에도 트리거. '역사', '교과서', '단원'이 함께 나오면 이 스킬을 사용."
---

# History Slide Maker

고등학교 역사 교과서(한국사/동양사/서양사) 내용을 웹 슬라이드로 변환하는 스킬.
교과서 PDF나 텍스트를 받아서, 단원 구조를 따라가며 빠르게 넘기는 수업용 슬라이드를 만든다.

## 핵심 전제

- **고등학교** 수업용
- **단원별** 슬라이드 (한 차시가 아님)
- **빠르게 넘기는** 스타일 — 학생 필기 시간 없음
- **교과서 단원 구조** 그대로 따라감
- 교과서 텍스트를 **최대한 쪼개고 분석**해서 시각적으로 재구성
- 교과서 이미지/그래프/지도는 **캡쳐해서 그대로** 사용 (저작권 OK)

---

## 기본 제약 (web-slide-presenter 공통)

- 모든 슬라이드: `100vw × 100vh`, `overflow: hidden`, 스크롤 없음
- **슬라이드 콘텐츠는 화면 중앙 정렬**이 기본. CSS에 반드시 포함:
```css
.slide {
  display: flex;
  flex-direction: column;
  align-items: center;      /* 가로 중앙 */
  justify-content: center;  /* 세로 중앙 */
  padding: 5vh 8vw;         /* 양쪽 여백 충분히 */
}
```
- 콘텐츠 넘치면 **슬라이드를 쪼개라** (폰트 줄이지 마라)
- 순수 바닐라 JS, 외부 라이브러리 금지 (웹폰트 CDN 허용)
- 키보드 네비게이션: →/↓/Space = 다음, ←/↑ = 이전
- 단일 HTML 파일 (이미지는 별도 폴더)
- vw/vh 혼용 금지 — 원, 정사각형 등 비율 중요한 요소는 한 단위만

---

## 폰트

- **메인**: `'Pretendard'` — 제목, 숫자, 키워드, 라벨
  - CDN: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css`
- **서브**: `'Gowun Batang'` 볼드(700) 고정 — 설명문, 서술, 인용문, 사료 해석, 따뜻한 톤의 문장
  - CDN: `@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@700&display=swap');`
  - 역사 수업은 서사/이야기 중심이므로 Gowun Batang 비중이 일반 발표보다 높다
  - 교과서 서술 재구성 텍스트, 사료 번역, "~했다", "~이었다" 같은 서술체는 전부 Gowun Batang

---

## 색상 팔레트

과목 구분 없이 **통일된 역사 수업 팔레트**를 사용한다. 교과서 이미지(대부분 갈색/세피아 톤)와 충돌하지 않는 차분한 톤.

```
배경 (라이트): #faf8f5 (따뜻한 아이보리)
배경 (다크):   #1c1917 (따뜻한 차콜, 순수 블랙 아님)
텍스트:        #292524
서브텍스트:    #78716c
강조 (메인):   #92400e (앰버/호박색 — 역사적 따뜻함)
강조 (보조):   #166534 (짙은 녹색 — 성장/발전 표현 시)
위험/쇠퇴:     #991b1b (짙은 적색 — 전쟁, 위기, 쇠퇴)
라인/구분선:   #d6d3d1
```

- 슬라이드 배경은 라이트/다크 교차로 시각적 리듬
- 소단원 전환 시 다크 배경 슬라이드로 구분
- AI 클리셰(블랙+네온 퍼플/그린/블루) 절대 금지
- 이모지 사용 금지

---

## 글자 크기 (교실 뒷자리 가독성)

| 요소 | 최소 | 권장 |
|------|------|------|
| 단원/슬라이드 제목 | 4vw | 5~7vw |
| 소단원 제목 | 3vw | 3.5~4.5vw |
| 핵심 키워드/숫자 | 3vw | 4~6vw |
| 본문/설명 | 2vw | 2~2.5vw |
| 캡션/출처 | 1.4vw | 1.5~1.8vw |

**한국어 단어 줄바꿈 방지**: 한국어는 기본적으로 글자 단위로 줄바꿈되어 "백인 우월주" / "의" 처럼 단어 중간에서 잘린다. 이를 방지하기 위해 CSS에 반드시 아래를 추가:
```css
* { word-break: keep-all; overflow-wrap: break-word; }
```
`word-break: keep-all`은 한국어 단어 단위로 줄바꿈하고, `overflow-wrap: break-word`는 정말 긴 단어가 넘칠 때만 글자 단위로 자른다. 이 두 줄은 모든 슬라이드에 필수.

---

## 입력 처리: 교과서 PDF

사용자가 교과서 PDF를 제공하면:

**1단계: 자동 추출 스크립트 실행**
```bash
python <skill-dir>/scripts/extract_pdf.py <pdf경로> <출력폴더> --pages <범위>
```
이 스크립트가 자동으로:
- `text.txt` — 페이지별 전체 텍스트 추출
- `images/` — 모든 이미지를 `p3_img0.jpeg` 형태로 추출 (50px 미만 아이콘은 자동 스킵)
- `image_manifest.json` — 이미지 목록 (파일명, 페이지, 크기)

**2단계: 텍스트 분석**
- **본문만이 아니라 교과서의 모든 요소를 활용한다**: 양 날개의 작은 글씨, 사료 박스, 탐구 활동, 그래프 캡션, 지도 설명, 사진 캡션, 각주, 용어 설명 등. 교과서 페이지에 있는 모든 텍스트와 자료를 빠짐없이 슬라이드에 반영해야 한다

**3단계: 이미지 매칭**
- `image_manifest.json`을 읽고, 텍스트에서 언급하는 이미지(지도, 사진, 그래프 등)와 추출된 이미지 파일을 매칭
- 슬라이드에서 `<img src="images/p3_img0.jpeg">` 형태로 참조
- 텍스트의 캡션을 통해 어떤 이미지가 어떤 내용인지 파악

**4단계: 단원 구조 파악 후 슬라이드 생성**

**이미지 처리:**
- 사용자가 제공한 이미지는 별도 폴더에 저장 (예: `images/`)
- HTML에서 `<img src="images/지도1.png">` 형태로 참조
- base64 인라인은 5장 이하일 때만. 그 이상이면 별도 파일
- 이미지 슬라이드: `object-fit: contain`으로 비율 유지, 100vh 안에 맞춤

---

## 슬라이드 시퀀스: 단원 구조 → 슬라이드 매핑

교과서 단원의 일반적 구조를 슬라이드로 변환하는 규칙:

### 1. 단원 표지 (1장)
- 대단원 번호 + 제목을 크게
- 배경: 다크. 단원의 대표 이미지가 있으면 풀블리드로 깔고 텍스트 오버레이

### 2. 학습목표 (1장)
- 교과서의 학습목표를 프래그먼트로 순차 표시
- Gowun Batang으로 서술

### 3. 소단원별 슬라이드 (본문)
- 소단원 시작: 다크 배경 구분 슬라이드 (소단원 번호 + 제목)
- 이후 교과서 내용을 쪼개서 슬라이드화 (아래 "텍스트 재구성 규칙" 참고)
- **교과서 1페이지당 2~4장 슬라이드** 예상

### 4. 단원 정리 (1~2장)
- 핵심 키워드 정리
- 또는 교과서의 "단원 정리" 내용을 시각화

---

## 텍스트 재구성 규칙

교과서 서술문을 읽고, 아래 패턴 중 가장 적합한 것으로 변환한다. **텍스트를 그대로 옮기지 마라 — 쪼개고, 분석하고, 시각적으로 재구성하라.**

### 6×6 원칙
- 한 슬라이드에 **키워드 6개 이하**, 한 줄에 **6단어 이하**
- 문장이 아닌 **키워드** 중심으로 쪼개라
- 설명이 필요하면 Gowun Batang으로 짧은 서술문 1~2줄 추가

### 패턴 매칭

| 교과서 서술 유형 | 슬라이드 변환 | 예시 |
|-----------------|-------------|------|
| "A 때문에 B가 일어났다" (인과) | 흐름도/화살표 | 원인 → 과정 → 결과 |
| "A와 B를 비교하면" (비교) | 2단 비교표 | 조선 vs 일본, 전기 vs 후기 |
| "첫째, 둘째, 셋째" (나열) | 카드 3장 순차 등장 | 특징 3가지, 정책 3가지 |
| "1919년에... 1920년에..." (연대기) | 타임라인 | 3행 구조 (라벨/선+점/설명) |
| 수치 데이터 | 막대 그래프 | vh 단위 높이 |
| 사료/원문 인용 | 인용 레이아웃 | 원문 + 해석 + 출처 |
| 인물 설명 | 인물 카드 | 이름, 생몰년, 업적 |
| 지도/영토 설명 | 이미지 풀블리드 + 캡션 | 교과서 지도 캡쳐 사용 |

### 복잡한 서술 처리
- 3문장 이상의 단락 → 무조건 쪼개서 2장 이상의 슬라이드로
- 하나의 개념 = 하나의 슬라이드. 한 슬라이드에 두 개념 넣지 마라
- 쪼갤 때 기준: **서술의 뼈대(시간순 or 인과관계)**를 먼저 파악하고, 키워드 2~3개씩 시각 요소로 분배

---

## 역사 전용 슬라이드 유형

### 타임라인 (연대기)
스킬에서 검증된 3행 구조를 그대로 사용한다:

```html
<div class="timeline">
  <div class="tl-labels">
    <div class="tl-label">1876년</div>
    <div class="tl-label current">1894년</div>
    <div class="tl-label">1897년</div>
  </div>
  <div class="tl-track">
    <div class="tl-line"></div>
    <div class="tl-dot"></div>
    <div class="tl-dot current"></div>
    <div class="tl-dot"></div>
  </div>
  <div class="tl-descs">
    <div class="tl-desc">강화도 조약</div>
    <div class="tl-desc">갑오개혁</div>
    <div class="tl-desc">대한제국 선포</div>
  </div>
</div>
```

```css
/* 타임라인 전체를 CSS Grid로 구성. 열 수 = 이벤트 수. */
/* 라벨, 점, 설명이 같은 열에 있으므로 무조건 정렬됨. */
.timeline {
  display: grid;
  grid-template-columns: repeat(var(--tl-cols), 1fr); /* JS로 --tl-cols 설정 또는 HTML에서 직접 지정 */
  width: 85vw;
  margin: 0 auto;
  row-gap: 1vh;
}
/* 1행: 라벨 */
.tl-label {
  text-align: center;
  font-family: 'Pretendard'; font-size: 2vw; font-weight: 800;
  color: #92400e;
}
.tl-label.current { color: #166534; }
/* 2행: 점 + 선 (같은 그리드 행) */
.tl-dot-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 4vh;
}
/* 선: 첫 번째 점~마지막 점까지만 이어야 함 → 첫 셀~마지막 셀에 걸쳐서 배치 */
.tl-line-overlay {
  position: absolute;
  top: 50%; left: 0; right: 0;
  transform: translateY(-50%);
  height: 3px;
  background: #d6d3d1;
  z-index: 0;
  /* 부모 그리드 전체 너비에 걸침: 첫 번째 dot-cell에 넣고 width를 그리드 전체로 */
  grid-column: 1 / -1;
  pointer-events: none;
}
.tl-dot {
  width: 1.8vw; height: 1.8vw;
  border-radius: 50%;
  background: #92400e;
  border: 3px solid #faf8f5;
  z-index: 1;
}
.tl-dot.current {
  width: 2.4vw; height: 2.4vw;
  background: #166534;
  box-shadow: 0 0 0 4px rgba(22,101,52,0.3);
}
/* 3행: 설명 */
.tl-desc {
  text-align: center;
  font-family: 'Gowun Batang', serif; font-weight: 700;
  font-size: 1.5vw; color: #78716c;
}
```

```html
<!-- 예시: 이벤트 3개 → grid-template-columns: repeat(3, 1fr) -->
<div class="timeline" style="grid-template-columns: repeat(3, 1fr);">
  <!-- 1행: 라벨 -->
  <div class="tl-label">1876년</div>
  <div class="tl-label current">1894년</div>
  <div class="tl-label">1897년</div>
  <!-- 2행: 선 + 점 -->
  <div class="tl-dot-cell" style="grid-column: 1 / -1; display: flex; justify-content: space-around; position: relative;">
    <div class="tl-line-overlay"></div>
    <div class="tl-dot"></div>
    <div class="tl-dot current"></div>
    <div class="tl-dot"></div>
  </div>
  <!-- 3행: 설명 -->
  <div class="tl-desc">강화도 조약</div>
  <div class="tl-desc">갑오개혁</div>
  <div class="tl-desc">대한제국 선포</div>
</div>
```

핵심: **CSS Grid의 열(column)이 정렬을 보장한다.** 라벨, 점, 설명이 같은 열 너비를 공유하므로 어긋날 수 없다. 점들은 `tl-dot-cell` 안에서 `justify-content: space-around`로 균등 배치되고, 선은 같은 셀 안에서 absolute로 깔린다.

10개 이상 사건일 때: 2단 타임라인(위/아래 교차 배치) 또는 2장 슬라이드로 분할.

### 인과관계도
```
원인 ──→ 과정 ──→ 결과
```
- 가로 3단 flexbox, 화살표(→)로 연결
- 각 단계는 프래그먼트로 순차 등장
- 원인=적색 톤, 과정=중립, 결과=녹색 톤

### 사료/원문 인용 레이아웃
원문 사료가 나오면 **슬라이드 배경을 다크(#1c1917)로 전환**한다. 오래된 문서를 꺼내 보는 듯한 고풍스러운 분위기를 만든다. 사진 자료 슬라이드는 라이트 배경 그대로.

```html
<!-- 사료 슬라이드는 다크 배경 -->
<div class="slide dark">
  <div class="source-quote">
    <div class="source-original">"원문 텍스트 (한문/영어 등)"</div>
    <div class="source-translation">현대어 해석</div>
    <div class="source-meta">— 출처, 연도</div>
  </div>
</div>
```
- `.source-original`: Gowun Batang, 밝은 아이보리색(#faf8f5), 큰 따옴표와 함께
- `.source-translation`: Gowun Batang, 앰버 강조색(#d97706), 본문 크기
- `.source-meta`: Pretendard, 캡션 크기, 어두운 서브텍스트(#a8a29e)

### 인물 카드
```html
<div class="person-card">
  <div class="person-initial">세</div>  <!-- 이름 첫 글자 -->
  <div class="person-name">세종대왕</div>
  <div class="person-dates">1397~1450</div>
  <div class="person-desc">훈민정음 창제, 과학기술 발전</div>
</div>
```
- 이니셜 원형 아바타 + 이름 + 생몰년 + 핵심 업적
- 2~4명이면 가로 그리드, 프래그먼트 순차 등장

### 이미지 풀블리드 + 캡션
교과서에서 캡쳐한 지도/그림/사진을 보여줄 때:
```html
<div class="img-slide">
  <img src="images/지도.png" alt="삼국시대 영토">
  <div class="img-caption">삼국시대 영토 변화 (5세기)</div>
</div>
```
```css
.img-slide { position: relative; width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; }
.img-slide img { max-width: 90vw; max-height: 80vh; object-fit: contain; }
.img-caption { position: absolute; bottom: 4vh; font-family: 'Gowun Batang'; font-weight: 700; font-size: 1.8vw; color: #78716c; }
```

### 비교표
```html
<div class="compare">
  <div class="compare-col">
    <h3>조선 전기</h3>
    <ul>
      <li class="fragment">중앙집권 강화</li>
      <li class="fragment">과전법 시행</li>
    </ul>
  </div>
  <div class="compare-divider"></div>
  <div class="compare-col">
    <h3>조선 후기</h3>
    <ul>
      <li class="fragment">세도정치</li>
      <li class="fragment">대동법 확대</li>
    </ul>
  </div>
</div>
```

### 막대 그래프
수치 데이터가 있을 때. **height를 vh 단위 inline style로 지정**:
```html
<div class="bar-chart">
  <div class="bar-col">
    <div class="bar" style="height: 8vh;"></div>
    <span class="bar-val">120만</span>
    <span class="bar-label">1800년</span>
  </div>
  <!-- 반복 -->
</div>
```

---

## 프래그먼트 (빌드 효과)

### 반드시 써야 하는 곳
- 같은 레벨 항목 나열 (카드, 리스트, 타임라인 이벤트) → 순차 등장
- 인과관계도의 원인 → 과정 → 결과 → 하나씩 공개
- 비교표의 양쪽 항목
- 사료 인용의 원문 → 해석 → 출처 순서

### 쓰지 마라
- 단원 표지, 소단원 구분 슬라이드 (간결해서 필요 없음)
- 이미지 풀블리드 슬라이드 (이미지 자체가 내용)

---

## 동심원 금지

CSS 동심원(concentric circles)은 겹침 문제가 반복 발생하므로 **절대 사용하지 마라**. 대안: 가로 막대, 카드 나열, 세로 스택.

---

## 언어 원칙

사용자가 한국어로 요청하면 모든 콘텐츠 한국어. 섹션 라벨도 한국어. 고유명사/학술 용어만 영어/한자 허용.

---

## 출력 구조

```
단원명/
├── index.html     (슬라이드 본체)
└── images/        (교과서 캡쳐 이미지들)
    ├── 지도1.png
    ├── 그래프1.png
    └── ...
```

이미지가 없으면 단일 HTML 파일로 출력.

---

## 체크리스트

- [ ] 모든 슬라이드가 전체화면, 스크롤 없음
- [ ] 교과서 단원 구조를 따라가는가
- [ ] 교과서 텍스트를 쪼개서 시각적으로 재구성했는가 (원문 그대로 복붙 아님)
- [ ] 6×6 원칙: 키워드 6개 이하, 한 줄 6단어 이하
- [ ] 같은 레벨 항목은 프래그먼트로 순차 등장
- [ ] 타임라인은 3행 구조 (라벨/선+점/설명)
- [ ] 막대 그래프 height는 vh 단위
- [ ] Pretendard(제목/숫자) + Gowun Batang 700(서술/인용)
- [ ] 이모지 없음, AI 클리셰 색상 없음
- [ ] 키보드 네비게이션 작동
