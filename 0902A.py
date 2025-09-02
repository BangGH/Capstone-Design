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

        # 's' → 웹캠 켜기
        if key == ord('s'):
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
