# pip install flask ultralytics opencv-python deep-sort-realtime

from flask import Flask, Response
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

app = Flask(__name__)

# Carga modelo YOLOv8
model = YOLO("modelos_yolo\\entrenamiento_colab\\modelo_personas2\\weights\\best.pt")

# Inicializa DeepSORT con menor tolerancia
tracker = DeepSort(max_age=20)

# Fuente de video (0 = cámara del PC)
cap = cv2.VideoCapture(0)

def generate_frames():
    CONFIDENCE_THRESHOLD = 0.5  # Umbral de detección

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detección con YOLOv8
        results = model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # Solo clase "persona" 
            if cls == 0 and conf > CONFIDENCE_THRESHOLD:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

        # Seguimiento con DeepSORT
        tracks = tracker.update_tracks(detections, frame=frame)

        # Contador de personas visibles (tracks confirmados)
        active_tracks = []

        for track in tracks:
            if not track.is_confirmed():
                continue
            active_tracks.append(track)
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track.track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Mostrar cantidad de personas visibles
        num_people = len(active_tracks)
        cv2.putText(frame, f"Personas: {num_people}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Stream MJPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Seguimiento en Vivo</title></head>
    <body style="text-align:center;">
        <h1>Detección y Seguimiento en Vivo</h1>
        <img src="/video" width="70%" />
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
