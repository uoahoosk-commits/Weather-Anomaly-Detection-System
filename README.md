# 🌡️ Weather Anomaly Detection System (날씨 온도 이상탐지)

A Python-based anomaly detection system for Seoul's temperature data using machine learning and Open-Meteo API.

## 📋 Project Overview

이 프로젝트는 서울의 일별 최고기온 데이터를 수집하여 Isolation Forest 알고리즘으로 이상기온(폭염 또는 한파)을 자동으로 탐지하고 시각화합니다.

**주요 목표:**
- Open-Meteo API를 통한 1년치 기온 데이터 자동 수집
- 머신러닝(Isolation Forest)을 이용한 이상기온 탐지
- 폭염 vs 한파 자동 분류
- 전문적 데이터 시각화

---

## 🎯 Project Structure

```
.
├── collect_data.py           # 데이터 수집 모듈
├── detect.py                 # 이상탐지 모듈
├── visualize.py              # 시각화 모듈
├── requirements.txt          # 파이썬 패키지 의존성
├── weather.csv               # 수집된 기온 데이터 (자동 생성)
├── weather_with_anomalies.csv # 이상탐지 결과 (자동 생성)
└── temperature_analysis.png  # 시각화 그래프 (자동 생성)
```

---

## 📦 Installation

### 1. Python 설치 확인
```bash
python --version  # Python 3.8 이상 필요
```

### 2. 의존성 패키지 설치
```bash
pip install -r requirements.txt
```

**필요한 패키지:**
- `pandas` - 데이터 처리
- `numpy` - 수치 계산
- `matplotlib` - 그래프 시각화
- `scikit-learn` - 머신러닝 (Isolation Forest)
- `requests` - API 호출

---

## 🚀 Quick Start

### Step 1: 데이터 수집
서울의 1년치 일별 최고기온 데이터를 Open-Meteo API에서 수집합니다.

```bash
python collect_data.py
```

**출력 예시:**
```
Fetching weather data from 2025-05-06 to 2026-05-06...
✓ Data saved to weather.csv
  - Total records: 365
  - Date range: 2025-05-06 to 2026-05-06
  - Temperature range: 8.5°C to 37.2°C
```

### Step 2: 이상기온 탐지
Isolation Forest 알고리즘으로 이상기온을 자동 탐지합니다.

```bash
python detect.py
```

**출력 예시:**
```
Loaded 365 temperature records

============================================================
🌡️  이상 기온 탐지 결과
============================================================
정상 기온: 345개
이상 기온: 20개
  - 폭염: 12개
  - 한파: 8개

평균 기온: 18.5°C
기온 범위: 8.5°C ~ 37.2°C
```

### Step 3: 시각화 생성
기온 데이터와 이상탐지 결과를 그래프로 시각화합니다.

```bash
python visualize.py
```

**생성 파일:**
- `temperature_analysis.png` - 고해상도(300 DPI) 그래프

**그래프 특징:**
- 🔵 파란선: 정상 기온
- 🔴 빨간점: 이상 기온 (폭염/한파)
- 🟠 주황선: 7일 이동평균
- 📊 통계 정보 박스

---

## 📊 Data Files

### weather.csv (입력)
```csv
date,max_temp
2025-05-06,22.5
2025-05-07,24.1
2025-05-08,20.3
...
```

### weather_with_anomalies.csv (출력)
```csv
date,max_temp,is_anomaly,anomaly_score,type
2025-05-06,22.5,False,-0.523,정상
2025-05-07,24.1,False,-0.541,정상
2025-07-15,35.8,True,0.812,폭염 (Heat Wave)
...
```

---

## 🤖 Algorithm: Isolation Forest

**작동 원리:**
1. 각 특성(기온)의 값에 대해 랜덤하게 분할
2. 이상치는 정상치보다 적은 분할로 고립됨
3. 고립되기 쉬운 데이터를 이상치로 분류

