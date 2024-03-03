# -*- coding: utf-8 -*-   # 파일 인코딩 형식을 파일 첫머리에 명시해주어 인코딩 오류를 방지함

import os 
import sys
import datetime as dt
import schedule
import time
import pymysql
import datetime
import subprocess

# #MYSQL연결
try: 
    conn = pymysql.connect(host='175.121.197.205',port =3306, user='bkc_manager', password='bkcManager1234@', db='smart_lora', charset='utf8')
    print(f" DB연동완료")
except:
    print(f"DB연동 중 문제 발생. 유저 이름, 비밀번호 혹은 사용자권한이 설정되어 있는지 재확인하세요")

#커서생성
cur = conn.cursor()
#입력 쿼리 작성
try:
    
    sql_inputmaker = f"""select distinct b.* from equipment a, facility b, equipment_type c
where a.dno > 0
and a.type_dno = c.dno
and binary c.service like '%c%'
and binary c.service like '%d%'
and a.facility_dno = b.dno
;"""
    cur.execute(sql_inputmaker)
    
    # 결과 추출
    result_input = cur.fetchall()  # 모든 결괏값 반환


    # 특정 컬럼 값 변수화
    latitude_input = result_input[0][7]  # 위도 값을 변수에 저장
    longitude_input = result_input[0][8] # 경도 값을 변수에 저장

    print(latitude_input)
    print(longitude_input)
    

except:
    print(f"쿼리에 오류 발생. 문법 및 기타 사항 재확인하세요.")
    
# 쿼리 실행
cur.execute(sql_inputmaker)
# 입력값 저장
conn.commit()
print(f" 입력값 저장 완료")
# MYSQL 연결 종료
conn.close()


current_date = dt.date.today() # datetime.date.today()메서드로 오늘 날짜 반환
current_date_input = current_date.strftime('%Y%m%d') # start_date가 요구하는 형식은 'yyyymmdd' 형식이므로, strftime메서드를 활용해 문자열로 바꿈
   


# dt.datetime.now()메서드로 오늘 날짜 반환. 2023-12-07 형식으로 내보냄

previous_date = current_date - dt.timedelta(days=1) # current_date로부터 하루 후 날짜 계산
previous_date_input = previous_date.strftime('%Y%m%d') # start_date가 요구하는 형식은 'yyyymmdd' 형식이므로, strftime메서드를 활용해 문자열로 바꿈
previous_seven_date = current_date - dt.timedelta(days=7)# current_date로부터 하루 전 날짜 계산
previous_seven_date_input = previous_seven_date.strftime('%Y%m%d') # start_date가 요구하는 형식은 'yyyymmdd' 형식이므로, strftime메서드를 활용해 문자열로 바꿈


start_date = previous_seven_date_input
end_date = previous_date_input
first_api_input='01e9193c9c3f6b3631db3612599f6246'
second_api_input='ghBQh0IXRimQUIdCFzYp4w'
print(start_date)
print(type(start_date))
print(end_date)
print(type(end_date))
print(first_api_input)
print(type(first_api_input))
print(second_api_input)
print(type(second_api_input))



def get_script_path(filename):
    # 사용자 홈 디렉터리에 있는 'Desktop' 폴더 경로를 얻음
    user_desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    # 'Desktop' 폴더 아래에 'Battery_Charging_Algorithm' 폴더 경로를 추가
    folder_path = os.path.join(user_desktop, 'Battery_Charging_Algorithm')

    # 'Battery_Charging_Algorithm' 폴더가 존재하지 않는 경우 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 'Battery_Charging_Algorithm' 폴더 안에 지정된 파일의 경로를 반환
    return os.path.join(folder_path, filename)

# py 파일을 실행하는 함수
def execute_py(file_name, start_date, end_date, latitude_input, longitude_input, first_api_input, second_api_input):
    file_path = get_script_path(file_name)  # 파일 경로 동적 설정

    # 파일 경로 유효성 검사
    if not os.path.exists(file_path):
        print(f"파일 경로가 유효하지 않습니다: {file_path}")
        return  # 파일이 없으면 함수 실행 중단

    try:
        subprocess.run(['python', file_path, start_date, end_date, latitude_input, longitude_input, first_api_input, second_api_input], check=True)
    except subprocess.CalledProcessError as e:
        print(f"execute함수 실행 중 작업 실행 중 오류 발생: {e}")
        

def scheduled_job():
    for file_name in py_files:
        execute_py(file_name=file_name, 
                   start_date=previous_seven_date_input, 
                   end_date=previous_date_input, 
                   latitude_input=latitude_input, 
                   longitude_input=longitude_input, 
                   first_api_input='01e9193c9c3f6b3631db3612599f6246', 
                   second_api_input='ghBQh0IXRimQUIdCFzYp4w')


    #with open(file_path, 'r', encoding='utf-8-sig') as file:
    #    exec(file.read())



# 실행할 py 파일의 목록
py_files = ["API.py","API_2.py","get_battery_charge_DB.py"] # 본 스크립트 파일(Auto_Script)과 같은 디렉토리

try:
    while start_date <= end_date: #현재날짜가 종료날짜에 도달할 떄까지
        for file in py_files:# 실행할 py파일들에 대해서
            # execute_py(file, current_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"), float(latitude_input), float(longitude_input),  first_api_input.replace(" ", "").replace(".", ""),second_api_input.replace(" ", "").replace(".", "") )  # execute함수 실행하여 각 py파일에 대하여 정해 둔 파이썬 스크립트 실행. 문자열 형태로 변환하여 전달
            execute_py(file, start_date, end_date, latitude_input, longitude_input,  first_api_input,second_api_input )
        start_date += datetime.timedelta(days=1)  # 한 개의 파일 실행이 완료되면 timedelta 활용하여 다음 날짜로 이동
except:

    paths = [r"C:\Users\user1\Desktop\Battery_Charging_Algorithm\API.py",r"C:\Users\user1\Desktop\Battery_Charging_Algorithm\API_2.py",r"C:\Users\user1\Desktop\Battery_Charging_Algorithm\get_battery_charge_DB.py" ]

    while start_date <= end_date: #현재날짜가 종료날짜에 도달할 떄까지
          for path in paths:# 실행할 py파일들에 대해서
                # execute_py(file, current_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"), float(latitude_input), float(longitude_input),  first_api_input.replace(" ", "").replace(".", ""),second_api_input.replace(" ", "").replace(".", "") )  # execute함수 실행하여 각 py파일에 대하여 정해 둔 파이썬 스크립트 실행. 문자열 형태로 변환하여 전달
                execute_py(path, start_date, end_date, latitude_input, longitude_input,  first_api_input,second_api_input )
                start_date += datetime.timedelta(days=1)  # 한 개의 파일 실행이 완료되면 timedelta 활용하여 다음 날짜로 이동

 
print(sys.argv)

#schedule.every().day.at("21:10").do(scheduled_job)

#while True:
#    # 파일 경로가 유효하지 않으면 루프 중단
#    current_datetime = datetime.datetime.now() 
#    print(f"예약작업실행조건 체크 중..{current_datetime}")

#    schedule.run_pending()
#    time.sleep(1) # 1초마다 작업실행조건이 충족되었는지 검사         