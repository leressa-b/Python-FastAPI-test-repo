from fastapi import APIRouter, Depends
from app.controllers import auth_controller

router = APIRouter()

@router.post("/login")
def login_user():
    return auth_controller.login()

@router.post("/signup")
def signup_user():
    return auth_controller.signup()
