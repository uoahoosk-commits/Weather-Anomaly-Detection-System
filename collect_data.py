"""
Weather Data Collection Module
Collects historical daily maximum temperature data for Seoul using Open-Meteo API
"""

import requests
import pandas as pd
from datetime import datetime, timedelta


def collect_weather_data():
    """
    Collects 1 year of daily maximum temperature data for Seoul
    using the Open-Meteo API (latitude: 37.5665, longitude: 126.9780)
    Saves the result to weather.csv
    """
    
    # API configuration
    latitude = 37.5665 #서울 위도
    longitude = 126.9780 #서울 경도
    
    # Calculate date range (past 1 year from today)
    end_date = datetime.now().date()#오늘 날짜를 갖져옴ㅁ (조회 종료일로 사용)
    start_date = end_date - timedelta(days=365) #오늘로부터 365일 전 날짜 계산
    
    # Open-Meteo API endpoint
    url = "https://archive-api.open-meteo.com/v1/archive"#Open-Meteo의 과거 기상 데이터(아카이브) API 주소

    
    params = {  # 조건을 딕셔너리로 정리
        "latitude": latitude, #조회할 지점의 위도
        "longitude": longitude, #경도
        "start_date": start_date.strftime("%Y-%m-%d"), #조회시작일 문자열로 변환
        "end_date": end_date.strftime("%Y-%m-%d"), # 조회 종료일 
        "daily": "temperature_2m_max", #일 단위 데이터 중 일 최고기온 요청 
        "timezone": "Asia/Seoul" #시간대를 서울로 설정 
    }
    
    try: #try except 로 오류 정리
        print(f"Fetching weather data from {start_date} to {end_date}...") #현재 어떤 시간을 조회하는지 출력 
        response = requests.get(url, params=params)#위에서 만든 주소와 조건으로 요청을 보내고 응답을 받음  
        response.raise_for_status() #응답 상태가 오류(4xx, 5xx)면 예외를 발생시켜 except 블록으로 넘김
        
        data = response.json() #json으로 파일 변환
        
        # Extract data
        dates = data["daily"]["time"] #응답 데이터에서 날짜 목록을 꺼냄 (daily 안의 time 리스트)
        temps = data["daily"]["temperature_2m_max"] #응답 데이터에서 일 최고기온 목록을 꺼냄 (daily 안의 temperature_2m_max 리스트)
        
        # Create DataFrame
        df = pd.DataFrame({
            "date": dates, #날짜목록 컬럼 생성
            "max_temp": temps #일 최고기온 목록 컬럼 생성
        })
        
        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"])
        #문자열로 들어온 날짜 컬럼을 진짜 날짜 타입으로 변환
        # Save to CSV
        df.to_csv("weather.csv", index=False, encoding="utf-8") # 완성된 표 저장, 자동행번호 저장 안함
       
        print(f"✓ Data saved to weather.csv") #저장 알림
        print(f"  - Total records: {len(df)}") # 총 몇 개의 데이터가 저장됐는지 출력
        print(f"  - Date range: {df['date'].min().date()} to {df['date'].max().date()}") #실제로 저장된 데이터의 시작 날짜와 끝 날짜를 출력
        print(f"  - Temperature range: {df['max_temp'].min()}°C to {df['max_temp'].max()}°C") #기온의 최저값과 최고값(범위)을 출력
        
        return df #만들어진 데이터프레임을 함수 결과로 돌려줌 
    
    except requests.exceptions.RequestException as e: #네트워크 관련 오류났을때 처리
        print(f"✗ Error fetching data from API: {e}")
        return None #실패했으므로 none을 반환
    except Exception as e:# 그 외 데이터 가공 등에서 생긴 오류 처리
        print(f"✗ Error processing data: {e}")
        return None

# 이 파일을 직접 실행했을 때만 아래 코드를 동작시킴 (다른 파일에서 import하면 실행 안 됨)
if __name__ == "__main__":
    collect_weather_data()
