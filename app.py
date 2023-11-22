from flask import Flask, render_template, request, redirect, url_for, flash
import cv2
import numpy as np
from dotenv import load_dotenv
import cloudinary
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
import os

import mongo_utils, model_utils

load_dotenv()

app = Flask('__name__')
app.secret_key = 'verysecret'

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'), 
    api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET')
)

@app.route('/')
def index():
    students_list = list(mongo_utils.students_collection.find({}, {'_id': 0, 'embedding': 0}))
    print(students_list)
    return render_template('index.html', students_list=students_list)

@app.route('/add-student', methods = ['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('student_form.html', student = None)
    else:
        name = request.form['name']
        student_id = request.form['student_id']
        branch = request.form['branch']
        photo = request.files['photo']

        if photo.filename == '':
            flash('Error: Empty file', 'error')
            return 'Error: Empty file'
        try:
            upload_result = upload(photo)
            photo_url = upload_result['secure_url']

            photo.seek(0)  
            img = cv2.imdecode(np.frombuffer(photo.read(), np.uint8), cv2.IMREAD_COLOR)
            embedding = model_utils.getEmbedding(img)

            mongo_utils.students_collection.insert_one({
                'name': name,
                'studentId': student_id,
                'branch': branch,
                'embedding': embedding,
                'photoUrl': photo_url}
            )
            flash('Added new student', 'success')
            return redirect(url_for('index'))

        except CloudinaryError as e:
            flash('Could not add new student', 'error')
            return f'Error: {str(e)}'

@app.route('/edit-student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = mongo_utils.getStudentDetails(student_id=student_id)
    
    if request.method == 'GET':
        return render_template('student_form.html', student = student)
    else:
        name = request.form['name']
        student_id = request.form['student_id']
        branch = request.form['branch']
        photo = request.files['photo']

        if photo.filename == '':
            return 'Error: Empty file'
        try:
            upload_result = upload(photo)
            photo_url = upload_result['url']

            photo.seek(0)  
            img = cv2.imdecode(np.frombuffer(photo.read(), np.uint8), cv2.IMREAD_COLOR)
            embedding = model_utils.getEmbedding(img)

            mongo_utils.students_collection.update_one(
                {'studentId': student_id}, 
                {
                    '$set': {
                        'name': name,
                        'studentId': student_id,
                        'branch': branch,
                        'embedding': embedding,
                        'photoUrl': photo_url
                    }
                }
            )
            flash('Updated student details', 'success')
            return redirect(url_for('index'))

        except CloudinaryError as e:
            flash('Could not update student details', 'error')
            return f'Error: {str(e)}'


@app.route('/delete-student/<student_id>')
def delete_student(student_id):
    mongo_utils.deleteStudent(student_id=student_id)
    flash('Removed student', 'success')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)