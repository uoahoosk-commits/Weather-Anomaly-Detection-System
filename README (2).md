# 🌡️ Weather Anomaly Detection System

서울의 일별 최고기온 데이터를 수집하여 **Isolation Forest** 알고리즘으로 이상기온(폭염/한파)을 자동 탐지하고 시각화합니다.

---

## 📦 설치

```bash
pip install -r requirements.txt
```

> 필요 패키지: `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `requests`

---

## 🚀 실행 순서

```bash
python collect_data.py   # 1. Open-Meteo API로 1년치 기온 데이터 수집
python detect.py         # 2. 이상기온 탐지 (폭염/한파 분류)
python visualize.py      # 3. 그래프 시각화 → temperature_analysis.png
```

---

## 📁 파일 구조

| 파일 | 설명 |
|------|------|
| `collect_data.py` | 데이터 수집 |
| `detect.py` | 이상탐지 |
| `visualize.py` | 시각화 |
| `weather.csv` | 수집된 기온 데이터 (자동 생성) |
| `weather_with_anomalies.csv` | 이상탐지 결과 (자동 생성) |
| `temperature_analysis.png` | 시각화 그래프 (자동 생성) |

---

## 🔧 주요 설정

| 항목 | 파일 | 변경 방법 |
|------|------|-----------|
| 수집 기간 | `collect_data.py` | `timedelta(days=365)` 수정 |
| 수집 지역 | `collect_data.py` | `latitude`, `longitude` 수정 |
| 이상치 비율 | `detect.py` | `contamination=0.05` 수정 |
| 이동평균 기간 | `visualize.py` | `rolling(window=7)` 수정 |

---

## 📚 References

- [Open-Meteo API](https://open-meteo.com/)
- [Isolation Forest](https://scikit-learn.org/stable/modules/ensemble.html#isolation-forest)
