from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Sample leave balances for demo purposes
leave_balances = {
    "john.doe@example.com": {"casual_leave": 5, "sick_leave": 3, "earned_leave": 10},
    "pini@example.com": {"casual_leave": 8, "sick_leave": 2, "earned_leave": 7},
}

# Pydantic model for incoming request
class LeaveRequest(BaseModel):
    email: str

# Webhook endpoint
@app.post("/leave-balance")
async def get_leave_balance(request: LeaveRequest):
    email = request.email
    if email in leave_balances:
        return {
            "status": "success",
            "email": email,
            "leave_balance": leave_balances[email]
        }
    else:
        return {
            "status": "error",
            "message": f"No leave data found for {email}"
        }

# Optional health check route
@app.get("/")
def root():
    return {"message": "Leave Balance API Webhook is live"}
