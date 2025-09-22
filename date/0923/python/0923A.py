import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('testkey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-c7ea9-default-rtdb.firebaseio.com/' 
})


ref = db.reference('fill_A')
A=(ref.get())
ref = db.reference('fill_B')
B=(ref.get())
ref = db.reference('fill_C')
C=(ref.get())

A=A+10
B=B-2
C=C+7

ref = db.reference()
ref.update({'fill_A' : A})
ref.update({'fill_B' : B})
ref.update({'fill_C' : C})

py_serial = serial.Serial(
    port='COM5',
    baudrate=115200,
)

print("sirial on")

while True:
    user_input = input("문자 입력 (A/B): ")  # 키보드 입력
    if user_input in ['A', 'B']:
        py_serial.write(user_input.encode())  # STM32로 전송
        print(f"전송: {user_input}")
    else:
        print("A 또는 B만 입력하세요.")