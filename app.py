from flask import Flask, render_template, request
import joblib
import numpy as np
import tensorflow
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# mydb=mysql.connector.connect(host='localhost',user='root',passwd='Munshid_123',database='vertual_doctor')



@app.route('/')
def chat():
    questions = [
        "1-Do you experience itching?",
        "2-Do you have a skin rash?",
        "3-Are there nodal skin eruptions on your body?",
        "4-Do you have continuous sneezing?",
        "5-Are you shivering?",
        "6-Do you have chills?",
        "7-Are you experiencing joint pain?",
        "8-Do you feel stomach pain?",
        "9-Are you dealing with acidity?",
        "10-Do you have ulcers on your tongue?",
        "11-Are you experiencing muscle wasting?",
        "12-Do you vomit frequently?",
        "13-Do you have burning micturition?",
        "14-Do you notice spotting during urination?",
        "15-Are you fatigued?",
        "16-Have you gained weight recently?",
        "17-Do you feel anxious?",
        "18-Do you have cold hands and feet?",
        "19-Are you having mood swings?",
        "20-Are you losing weight?",
        "21-Do you feel restless?",
        "22-Are you experiencing lethargy?",
        "23-Do you have patches in your throat?",
        "24-Do you have irregular sugar levels?",
        "25-Are you coughing?",
        "26-Do you have a high fever?",
        "27-Do you have sunken eyes?",
        "28-Are you breathless?",
        "29-Do you experience excessive sweating?",
        "30-Are you dehydrated?",
        "31-Do you have indigestion?",
        "32-Do you have a headache?",
        "33-Is your skin turning yellowish?",
        "34-Do you have dark urine?",
        "35-Are you feeling nauseous?",
        "36-Have you lost your appetite?",
        "37-Do you have pain behind the eyes?",
        "38-Are you experiencing back pain?",
        "39-Do you suffer from constipation?",
        "40-Are you dealing with abdominal pain?",
        "41-Do you have diarrhea?",
        "42-Have you had a mild fever?",
        "43-Is your urine yellow?",
        "44-Do you have yellowing of the eyes?",
        "45-Have you experienced acute liver failure?",
        "46-Do you have fluid overload?",
        "47-Do you have swelling in your stomach?",
        "48-Do you have swollen lymph nodes?",
        ]

    return render_template('chat.html', questions=questions)



@app.route('/predict', methods=['POST'])
def predict():

    user_name = request.form['user-name']
    user_gender = request.form['gender']
    user_age = int(request.form['user-age'])
    user_phone_nomber = int(request.form['user-phone_number'])
    current_date_formatted = datetime.now().strftime('%Y-%m-%d')

 
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Munshid_123',
        database='vertual_doctor'
    )


    if mydb:
        print("Connected to the database!")
    mycursor = mydb.cursor()


    data = [ (user_name,user_age,user_phone_nomber,current_date_formatted,user_gender) ]

    sql = "INSERT INTO patient_details (name, age, phone_nomber,date,gender) VALUES (%s, %s, %s,%s,%s)"
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "record(s) inserted.")
    mydb.close()



    # Creating a list of user responses to the questions
    user_responses = [int(request.form[f'q{i}']) for i in range(1, 49)]
    print(user_responses)
    model=joblib.load('trained_model')

    final_prediction=model.predict([user_responses])
    pred=np.argmax(final_prediction, axis=1)

    encoder=joblib.load("encoder")
    predicted=encoder.inverse_transform(pred)
    print(f'result is {predicted}')



    return render_template('predict.html',user_responses=user_responses,Name=user_name,Age=user_age,Gender=user_gender,predicted=predicted,user_phone_nomber=user_phone_nomber)


@app.route('/Fungal_infection')
def Fungal_infection():

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Munshid_123',
        database='vertual_doctor'
    )
    mycursor = mydb.cursor()

    sql = "SELECT name FROM patient_details ORDER BY id DESC LIMIT 1"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    if result:
        name= result[0]  # Assuming age is the first (or only) column retrieved
    else:
        name ='man'

    mydb.close()
    
    return render_template('Fungal_infection.html',name=name)


@app.route('/Diabetes')
def Diabetes():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Munshid_123',
        database='vertual_doctor'
    )
    mycursor = mydb.cursor()

    sql = "SELECT gender,name FROM patient_details ORDER BY id DESC LIMIT 1"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    if result:
        gender= result[0]
        name=result[1]  # Assuming age is the first (or only) column retrieved
    else:
        gender="male"
        name='user'

    mydb.close()


    return render_template('Diabetes.html',name=name,gender=gender)


@app.route('/Diabetes_resutl' ,methods=['POST'])
def Diabetes_resutl():
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Munshid_123',
        database='vertual_doctor'
    )
    mycursor = mydb.cursor()

    sql = "SELECT age,name,gender FROM patient_details ORDER BY id DESC LIMIT 1"

    mycursor.execute(sql)

    result = mycursor.fetchone()

    if result:
        Age= result[0]
        name=result[1]
        gender=result[2]  # Assuming age is the first (or only) column retrieved
    else:
        Age =24
        name='user'
        gender='male'

    mydb.close()
    if gender=='male':
        pregnancies= request.form["Pregnancies"]
    else:
        pregnancies=0
        
    Glucose = request.form["Glucose"]
    BloodPressure = request.form["BloodPressure"]
    SkinThickness= request.form["SkinThickness"]
    Insulin = request.form["Insulin"]
    BMI= request.form["BMI"]
    DiabetesPedigreeFunction= request.form["DiabetesPedigreeFunction"]


    input_data = [int(pregnancies), float(Glucose), int(BloodPressure), int(SkinThickness), int(Insulin), float(BMI), float(DiabetesPedigreeFunction), int(Age)]

    model=joblib.load('diabetes_doctor.pkl')

    final_prediction=model.predict([input_data])
    print(final_prediction)
    if final_prediction==[1]:
        result = "Considering the information you've provided, there appears to be a higher likelihood of a diabetes concern"
    else:
        result="Considering the information you've provided, there appears to be a lower likelihood of a diabetes concern"

    return render_template('diabetes_result.html',result=result,name=name)



@app.route('/submit_review', methods=['POST'])
def submit_review():
    user_review = request.form['user-review']
    
    
    return "Thank you for submitting your review!"

if __name__ == '__main__':
    app.run(debug=True)

