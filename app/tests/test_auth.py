from app.controllers import auth_controller
from app.models.user import User
import pytest

def test_signup_then_login():
    user = User(username="test", password="pass123")
    auth_controller.signup(user)
    result = auth_controller.login(user)
    assert result["token_type"] == "bearer"

def test_invalid_login():
    with pytest.raises(Exception):
        auth_controller.login(User(username="ghost", password="bad"))
