# app2.py
from flask import Flask, render_template, redirect, request, session, url_for
from werkzeug.utils import secure_filename
import cv2
import face_recognition
import os
import pyrebase
from firebase_admin import initialize_app, storage, db as firebase_db
import logging

import pickle

import cvzone
import numpy as np
import firebase_admin
from firebase_admin import credentials
from datetime import date
from datetime import datetime

app = Flask(__name__)

firebaseConfig = {
    "apiKey": "AIzaSyCfz9cWzB-q2sVxZQvxg2AdSmS-onQUm9I",
    "authDomain": "faces-38f82.firebaseapp.com",
    "databaseURL": "https://faces-38f82-default-rtdb.firebaseio.com",
    "projectId": "faces-38f82",
    "storageBucket": "faces-38f82.appspot.com",
    "messagingSenderId": "561665683184",
    "appId": "1:561665683184:web:62e1ea55549aef5bdcdc35",
    "measurementId": "G-PHWLRQ9GZN"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
firebase_storage = firebase.storage()
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)  # Generate a secure secret key
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_storage(file, filename):
    blob = firebase_storage.bucket().blob(filename)
    blob.upload_from_file(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def page1():
    return render_template('index.html')

@app.route('/login2', methods=['GET', 'POST'])
def page2():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     person_name = request.form.get('person_name')

    #     # Check if any of the required fields is missing
    #     if not email or not password or not person_name:
    #         return render_template('login2.html', error='All fields are required. Please try again.')

    #     users_ref = firebase_db.reference('myform')
    #     users = users_ref.get()

    #     if users:
    #         for user_key, user_data in users.items():
    #             if user_data.get('email') == email and user_data.get('password') == password:
    #                 session['user_id'] = user_key
    #                 register_faces(person_name)
    #                 return redirect(url_for('result'))

    #         # If the loop completes without a match, show an error message
    #         return render_template('login2.html', error='Invalid credentials. Please try again.')

    #     return redirect(url_for('index'))

    # return render_template('login2.html')
    
        error = None
        if request.method == 'POST':
            
            email = request.form.get('email')
            password = request.form.get('password')
            person_name = request.form.get('person_name')

            # Perform Firebase authentication (replace with your actual authentication code)
            # Example: authenticate the user using Firebase Auth
            # auth_result = authenticate_with_firebase(email, password)

            # Assuming auth_result is a dictionary containing user information
            
            auth_result = {'uid': 'user_uid'}

            if auth_result:
                session['user_id'] = auth_result['uid']

                # Update last login time in the database
                # update_last_login(auth_result['uid'])
                register_faces(person_name)
                return redirect(url_for('result'))
            error = 'Invalid credentials. Please try again.'

            # Handle authentication failure
            return render_template('login2.html', error='Invalid credentials. Please try again.')
            
        return render_template('login2.html',error=error)


@app.route('/register', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        # Extract user data from the registration form
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']  # Fix the typo here
        person_name = request.form['person_name']

        # Create a new user in Firebase Authentication
        try:
            user = auth.create_user_with_email_and_password(email, password)
        except Exception as e:
            # Handle registration error
            return render_template('register.html', error=str(e))

        # Handle file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Save the file to Firebase Storage
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'rb') as image_file:
                firebase_storage.child("images/" + filename).put(image_file)

            # Get the download URL of the uploaded image
            image_url = firebase_storage.child("images/" + filename).get_url(None)

        # Save the form data and image URL to the Firebase Realtime Database
        form_data = {
            "name": request.form.get('name', ''),
            "person_name": request.form.get('person_name', ''),
            "password": password,  # Use the corrected variable here
            "date": request.form.get('date', ''),
            "gender": request.form.get('gender', ''),
            "email": request.form.get('email', ''),
            "address": request.form.get('address', ''),
            "image_url": image_url if 'image_url' in locals() else ''  # Handle when image_url is not available
        }

        save_to_firebase(form_data)

        return redirect('/login2')
    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/final')
def page5():
    return render_template('final.html')

@app.route('/result')
def result():
    user_id = session.get('user_id')
    if user_id:
        return render_template('result.html')
    else:
        return redirect(url_for('index'))

def register_faces(person_name):
    

    # Your face registration logic (similar to the provided code)
    # ...
    # Your face registration logic (similar to the provided code)
    # ...
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faces-38f82-default-rtdb.firebaseio.com/",
            'storageBucket': "faces-38f82.appspot.com"
        })
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    # cred = credentials.Certificate("serviceAccountKey.json")
    # firebase_admin.initialize_app(cred, {
    #     # 'databaseURL': "https://facerecognition-8520d-default-rtdb.firebaseio.com/",
    #     'databaseURL': "https://faces-38f82-default-rtdb.firebaseio.com/",
        
    #     # 'storageBucket': "facerecognition-8520d.appspot.com"
    #     'storageBucket': "faces-38f82.appspot.com"

    # })

    bucket = storage.bucket()
    # calling webcam
    video=cv2.VideoCapture(0)

    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(3))
    height = int(video.get(4))
    output = cv2.VideoWriter(".mp4",
                cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                fps=fps*7, frameSize=(width, height))

    # adjusting the detection box dimensions
    video.set(3,640)
    video.set(4,480)

    # take bg image
    imgBackground=cv2.imread('Resources/background.png')

    # to get images of output display
    foldermodepath = 'Resources/Modes'
    modepathlist = os.listdir(foldermodepath)
    imgmodelist = []
        
    # adding images to our list
    for path in modepathlist:
        # adding path to our image
        imgmodelist.append(cv2.imread(os.path.join(foldermodepath,path)))
        
    # load the encode file
    file = open('Encodes.p','rb')
    knownEncodeListWIthIDs = pickle.load(file)   
    file.close()

    # extracting the file
    knownEncodeList,customerIDs = knownEncodeListWIthIDs

    modetype = 0
    ans=0
    counter = 0
    id = -1
    imgCustomer = []

    while True:
        # read the video
        success,img=video.read()
        if not success or img is None:
            print("Error: Failed to read the frame from the video source.")
            # You may want to handle this error appropriately, e.g., break out of the loop or return an error message.
            break
        img = cv2.resize(img, (width, height))
        output.write(img)
            
        # to resize required image
        imgSmall = cv2.resize(img ,(0,0),None,0.25,0.25)
        
        # to maintain the defualt color
        imgSmall = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
        # locate the face
        faceInCurrentFrame = face_recognition.face_locations(imgSmall)
        # prepare encoodes of current face
        encodesOfCurrentFace = face_recognition.face_encodings(imgSmall,faceInCurrentFrame)

        # display webcam in img background []holds the dimensions
        imgBackground[162:162+480,55:55+640]=img
        
        # display images in output display
        imgBackground[44:44+633,808:808+414]=imgmodelist[modetype]
        
        if faceInCurrentFrame:
            for encodeFaces , faceLoc in zip(encodesOfCurrentFace,faceInCurrentFrame):
                # compares images and gives true false
                match =face_recognition.compare_faces(knownEncodeList,encodeFaces)
            
                # find face distance the lower the face distance the better the accuracy
                faceDistance = face_recognition.face_distance(knownEncodeList,encodeFaces) 
            
                # this wil, give the index of image whose img got matched with highest accuracy
                matchIndex = np.argmin(faceDistance) 
            
                # to put a box if face is detected
                if match[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    boundingbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, boundingbox, rt=0)
                    id = customerIDs[matchIndex]
                
                    if counter==0:
                    
                        # once detection is done show active and make the counter 1
                        counter=1
                        modetype=1                
                    
            if counter!=0:
                # if counter is 1 it means we have to load the data from the database and show it 
                if counter==1:
                    # get the data from database
                    customerInfo = db.child('myForm').child(id).get()
                
                    # get the image from database
                    blob = bucket.get_blob(f'images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(),np.uint8)
                    imgCustomer = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                
                    # checking the time elapsed
                    # datetimeObject = datetime.strptime(customerInfo['last_login_dnt'],
                    #                                 "%Y-%m-%d %H:%M:%S")
                    # datetimeObject = datetime.strptime(customerInfo['last_login_dnt'], "%Y-%m-%d %H:%M:%S")
                    if customerInfo is not None:
                        customerInfo = customerInfo.val()  # Get the dictionary from PyreResponse

                        # Now, you can safely access the 'last_login_dnt' key
                        if 'last_login_dnt' in customerInfo:
                            datetimeObject = datetime.strptime(customerInfo['last_login_dnt'], "%Y-%m-%d %H:%M:%S")
                        else:
                            # Handle the case when 'last_login_dnt' is not present in the data
                            print("'last_login_dnt' not found in customerInfo")
                    else:
                        # Handle the case when customerInfo is None
                        print("No data found for the specified ID")

                
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                
                    if secondsElapsed>60:
                        # update the database
                        ref = db.child('myForm').child(id)

                        ref.child('last_login_dnt').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        ref.child('last_login_time').set(current_time)
                        ref.child('last_login_date').set(current_date)
                
                    else:
                        modetype=3
                        counter = 0
                        imgBackground[44:44+633,808:808+414]=imgmodelist[modetype]
                        break
                        
                if modetype!=3:
                    if 10<counter<30:
                        modetype = 2
                        ans = 1
                        
                    imgBackground[44:44+633,808:808+414]=imgmodelist[modetype]
                    if counter<=10 :
                        # to align the name according to the length
                        (w, h), _ = cv2.getTextSize(customerInfo['customer_name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w)//2
            
                        cv2.putText(imgBackground, str(customerInfo['customer_name']), (890+offset, 363),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
                                
                        cv2.putText(imgBackground, str(customerInfo['customerid']), (1022, 413),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        
                        cv2.putText(imgBackground, str(customerInfo['last_login_time']), (1053, 465),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        
                        cv2.putText(imgBackground, str(customerInfo['last_login_date']), (1036, 517),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        
                        imgBackground[93:93+216,904:904+216] = imgCustomer
                    
                    counter+=1
            
                    if counter >= 30:
                        counter = 0
                        modeType = 0
                        customerInfo = []
                        imgCustomer = []
                        imgBackground[44:44+633,808:808+414]=imgmodelist[modetype]
        
        else:
            modeType = 0
            counter = 0
            
        # show webcame img
        # cv2.imshow("Webcam",img)

        # show img bg
        cv2.imshow("Facial Authentication",imgBackground)

        cv2.waitKey(1)    



    
def save_to_firebase(form_data):
    
    db.child("myForm").push(form_data)


if __name__ == '__main__':
    app.run(debug=True)
