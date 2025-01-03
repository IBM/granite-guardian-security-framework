from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from guardian import check_user_risk, check_ai_risk, all_checks
from send_email import send_email
from db import insert_data
import os
from dotenv import load_dotenv

load_dotenv()


class UserInput(BaseModel):
    input_text: str


class User(BaseModel):
    user_name: str
    email: str


class RiskAnalyse(BaseModel):
    user_input: str
    ai_response: Optional[str] = None
    context: Optional[str] = None


app = FastAPI()

user_name = "John Smith"  # Replace with actual user name retrieval logic
email = "john.smith@example.com"  # Replace with actual email retrieval logic


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/set-user")
def set_user(input: User):

    global user_name
    global email
    user_name = input.user_name
    email = input.email
    return {"message": f"User {user_name} with email {email} is set."}


@app.post("/user-risk")
def check_user_input(input: UserInput):
    # Process the user input here
    risk, prob_of_risk = check_user_risk(input.input_text)
    if risk == "Yes":
        # Check if the environment variable exists
        if os.getenv("SENDGRID_API_KEY"):
            send_email(
                risk_type="User Input",
                name=user_name,
                email=email,
            )

        insert_data(
            user_name=user_name,
            email=email,
            user_prompt=input.input_text,
            user_risk=risk,
            user_risk_prob=prob_of_risk,
        )
    return {"risk": risk, "prob_of_risk": prob_of_risk}


@app.post("/ai-risk")
def check_ai_response(input: RiskAnalyse):
    # Process the user input here
    risk, prob_of_risk = check_ai_risk(input.user_input, input.ai_response)
    if risk == "Yes":
        if os.getenv("SENDGRID_API_KEY"):
            send_email(risk_type="AI Response", name=user_name, email=email)

        insert_data(
            user_name=user_name,
            email=email,
            user_prompt=input.user_input,
            ai_response=input.ai_response,
            ai_risk=risk,
            ai_risk_prob=prob_of_risk,
        )
    return {"risk": risk, "prob_of_risk": prob_of_risk}


@app.post("/all-checks")
def risk_analyse(input: RiskAnalyse):
    # Process the user input here
    print("Input received:", input)
    risks = all_checks(input.user_input, ai_response=input.ai_response)
    print("Risks:", risks)
    if (
        risks["user_risk"] == "Yes"
        or risks["ai_risk"] == "Yes"
        or risks["relevance_risk_prob"] >= 0.8
    ):
        if os.getenv("SENDGRID_API_KEY"):
            send_email(risk_type="", name=user_name, email=email)

        insert_data(
            user_name=user_name,
            email=email,
            user_prompt=input.user_input,
            ai_response=input.ai_response,
            user_risk=risks["user_risk"],
            user_risk_prob=risks["user_risk_prob"],
            ai_risk=risks["ai_risk"],
            ai_risk_prob=risks["ai_risk_prob"],
            relevance_risk=risks["relevance_risk"],
            relevance_risk_prob=risks["relevance_risk_prob"],
        )
    return {
        "user_risk": risks["user_risk"],
        "ai_risk": risks["ai_risk"],
        "relevance_risk": risks["relevance_risk"],
    }