**장점:**
- ✅ 이상치의 개수를 미리 지정 가능 (contamination 파라미터)
- ✅ 계산이 빠르고 효율적
- ✅ 비지도 학습 (라벨 필요 없음)
- ✅ 다차원 데이터에도 적용 가능

**파라미터:**
- `contamination`: 예상되는 이상치 비율 (기본값: 5%)
- `random_state`: 재현성을 위한 난수 시드 (기본값: 42)
- `n_estimators`: 트리의 개수 (기본값: 100)

---

## 🔧 Customization

### 1. 기온 수집 기간 변경
`collect_data.py` 수정:
```python
# 예: 2년치 데이터 수집
start_date = end_date - timedelta(days=730)  # 365 -> 730
```

### 2. 서울 이외 다른 지역 데이터 수집
`collect_data.py` 수정:
```python
# 서울 좌표 대신 다른 지역 좌표 사용
latitude = 37.5665    # 부산: 35.1796
longitude = 126.9780  # 부산: 129.0756
```

### 3. 이상치 비율 조정
`detect.py` 수정:
```python
# 더 많은 이상치를 탐지하려면 contamination 값 증가
iso_forest = IsolationForest(
    contamination=0.1,  # 10%로 증가
    random_state=42,
    n_estimators=100
)
```

### 4. 이동평균 윈도우 크기 변경
`visualize.py` 수정:
```python
# 14일 이동평균으로 변경
moving_avg = df_sorted["max_temp"].rolling(window=14, center=True).mean()
```

---

## 📈 Output Examples

### 콘솔 출력
```
Loaded 365 temperature records

============================================================
🌡️  이상 기온 탐지 결과
============================================================
정상 기온: 345개
이상 기온: 20개
  - 폭염: 12개 (35°C 이상)
  - 한파: 8개 (10°C 이하)

평균 기온: 18.5°C
기온 범위: 8.5°C ~ 37.2°C
```

### CSV 출력
탐지된 모든 날짜의 기온, 이상여부, 이상도 점수, 분류 결과 저장

### 그래프 출력
- 고해상도(300 DPI) PNG 파일
- 정상 기온: 파란선
- 이상 기온: 빨간 점
- 기온 추세: 주황 점선 (7일 이동평균)
- 통계 정보: 우측 상단 박스

---

## 🐛 Troubleshooting

### 1. "weather.csv not found" 에러
**원인:** 데이터 수집을 먼저 하지 않음
**해결:** `python collect_data.py` 먼저 실행

### 2. API 연결 에러
**원인:** 인터넷 연결 불안정 또는 API 서버 문제
**해결:** 잠시 후 다시 시도하거나 인터넷 연결 확인

### 3. "No module named 'sklearn'" 에러
**원인:** scikit-learn 패키지 미설치
**해결:** `pip install scikit-learn` 실행

### 4. 그래프가 표시되지 않음
**원인:** matplotlib 백엔드 문제
**해결:** 
```bash
pip install --upgrade matplotlib
```

---

## 📚 References

- **Open-Meteo API**: https://open-meteo.com/
- **Isolation Forest**: https://scikit-learn.org/stable/modules/ensemble.html#isolation-forest
- **Pandas Documentation**: https://pandas.pydata.org/
- **Matplotlib Documentation**: https://matplotlib.org/

---

## 📝 License

MIT License - 자유롭게 사용 및 수정 가능합니다.

---

## 👨‍💻 Author

작성일: 2026-05-06  
Python 3.8+

---

## ✨ Features

- ✅ 자동 데이터 수집 (Open-Meteo API)
- ✅ 머신러닝 기반 이상탐지 (Isolation Forest)
- ✅ 폭염/한파 자동 분류
- ✅ 전문적 데이터 시각화
- ✅ CSV 형식 결과 저장
- ✅ 상세한 통계 정보
- ✅ 완벽한 에러 처리
- ✅ 한글 지원
