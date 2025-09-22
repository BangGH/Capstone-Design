import serial

py_serial = serial.Serial(
    port='COM5',
    baudrate=115200,
)

print("sirial on")

while True:
    if py_serial.readable():
        response = py_serial.readline()  # 한 줄 수신
        try:
            print(response.decode().strip())  # 디코딩 + 개행 제거
        except UnicodeDecodeError:
            print(f"수신데이터(디코딩불가): {response}")