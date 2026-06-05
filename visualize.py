"""
Visualization Module
Visualizes temperature data with anomalies highlighted
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def visualize_temperatures():
    """
    Creates a visualization of temperature data with anomalies
    Normal temperatures: blue line
    Anomalies: red points
    Includes statistics box with summary information
    """
    
    try: 
        # Load the data with anomalies
        # 이상치 정보가 포함된 CSV 파일을 읽어서 표(DataFrame)로 불러옴
        df = pd.read_csv("weather_with_anomalies.csv")
        # 문자열로 읽힌 날짜 컬럼을 진짜 날짜(datetime) 타입으로 변환
        df["date"] = pd.to_datetime(df["date"])
        
        if df.empty: #데이터가 비어있는지 확인
            print("✗ No data found in weather_with_anomalies.csv") 
            print("  Please run detect.py first.")
            return
        
        print("Creating visualization...") #그래프 생성 시작 알림
        
        # Create figure and axis
        # 그림(fig)과 좌표축(ax)을 생성, figsize로 그래프 크기(가로14, 세로7) 지정
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Separate normal and anomaly data
        normal_data = df[~df["is_anomaly"]] #정상 데이터 추출
        anomaly_data = df[df["is_anomaly"]] #이상치만 따로 추출
        
        # Plot normal temperatures as a blue line
        # 정상 기온을 파란색 선(line)으로 그림 (alpha는 투명도)
        ax.plot(normal_data["date"], normal_data["max_temp"], 
                color="blue", linewidth=2, label="Normal Temperature", alpha=0.7)
        
        # Plot anomalies as red points
        #이상치를 빨간색 점으로 강조해서 표시 (s는 점 크기, zorder는 겹침 순서)
        ax.scatter(anomaly_data["date"], anomaly_data["max_temp"], 
                   color="red", s=100, label="Anomaly (Heat Wave/Cold Snap)", 
                   marker="o", zorder=5, edgecolors="darkred", linewidth=1.5)
        
        # Add moving average (7-day)
        df_sorted = df.sort_values("date") #계산을위해 날짜순으로 데이터 정렬 
        moving_avg = df_sorted["max_temp"].rolling(window=7, center=True).mean()#7일 단위 이동평균 계산
        ax.plot(df_sorted["date"], moving_avg, #주황색 점선으로 표시
                color="orange", linewidth=2, label="7-day Moving Average", 
                linestyle="--", alpha=0.6)
        
        # Formatting 그래프 서식 설정
        ax.set_xlabel("Date", fontsize=12, fontweight="bold") 
        ax.set_ylabel("Maximum Temperature (°C)", fontsize=12, fontweight="bold")
        ax.set_title("Seoul Temperature Analysis - Anomaly Detection", 
                     fontsize=14, fontweight="bold", pad=20)
        
        # Format x-axis to show dates nicely
        ax.xaxis.set_major_locator(mdates.MonthLocator()) #x축 눈금을 월 단위로 표시 
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m")) #x축 날짜 표기 형식을 연 월 형태로 지정
        plt.xticks(rotation=45, ha="right") #글자 기울이고 오른쪽 정렬
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle="--") #그리드
        
        # Add legend
        ax.legend(loc="upper left", fontsize=10, framealpha=0.95) #범례 왼쪾 위 표시
        
        # Calculate statistics
        total_records = len(df) #전체 데이터행 
        anomaly_count = len(anomaly_data)#이상치
        normal_count = len(normal_data)#정상
        avg_temp = df["max_temp"].mean()#평균기온
        min_temp = df["max_temp"].min()#최저기온
        max_temp = df["max_temp"].max()#최고기온
        
        # Add statistics box
        stats_text = ( #문자열로구성 
            f"📊 Statistics\n"
            f"─────────────────\n"
            f"Total Records: {total_records}\n"
            f"Anomalies: {anomaly_count} ({100*anomaly_count/total_records:.1f}%)\n"
            f"Normal: {normal_count}\n"
            f"─────────────────\n"
            f"Avg Temp: {avg_temp:.1f}°C\n"
            f"Min Temp: {min_temp:.1f}°C\n"
            f"Max Temp: {max_temp:.1f}°C"
        )
        
        props = dict(boxstyle="round", facecolor="wheat", alpha=0.8) # 통계 박스의 모양/색/투명도 설정 (둥근 모서리, 밀짚색 배경)
       # 통계 텍스트를 그래프 좌상단(0.02, 0.97 위치)에 박스 형태로 표시
        ax.text(0.02, 0.97, stats_text, transform=ax.transAxes, 
                fontsize=10, verticalalignment="top", bbox=props, 
                family="monospace")
        
        # Tight layout
        plt.tight_layout() #레이아웃 정리
        
        # Save figure 파일 이름 지정
        output_file = "temperature_analysis.png"
        plt.savefig(output_file, dpi=300, bbox_inches="tight") #여백 최소화
        print(f"✓ Visualization saved to {output_file}") #저장 알림
        
        # Display the plot
        plt.show() #화면에 그래프 보여줌
        
    except FileNotFoundError: #csv파일 존재 안할때
        print("✗ weather_with_anomalies.csv not found.")
        print("  Please run detect.py first.")
    except Exception as e: #그외오류알림
        print(f"✗ Error during visualization: {e}")


if __name__ == "__main__":
    visualize_temperatures()
