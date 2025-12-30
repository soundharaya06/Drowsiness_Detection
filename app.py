from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import time
import sqlite3
import mediapipe as mp
import numpy as np
import pygame
from datetime import datetime
import os

# ================= APP SETUP =================
app = Flask(__name__)

def ensure_tables():
    conn = sqlite3.connect("databases/system.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        role TEXT
    )
    """)
    conn.commit()
    conn.close()

    

os.makedirs("databases", exist_ok=True)

# ================= ALARM =================
pygame.mixer.init()
pygame.mixer.music.load("static/alarm.wav")

# ================= MEDIAPIPE MODEL =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# ================= PARAMETERS =================
EAR_THRESHOLD = 0.25
DROWSY_TIME = 3  # seconds (fast detection)

start_time = None
alarm_on = False
CURRENT_EMPLOYEE_ID = None

# ================= CAMERA =================
camera = None
camera_active = False

# ================= HELPER FUNCTIONS =================
def calculate_ear(eye):
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

def get_employees():
    conn = sqlite3.connect("databases/system.db")
    c = conn.cursor()
    c.execute("SELECT employee_id, name FROM employees")
    data = c.fetchall()
    conn.close()
    return data

def log_drowsiness(emp_id, eye_status, drowsy):
    if emp_id is None:
        return
    conn = sqlite3.connect("databases/system.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs VALUES (NULL, ?, ?, ?, ?)",
        (emp_id, eye_status, drowsy, datetime.now())
    )
    conn.commit()
    conn.close()

# ================= VIDEO STREAM =================
def generate_frames():
    global camera, camera_active, start_time, alarm_on

    camera = cv2.VideoCapture(0)
    camera_active = True

    while camera_active:
        success, frame = camera.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        eye_status = "OPEN"
        drowsy_status = "NO"

        if results.multi_face_landmarks:
            h, w, _ = frame.shape
            lm = results.multi_face_landmarks[0].landmark

            left_eye = [(int(lm[i].x * w), int(lm[i].y * h)) for i in LEFT_EYE]
            right_eye = [(int(lm[i].x * w), int(lm[i].y * h)) for i in RIGHT_EYE]

            ear = (calculate_ear(left_eye) + calculate_ear(right_eye)) / 2

            if ear < EAR_THRESHOLD:
                eye_status = "CLOSED"
                if start_time is None:
                    start_time = time.time()
                elif time.time() - start_time >= DROWSY_TIME:
                    drowsy_status = "YES"
                    if not alarm_on:
                        pygame.mixer.music.play(-1)
                        alarm_on = True
                        log_drowsiness(CURRENT_EMPLOYEE_ID, eye_status, drowsy_status)
            else:
                start_time = None
                if alarm_on:
                    pygame.mixer.music.stop()
                alarm_on = False

        cv2.putText(frame, f"Eye Status: {eye_status}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 105, 180), 2)
        cv2.putText(frame, f"Drowsy: {drowsy_status}", (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (138, 43, 226), 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    # 🔴 CLEANUP WHEN USER LEAVES DASHBOARD
    camera.release()
    camera = None

# ================= ROUTES =================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    employees = get_employees()
    return render_template("dashboard.html", employees=employees)

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/start_camera", methods=["POST"])
def start_camera():
    global camera, camera_active
    if not camera_active:
        camera = cv2.VideoCapture(0)
        camera_active = True
    return ("", 204)


@app.route("/stop_camera", methods=["POST"])
def stop_camera():
    global camera, camera_active
    camera_active = False
    if camera:
        camera.release()
        camera = None
    return ("", 204)



@app.route("/employee")
def employee():
    return render_template("employee.html")

@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form["name"]
    department = request.form["department"]
    role = request.form["role"]

    conn = sqlite3.connect("databases/system.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO employees (name, department, role) VALUES (?, ?, ?)",
        (name, department, role)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/select_employee", methods=["POST"])
def select_employee():
    global CURRENT_EMPLOYEE_ID
    CURRENT_EMPLOYEE_ID = request.form["employee_id"]
    return redirect(url_for("dashboard"))

@app.route("/logs")
def logs():
    conn = sqlite3.connect("databases/system.db")
    c = conn.cursor()

    c.execute("""
        SELECT logs.log_id,
               COALESCE(employees.name, 'Unknown'),
               logs.eye_status,
               logs.drowsy,
               logs.timestamp
        FROM logs
        LEFT JOIN employees
        ON logs.employee_id = employees.employee_id
        ORDER BY logs.timestamp DESC
    """)

    data = c.fetchall()
    conn.close()
    return render_template("logs.html", logs=data)

# ================= MAIN =================
if __name__ == "__main__":
    app.run(debug=True)
