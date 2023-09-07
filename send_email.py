from flask import Flask, request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/chatbot_api/send_email', methods=['POST'])
def send_email():

    load_dotenv()
    
    data = request.form
    firstName = data.get('firstName')
    lastName = data.get('lastName') 
    email = data.get('email')
    userActions = data.get('userActions')
    
    senderEmail = os.getenv('SENDER_EMAIL')
    sendPassword = os.getenv('PASSWORD')
    receiverEmail = 'rajkumars@clouddestinations.com' 

    try:
        # Send email to sales
        hr_msg = MIMEMultipart()
        hr_msg['From'] = senderEmail
        hr_msg['To'] = receiverEmail
        hr_msg['Subject'] = f"Chatbot: New Lead with Interest in Our Services"

        hr_body = f"Dear Sales Team,<br><br>"
        hr_body += f"I wanted to inform you that a potential customer has shown interest in our company's services.<br>"
        hr_body += f"They recently visited our website and explored the following services:<br>"

        hr_body += f"<strong>{userActions}</strong> <br><br>"
        
        hr_body += f"They have expressed a desire to get in touch with us, indicating a potential opportunity for collaboration.<br>"
        hr_body += f"The individual provided their contact information:<br><br>"
        hr_body += f"<strong>First Name: </strong> {firstName}\n<br>"
        hr_body += f"<strong>Last Name: </strong> {lastName}\n<br>"
        hr_body += f"<strong>Email Address: </strong> {email}\n<br><br>"
        hr_body += f"Please reach out to them as soon as possible to discuss their specific requirements and provide any necessary assistance.<br>"
        hr_body += f"Thank you for your attention to this matter.<br><br>"
        hr_body += f"Best regards,<br>"
        hr_body += f" CD Virtual Assistant"


        hr_msg.attach(MIMEText(hr_body, 'html'))
        hr_server = smtplib.SMTP('smtp.gmail.com', 587)
        hr_server.starttls()
        hr_server.login(senderEmail, sendPassword)
        hr_text = hr_msg.as_string()
        hr_server.sendmail(senderEmail, receiverEmail, hr_text)
        hr_server.quit()

        user_msg = MIMEMultipart()
        user_msg['From'] = senderEmail
        user_msg['To'] = email
        user_msg['Subject'] = "Thank you for reaching Cloud Destinations"

        user_body = f"Dear {firstName},<br><br>"
        user_body += f"Thank you for reaching Cloud Destinations!<br><br>"
        user_body += f"We are delighted that you have taken the time to explore our company website. Your interest in our services is greatly appreciated. Our dedicated sales team has been notified of your visit and they will reach out to you shortly to discuss how Cloud Destinations can assist you with your specific needs.<br><br>"
        user_body += f"Once again, thank you for reaching Cloud Destinations. We look forward to the opportunity of working with you and meeting your requirements.<br><br>"
        user_body += f"Best regards,<br>"
        user_body += f"CD Virtual Assistant"
        
        user_msg.attach(MIMEText(user_body, 'html'))
        user_server = smtplib.SMTP('smtp.gmail.com', 587)
        user_server.starttls()
        user_server.login(senderEmail, sendPassword)
        user_text = user_msg.as_string()
        user_server.sendmail(senderEmail, email, user_text)
        user_server.quit()
        return 'Emails sent successfully'
    except Exception as e:
        print("Exception: %s %s" % (type(e), str(e.args)))
        raise SystemExit

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

