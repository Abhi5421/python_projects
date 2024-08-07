from tests.conftest import test_db,TestSessionLocal
from api.v1.users.model import User


def test_signup(test_db):
    response = test_db.post("/public/user/sign-up", json={"email": "user11@example.com", "password": "Rohit@4522"})
    assert response.status_code == 200


def test_sign_up_user_exists(test_db):
    db = TestSessionLocal()
    user = User(email="existinguser@example.com", password="Rohit@4522")
    db.add(user)
    db.commit()
    db.close()

    existing_user = {"email": "existinguser@example.com", "password": "Rohit@4522"}
    response = test_db.post("/public/user/sign-up", json=existing_user)
    assert response.status_code == 500
    assert response.json() == {"detail": "user already exists, try login"}
