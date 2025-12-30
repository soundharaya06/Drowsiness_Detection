🚗 Driver Drowsiness Detection System using AI & Computer Vision
An AI-powered real-time drowsiness monitoring system that detects prolonged eye closure using a webcam and alerts the user to prevent accidents. The system also supports employee management and logging of drowsiness events through a web-based dashboard.

📌 Table of Contents
1.	Overview
2.	Features
3.	Technologies Used
4.	System Architecture
5.	How It Works
6.	Project Structure
7.	Installation & Setup
8.	Usage Instructions
9.	Database Schema

📝 Overview
Driver drowsiness is one of the major causes of road accidents. This project presents a real-time driver drowsiness detection system that uses computer vision and AI to monitor eye activity. When the driver’s eyes remain closed beyond a defined threshold, an alarm is triggered to alert the driver.
The system is implemented as a Flask-based web application with a modern UI and includes features such as employee management and drowsiness event logging.

✨ Features
🎥 Real-time webcam-based monitoring
👁 Eye status detection (Open / Closed)
⏱ Fast drowsiness detection (within 1 second)
🔔 Audio alarm on drowsiness detection
👤 Employee registration and selection
📊 Drowsiness logs with timestamps
🖥 Web-based dashboard with sidebar navigation
🎨 Clean pink–lavender themed UI
🧰 Technologies Used
Frontend
1.	HTML5
2.	CSS3
3.	JavaScript
Backend
1.	Python
2.	Flask
Computer Vision & AI
1.	OpenCV
2.	MediaPipe Face Mesh (Pre-trained ML model)
3.	NumPy
Database
1.	SQLite
Audio
1.	Pygame (alarm sound)


🏗 System Architecture
Webcam → MediaPipe Face Mesh → Eye Landmark Detection
        ↓
Eye Aspect Ratio (EAR) Calculation
        ↓
Time-based Drowsiness Logic
        ↓
Alarm Trigger + Log Entry
        ↓
Flask Web Dashboard

🔍 How It Works
•	The webcam captures live video frames.
•	MediaPipe Face Mesh detects facial landmarks (468 points).
•	Eye landmarks are extracted.
•	Eye Aspect Ratio (EAR) is calculated.
•	If EAR remains below a threshold for a fixed time:
•	Drowsiness is detected
•	Alarm is triggered
•	Event is logged in the database
•	Logs can be viewed via the web dashboard.

📁 Project Structure
Drowsiness_Website/
│
├── app.py
├── database_setup.py
│
├── databases/
│   └── system.db
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── employee.html
│   └── logs.html
│
├── static/
│   ├── alarm.wav
│   └── css/
│       └── style.css
│
└── README.md

⚙ Installation & Setup
Install Required Packages
pip install flask opencv-python mediapipe numpy pygame

Create Database Tables
python database.py

🔍 How It Works
•	The webcam captures live video frames.
•	MediaPipe Face Mesh detects facial landmarks (468 points).
•	Eye landmarks are extracted.
•	Eye Aspect Ratio (EAR) is calculated.
•	If EAR remains below a threshold for a fixed time:
•	Drowsiness is detected
•	Alarm is triggered
•	Event is logged in the database
•	Logs can be viewed via the web dashboard.

🤖 Why MediaPipe?
•	Uses pre-trained deep learning models
•	No dataset or training required
•	Extremely fast and lightweight
•	Suitable for real-time applications
•	Developed by Google
•	MediaPipe Face Mesh internally uses CNN-based models trained on large-scale facial datasets.

🚀 Future Enhancements
•	Yawning detection
•	Head pose estimation
•	Night-time / low-light detection
•	Drowsiness score analytics
•	User authentication & roles
•	Cloud deployment
•	Mobile app integration

📌 Conclusion
This project demonstrates how AI and computer vision can be effectively used to enhance road safety. By leveraging MediaPipe’s pre-trained models and a clean web interface, the system delivers accurate real-time drowsiness detection without the need for complex model training.

