# -*- coding: utf-8 -*-   # ���� ���ڵ� ������ ���� ù�Ӹ��� ������־� ���ڵ� ������ ������

import os 
import sys
import datetime as dt
import schedule
import time
import pymysql
import datetime
import subprocess

# #MYSQL����
try: 
    conn = pymysql.connect(host='175.121.197.205',port =3306, user='bkc_manager', password='bkcManager1234@', db='smart_lora', charset='utf8')
    print(f" DB�����Ϸ�")
except:
    print(f"DB���� �� ���� �߻�. ���� �̸�, ��й�ȣ Ȥ�� ����ڱ����� �����Ǿ� �ִ��� ��Ȯ���ϼ���")

#Ŀ������
cur = conn.cursor()
#�Է� ���� �ۼ�
try:
    
    sql_inputmaker = f"""select distinct b.* from equipment a, facility b, equipment_type c
where a.dno > 0
and a.type_dno = c.dno
and binary c.service like '%c%'
and binary c.service like '%d%'
and a.facility_dno = b.dno
;"""
    cur.execute(sql_inputmaker)
    
    # ��� ����
    result_input = cur.fetchall()  # ��� �ᱣ�� ��ȯ


    # Ư�� �÷� �� ����ȭ
    latitude_input = result_input[0][7]  # ���� ���� ������ ����
    longitude_input = result_input[0][8] # �浵 ���� ������ ����

    print(latitude_input)
    print(longitude_input)
    

except:
    print(f"������ ���� �߻�. ���� �� ��Ÿ ���� ��Ȯ���ϼ���.")
    
# ���� ����
cur.execute(sql_inputmaker)
# �Է°� ����
conn.commit()
print(f" �Է°� ���� �Ϸ�")
# MYSQL ���� ����
conn.close()


current_date = dt.date.today() # datetime.date.today()�޼���� ���� ��¥ ��ȯ
current_date_input = current_date.strftime('%Y%m%d') # start_date�� �䱸�ϴ� ������ 'yyyymmdd' �����̹Ƿ�, strftime�޼��带 Ȱ���� ���ڿ��� �ٲ�
   


# dt.datetime.now()�޼���� ���� ��¥ ��ȯ. 2023-12-07 �������� ������

previous_date = current_date - dt.timedelta(days=1) # current_date�κ��� �Ϸ� �� ��¥ ���
previous_date_input = previous_date.strftime('%Y%m%d') # start_date�� �䱸�ϴ� ������ 'yyyymmdd' �����̹Ƿ�, strftime�޼��带 Ȱ���� ���ڿ��� �ٲ�
previous_seven_date = current_date - dt.timedelta(days=7)# current_date�κ��� �Ϸ� �� ��¥ ���
previous_seven_date_input = previous_seven_date.strftime('%Y%m%d') # start_date�� �䱸�ϴ� ������ 'yyyymmdd' �����̹Ƿ�, strftime�޼��带 Ȱ���� ���ڿ��� �ٲ�


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
    # ����� Ȩ ���͸��� �ִ� 'Desktop' ���� ��θ� ����
    user_desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    # 'Desktop' ���� �Ʒ��� 'Battery_Charging_Algorithm' ���� ��θ� �߰�
    folder_path = os.path.join(user_desktop, 'Battery_Charging_Algorithm')

    # 'Battery_Charging_Algorithm' ������ �������� �ʴ� ��� ����
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 'Battery_Charging_Algorithm' ���� �ȿ� ������ ������ ��θ� ��ȯ
    return os.path.join(folder_path, filename)

# py ������ �����ϴ� �Լ�
def execute_py(file_name, start_date, end_date, latitude_input, longitude_input, first_api_input, second_api_input):
    file_path = get_script_path(file_name)  # ���� ��� ���� ����

    # ���� ��� ��ȿ�� �˻�
    if not os.path.exists(file_path):
        print(f"���� ��ΰ� ��ȿ���� �ʽ��ϴ�: {file_path}")
        return  # ������ ������ �Լ� ���� �ߴ�

    try:
        subprocess.run(['python', file_path, start_date, end_date, latitude_input, longitude_input, first_api_input, second_api_input], check=True)
    except subprocess.CalledProcessError as e:
        print(f"execute�Լ� ���� �� �۾� ���� �� ���� �߻�: {e}")
        

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



# ������ py ������ ���
py_files = ["API.py","API_2.py","get_battery_charge_DB.py"] # �� ��ũ��Ʈ ����(Auto_Script)�� ���� ���丮

try:
    while start_date <= end_date: #���糯¥�� ���ᳯ¥�� ������ ������
        for file in py_files:# ������ py���ϵ鿡 ���ؼ�
            # execute_py(file, current_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"), float(latitude_input), float(longitude_input),  first_api_input.replace(" ", "").replace(".", ""),second_api_input.replace(" ", "").replace(".", "") )  # execute�Լ� �����Ͽ� �� py���Ͽ� ���Ͽ� ���� �� ���̽� ��ũ��Ʈ ����. ���ڿ� ���·� ��ȯ�Ͽ� ����
            execute_py(file, start_date, end_date, latitude_input, longitude_input,  first_api_input,second_api_input )
        start_date += datetime.timedelta(days=1)  # �� ���� ���� ������ �Ϸ�Ǹ� timedelta Ȱ���Ͽ� ���� ��¥�� �̵�
except:

    paths = [r"C:\Users\user1\Desktop\Battery_Charging_Algorithm\API.py",r"C:\Users\user1\Desktop\Battery_Charging_Algorithm\API_2.py",r"C:\Users\user1\Desktop\Battery_Charging_Algorithm\get_battery_charge_DB.py" ]

    while start_date <= end_date: #���糯¥�� ���ᳯ¥�� ������ ������
          for path in paths:# ������ py���ϵ鿡 ���ؼ�
                # execute_py(file, current_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"), float(latitude_input), float(longitude_input),  first_api_input.replace(" ", "").replace(".", ""),second_api_input.replace(" ", "").replace(".", "") )  # execute�Լ� �����Ͽ� �� py���Ͽ� ���Ͽ� ���� �� ���̽� ��ũ��Ʈ ����. ���ڿ� ���·� ��ȯ�Ͽ� ����
                execute_py(path, start_date, end_date, latitude_input, longitude_input,  first_api_input,second_api_input )
                start_date += datetime.timedelta(days=1)  # �� ���� ���� ������ �Ϸ�Ǹ� timedelta Ȱ���Ͽ� ���� ��¥�� �̵�

 
print(sys.argv)

#schedule.every().day.at("21:10").do(scheduled_job)

#while True:
#    # ���� ��ΰ� ��ȿ���� ������ ���� �ߴ�
#    current_datetime = datetime.datetime.now() 
#    print(f"�����۾��������� üũ ��..{current_datetime}")

#    schedule.run_pending()
#    time.sleep(1) # 1�ʸ��� �۾����������� �����Ǿ����� �˻�         