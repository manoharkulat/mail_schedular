from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime as dt
import time

app= Flask (__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method=='POST':
        try:
            from_adr=str(request.form['sender_email'])
            to_adr = str(request.form['receiver_email'])
            passw=str(request.form['password'])
            year=int(request.form['year'])
            month=int(request.form['month'])
            date=int(request.form['date'])
            hour=int(request.form['hour'])
            minute=int(request.form['minute'])
            sec=int(request.form['sec'])
            email_body = """<p> 
                You can download images now .
                Go to the page: <a href="https://aidboto.s3.amazonaws.com/bengaluru_images.zip?response-content-disposition=attachment&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXVPB73N56RUUJF46%2F20210927%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20210927T131256Z&X-Amz-Expires=600000&X-Amz-SignedHeaders=host&X-Amz-Signature=570ab921fa62cf0c731e900614aa32babecece728c68339f894b736867dbc0cc">click here</a>
                Thanks,
                AID Team.
                </p>"""
            msg = MIMEText(email_body, 'html')
            try:
                s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                s.login(from_adr, passw)
                send_time = dt.datetime(year, month, date, hour, minute, sec)
                time.sleep(send_time.timestamp() - time.time())
                s.sendmail(from_adr, to_adr, msg.as_string())
                s.quit()
                print('successfully send message')
            except Exception as e:
                print('Error:unable to send email', e)

            print('successfully send eamil')
            return render_template('results.html', Result='you can download images now')
        except Exception as e:
            print('The Exception message is',e)
            return 'Something went wrong'
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)