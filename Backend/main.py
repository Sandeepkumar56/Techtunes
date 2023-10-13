from typing import Union
import mysql.connector
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,date, time


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
        con.commit()
        con.close()
    
    except  mysql.connector.Error as e:
        return {"error_code":e.errno,"error_msg":e.msg}
    
    return {"msg":"booking alloted","reponse":serialized_data}
    # return {"msg":"done"}