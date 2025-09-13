from fastapi import FastAPI
from pydantic import BaseModel, Field
import datetime


class Booking(BaseModel):
    booking_id: int
    user_id: int
    room_id: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

class User(BaseModel):
    user_id: int
    username: str = Field(max_length=12)
    
class Room(BaseModel):
    romm_id: int
    room_name: str =Field(max_length=12)
    capacity: int
    
app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Success"}

@app.post("/users")
async def users(users: User):
    return {"users": users}

@app.post("/rooms")
async def CreateUser(rooms: Room):
    return {"rooms": rooms}

@app.post("/bookings")
async def CreateUser(bookings: Booking):
    return {"bookings": bookings}

