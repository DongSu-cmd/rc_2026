cap = cv2.VideoCapture(cam, cv2.Cap_GSTREAMER)

if not cap.isOpened():
    print("Not Found camera")

    for _ in range(120):
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.Canny(frame, 100, 200)
        cv2.imshow("soda", img)
    cap.release()