import serial
import time

py_serial = serial.Serial(
    
    # Window
    port='COM7',
    
    # 보드 레이트 (통신 속도)
    baudrate=115200,
)

while True:
      
    commend = input('아두이노에게 내릴 명령:')
    
    py_serial.write(commend.encode())
    
    time.sleep(0.1)