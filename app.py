import cv2
camera = cv2.VideoCapture(0)
while True:
    sucess, frame = camera.read()
    if not sucess:
        print("Couldn't Acess Camera")
        break
    cv2.imshow("RealityFrame AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

