import serial
import cv2

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # 현재 상태: False → 빈 화면
    show_camera = False

    while True:
        if show_camera:
            # 웹캠 프레임 읽기
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            cv2.imshow("Webcam Window", frame)
        else:
            # 빈 화면 (검은 배경)
            blank = 255 * (0 * np.ones((480, 640, 3), dtype=np.uint8))
            cv2.imshow("Webcam Window", blank)

        key = cv2.waitKey(1) & 0xFF

        if py_serial.readable():
        
        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
            response = py_serial.readline()
        
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            print(response[:len(response)-1].decode())

        # 's' → 웹캠 켜기
        if response == ord('CodeA'):
            show_camera = True

        # 'e' → 웹캠 끄고 빈 화면
        elif key == ord('e'):
            show_camera = False

        # 'q' → 프로그램 종료
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import numpy as np
    main()


py_serial = serial.Serial(
    
    # Window
    port='COM8',
    
    # 보드 레이트 (통신 속도)
    baudrate=115200,
)