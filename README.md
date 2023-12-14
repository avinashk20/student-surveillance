# Student Surveillance

## Overview
The Student Surveillance project is an automated surveillance system that utilizes advanced technologies to monitor and identify students using a video stream from a camera. The system employs facial recognition to match individuals against a database of students. Upon identification, relevant parties are notified via a Telegram alert, providing details of the recognized students along with the timestamp.

### Screenshots
![Dashboard](/screenshots/dashboard.jpg)
![Student Form](/screenshots/student_form.jpg)
![telegram_alert](/screenshots/alert.jpeg)

## Technologies Used

- **DeepFace Library:** Used for facial recognition.
- **Dlib:** Utilized for face detection.
- **Facenet:** Employed to obtain facial embeddings for recognition.
- **MongoDB:** Storage of student details.
- **Flask:** Web framework for creating the user interface.
- **HTML and CSS:** Used to design and style the web interface.
- **Multithreading:** Implemented for efficient real-time detection.

## Features

- Real-time facial recognition using a video stream.
- Telegram alerts for identified students with timestamp details.
- Database storage for student records.
- Web interface for managing student details.
- Multithreading for efficient real-time detection.

## Getting Started

### Prerequisites

- Ensure you have Python installed.
- Install required libraries using `requirements.txt`.

### Installation

1. Clone the repository: `git clone https://github.com/your-username/student-surveillance.git`
2. Navigate to the project directory: `cd student-surveillance`
3. Install dependencies: `pip install -r requirements.txt`

### Configuration
Set up your environment variables by following these steps:
1. Create a copy of the `.example.env` file and name it `.env`.
2. Open the newly created `.env` file and replace the placeholder values with your own.

### Usage
0. To start surveillance: `python main.py`
1. To start the web interface: `python app.py`
2. Access the web interface at `http://localhost:5000` to manage student records.


