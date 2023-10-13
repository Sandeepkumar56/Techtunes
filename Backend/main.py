from typing import Union
import mysql.connector
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,date, time
from send_mail import send_email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:58755",  # Allow all origins for development, update this with your frontend domain in production
    "http://localhost:8000",
    "http://127.0.0.1:5500"  # Assuming your frontend is served from the same domain as your FastAPI app
]

# Add CORS middleware to allow specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

class BookingDetailsBase(BaseModel):
    Name: str
    email: str
    phone_num: str
    date: date
    time: time
    services: str
    

@app.post("/booking")
async def booking_det(booking_details:BookingDetailsBase):

    try:
        con= mysql.connector.connect(user='root', password='root123',
                                    host='127.0.0.1',port=3306, auth_plugin='mysql_native_password',
                                    database='techtunes')
        cursor= con.cursor()
        formatted_date = booking_details.date.strftime('%Y-%m-%d')
        formatted_time = booking_details.time.strftime('%H:%M:%S')
        
        serialized_data = {
            "Name": booking_details.Name,
            "email": booking_details.email,
            "phone_num": booking_details.phone_num,
            "date": formatted_date,
            "time": formatted_time,
            "services": booking_details.services
        }
        
        insert_data_tuple= tuple(serialized_data.values())
        print(insert_data_tuple)
        query='''INSERT INTO booking_details (Name, email, phone_num, date, time, services)
                VALUES (%s,%s,%s,%s,%s,%s);
                '''
        cursor.execute(query,insert_data_tuple)
        # send_email("theuntoldlegends5556@gmail.com",serialized_data["email"])
        sender_email = "sandeepn.20.becs@acharya.ac.in"
        receiver_email =serialized_data["email"] 
        subject = "Booking Confirmation"
        message = "Your Booking has been confirmed."

        # Gmail SMTP server configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Port for TLS encryption

        # Login credentials (generally, you should use environment variables or a secure method to store these)
        smtp_username = "sandeepn.20.becs@acharya.ac.in"
        smtp_password = "Sandeep5556@1"  # If you're using 2-factor authentication, use an App Password here

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            # Establish a secure session with Gmail's outgoing SMTP server using your gmail account
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Upgrade the connection to secure (TLS) mode
            server.login(smtp_username, smtp_password)  # Login with your Gmail address and App Password

            # Send email
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the server connection
            server.quit()

        con.commit()
        con.close()
    
    except  mysql.connector.Error as e:
        return {"error_code":e.errno,"error_msg":e.msg}
    
    return {"msg":"booking alloted and confirmation mail will be sent","reponse":serialized_data}
    # return {"msg":"done"}