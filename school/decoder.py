import cv2
from pyzbar.pyzbar import decode as decode_qr
from pylibdmtx.pylibdmtx import decode as decode_dm
import threading

# ESP32-CAM 스트림 URL
url = "http://192.168.0.3:81/stream"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

# 디코딩 스레드용 변수
qr_results = []
dm_results = []
frame_original = None

# QR 디코딩 스레드 함수
def decode_qr_thread():
    global qr_results, frame_original
    while True:
        if frame_original is not None:
            qr_results = decode_qr(frame_original)

# 데이터 매트릭스 디코딩 스레드 함수
def decode_dm_thread():
    global dm_results, frame_original
    while True:
        if frame_original is not None:
            dm_results = decode_dm(frame_original)

# 스레드 시작
qr_thread = threading.Thread(target=decode_qr_thread, daemon=True)
dm_thread = threading.Thread(target=decode_dm_thread, daemon=True)
qr_thread.start()
dm_thread.start()

frame_skip = 10  # 프레임 스킵 간격
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # 프레임 원본 유지
    frame_original = frame

    frame_count += 1
    if frame_count % frame_skip == 0:
        # QR 코드 결과 출력
        for obj in qr_results:
            print(f"QR Code: {obj.data.decode('utf-8')}")

        # 데이터 매트릭스 결과 출력
        for obj in dm_results:
            print(f"Data Matrix: {obj.data.decode('utf-8')}")

    # 화면에 표시
    cv2.imshow('ESP32-CAM Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
