import cv2


def scan_qr_code():
    cap = cv2.VideoCapture(0)

    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()

        data, bbox, _ = detector.detectAndDecode(img)

        if data:
            a = data
            break

        cv2.imshow("QRCODEscanner", img)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    pairs = [item.strip() for item in a.split(',')]

    qr_dict = {}

    for pair in pairs:
        if ":" in pair:
            key, value = pair.split(':', 1)
            qr_dict[key.strip()] = value.strip()

    return qr_dict
