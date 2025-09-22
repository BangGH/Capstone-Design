import firebase_admin
from firebase_admin import credentials, firestore
import cv2
from pyzbar.pyzbar import decode as decode_qr
from pylibdmtx.pylibdmtx import decode as decode_dm
import threading

# Firebase 초기화
cred = credentials.Certificate('c:/VSstudio/testkey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestore 데이터 가져오기
def get_counts():
    collection_ref = db.collection('items')
    docs = collection_ref.stream()
    counts = {doc.id: doc.to_dict().get('count', 0) for doc in docs}
    return counts

# Firestore 데이터 업데이트
def update_count(doc_id, increment):
    doc_ref = db.collection('items').document(doc_id)
    doc = doc_ref.get()
    if doc.exists:
        current_count = doc.to_dict().get('count', 0)
        new_count = current_count + increment
        doc_ref.update({'count': new_count})
        print(f"Updated {doc_id}: {current_count} -> {new_count}")
    else:
        print(f"Document {doc_id} does not exist.")

# A, B, C 각각 다른 값을 더하는 함수
def update_a():
    increment_value = 2  # A는 +2
    update_count('A', increment_value)

def update_b():
    increment_value = 3  # B는 +3
    update_count('B', increment_value)

def update_c():
    increment_value = 1  # C는 +1
    update_count('C', increment_value)

# ESP32-CAM 스트림 URL
url = "http://192.168.0.4:81/stream"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

qr_results = []
dm_results = []
frame_original = None

# 특정 값 체크 함수 예시
def handle_specific_code(code):
    update_a()
    # 여기서 원하는 동작 추가 가능

def decode_qr_thread():
    global qr_results, frame_original
    while True:
        if frame_original is not None:
            qr_results = decode_qr(frame_original)

def decode_dm_thread():
    global dm_results, frame_original
    while True:
        if frame_original is not None:
            dm_results = decode_dm(frame_original)

qr_thread = threading.Thread(target=decode_qr_thread, daemon=True)
dm_thread = threading.Thread(target=decode_dm_thread, daemon=True)
qr_thread.start()
dm_thread.start()

frame_skip = 10
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame_original = frame
    frame_count += 1

    if frame_count % frame_skip == 0:
        for obj in qr_results:
            data = obj.data.decode('utf-8')
            print(f"QR Code: {data}")
            if data.startswith("88"):  # 조건 예시: "82"로 시작하면
                handle_specific_code(data)

        for obj in dm_results:
            data = obj.data.decode('utf-8')
            print(f"Data Matrix: {data}")
            if data.startswith("88"):  # 데이터매트릭스도 동일하게
                handle_specific_code(data)

    cv2.imshow('ESP32-CAM Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
