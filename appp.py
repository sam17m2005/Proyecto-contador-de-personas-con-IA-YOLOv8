from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

app = Flask(__name__)

# Cargar modelo YOLO
model = YOLO("entrenamiento_colab (1)\\content\\entrenamiento_colab\\modelo_personas\\weights\\best.pt")

# Trackers
tracker1 = DeepSort(max_age=20)
tracker2 = DeepSort(max_age=20)

# Cámaras
cap1 = cv2.VideoCapture(0)  # Cámara del PC
cap2 = cv2.VideoCapture(1)  # Cámara IP / Celular

CONFIDENCE_THRESHOLD = 0.5

people_count = {
    'camera1': 0,
    'camera2': 0
}

def generate_frames(cap, tracker, camera_name):
    global people_count
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            if cls == 0 and conf > CONFIDENCE_THRESHOLD:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

        tracks = tracker.update_tracks(detections, frame=frame)
        for track in tracks:
            if not track.is_confirmed():
                continue
            x1, y1, x2, y2 = map(int, track.to_ltrb())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {track.track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        num_people = sum(1 for t in tracks if t.is_confirmed())
        
        # NUEVO: Actualizar contador global
        people_count[camera_name] = num_people
        
        cv2.putText(frame, f"Personas: {num_people}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camaras')
def camaras():
    return render_template('camaras.html')

@app.route('/video_pc')
def video_pc():
    return Response(generate_frames(cap1, tracker1, 'camera1'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_movil')
def video_movil():
    return Response(generate_frames(cap2, tracker2, 'camera2'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/people_count')
def get_people_count():
    return jsonify(people_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
