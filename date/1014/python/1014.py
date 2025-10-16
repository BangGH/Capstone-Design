import firebase_admin
from firebase_admin import credentials, db
import cv2
from pyzbar.pyzbar import decode as decode_qr
from pyzbar.pyzbar import decode, ZBarSymbol
from pylibdmtx.pylibdmtx import decode as decode_dm
import serial
import threading
import time
import struct

# Firebase RTDB 초기화
cred = credentials.Certificate('testkey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-c7ea9-default-rtdb.firebaseio.com/' 
})

# RTDB 데이터 가져오기
fill_A_ref = db.reference('fill_A')
fill_B_ref = db.reference('fill_B')
fill_C_ref = db.reference('fill_C')

# RTDB 데이터 업데이트
a_val = fill_A_ref.get()
b_val = fill_B_ref.get()
c_val = fill_C_ref.get()
print(a_val, b_val, c_val)

def update_count(item, increment):
    ref = db.reference(item)
    current = ref.get() or 0
    ref.set(current + increment)
    print(f"Updated {item}: {current} -> {current + increment}")

# 알약 인식 시 올라가는 값
def update_a():
    increment_value = 10  # A는 +10
    update_count('fill_A', increment_value)

def update_b():
    increment_value = 15  # B는 +15
    update_count('fill_B', increment_value)

def update_c():
    increment_value = 20  # C는 +20
    update_count('fill_C', increment_value)

# 시리얼 설정
py_serial = serial.Serial(
    port='COM10',
    baudrate=115200,
)

cam_start  = True
cam_status = False
cam_stop   = False

# 시리얼 확인
def serial_listener():
    global cam_start
    while True:
        if py_serial.readable():
            data = py_serial.readline().decode().strip()
            if data:
                print("받은 데이터:", data)
                '''
                if data == 'G':
                    print("cam on")
                    cam_start=True
                '''


# 수신 스레드 시작
thread = threading.Thread(target=serial_listener, daemon=True)
thread.start()

# 실시간 재고 stm에게 전송
print(a_val, b_val, c_val)
py_serial.write(b'$')
time.sleep(0.1)
py_serial.write(b'a')
time.sleep(0.1)
py_serial.write(str(a_val).encode())
time.sleep(0.1)
py_serial.write(b'b')
time.sleep(0.1)
py_serial.write(str(b_val).encode())
time.sleep(0.1)
py_serial.write(b'c')
time.sleep(0.1)
py_serial.write(str(c_val).encode())
time.sleep(0.1)
py_serial.write(b'y')
py_serial.write(b'\r\n')
time.sleep(0.2)


# ESP32-CAM 스트림
url = "http://192.168.0.3:81/stream"

qr_results = []
dm_results = []
frame_original = None

def handle_specific_code(code):
    update_a() #A알약 값 증가

    # QR / DataMatrix 처리
def decode_qr_thread():
    global qr_results, frame_original
    while True:
        if frame_original is not None:
            qr_results = decode(frame_original, symbols=[ZBarSymbol.QRCODE])

def decode_dm_thread():
    global dm_results, frame_original
    while True:
        if frame_original is not None:
           dm_results = decode_dm(frame_original)

qr_thread = threading.Thread(target=decode_qr_thread, daemon=True)
dm_thread = threading.Thread(target=decode_dm_thread, daemon=True)
qr_thread.start()
dm_thread.start()

# 루프
frame_skip = 10
frame_count = 0

while True:
    if cam_start == True:
        cap = cv2.VideoCapture(url)
        cam_status = True
        cam_stop=False

        while cam_status:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame_original = frame
            frame_count += 1

            if frame_count % frame_skip == 0:
                # QR 코드 처리
                for obj in qr_results:
                    data = obj.data.decode('utf-8')
                    print(f"QR Code: {data}")
                    if data.startswith("A=3,B=2,C=1"):
                        update_count('fill_A', -3)
                        update_count('fill_B', -2)
                        update_count('fill_C', -1)
                        py_serial.write(b'!')
                        time.sleep(0.05)
                        py_serial.write(b'a3')
                        time.sleep(0.05)
                        py_serial.write(b'b2')
                        time.sleep(0.05)
                        py_serial.write(b'c1')
                        time.sleep(0.05)
                        py_serial.write(b'\r\n')
                        time.sleep(3)
                        cam_stop=True
                    if data.startswith("A=3,B=0,C=2"):
                        update_count('fill_A', -3)
                        update_count('fill_B', 0)
                        update_count('fill_C', -2)
                        py_serial.write(b'!')
                        time.sleep(0.05)
                        py_serial.write(b'a3')
                        time.sleep(0.05)
                        py_serial.write(b'b0')
                        time.sleep(0.05)
                        py_serial.write(b'c2')
                        time.sleep(0.05)
                        py_serial.write(b'\r\n')
                        time.sleep(3)
                        cam_stop=True
                    if data.startswith("A=0,B=1,C=3"):
                        update_count('fill_A', 0)
                        update_count('fill_B', -1)
                        update_count('fill_C', -3)
                        py_serial.write(b'#')
                        time.sleep(0.05)
                        py_serial.write(b'M111L111D111')
                        time.sleep(0.05)
                        py_serial.write(b'\r\n')
                        time.sleep(3)
                        cam_stop=True

            # DataMatrix 처리
            for obj in dm_results:
                data = obj.data.decode('utf-8')
                print(f"Data Matrix: {data}")
                if data.startswith("88"):
                    update_a()
                    py_serial.write(b'@')
                    time.sleep(0.05)
                    py_serial.write(b'a3')
                    time.sleep(0.05)
                    py_serial.write(b'\r\n')
                    time.sleep(3)
                    cam_stop=True

            cv2.imshow('ESP32-CAM Stream', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Q눌러 종료")
                    cap.release()
                    cv2.destroyAllWindows()
                    cam_status=False
                    cam_start=False
                    break
        
            if cam_stop == True:
                    print("종료")
                    cap.release()
                    cv2.destroyAllWindows()
                    cam_status=False
                    cam_start=False
                    break
    time.sleep(1)