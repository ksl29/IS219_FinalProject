import logging

from flask import session
from app import db
from app.db.models import User


def test_successful_registration(client):
    # test that viewing the page renders without template errors
    assert client.get("/signup").status_code == 200

    # test that successful registration redirects to the login page
    response = client.post("/signup",
                           data={"f_name": "Abe", "l_name": "Def", "email": "abe@def", "password": "Abcdef123",
                                 "confirm": "Abcdef123"})
    assert "/signin" == response.headers["Location"]
    user = User.query.filter_by(email='abe@def').first()
    # asserting that the user retrieved is correct
    assert user.email == 'abe@def'

def test_bad_login(client):
    assert client.get("/signin").status_code == 200
    response = client.post("/signin",
                           data={"email": "random@email", "password": "random123"})
    # incorrect signin redirects to signin page
    assert "/signin" == response.headers["Location"]


def test_password_confirmation(client):
    response = client.post(
        "/signup", data={"f_name": "Abel", "l_name": "Daft", "email": "a@d", "password": "Sobad1234", "confirm": ""}
    )
    # tests that this error message shows when passwords don't match
    assert b"Passwords must match" in response.data


def test_access_denied(client):
    # trying to access a @login.required page while not logged in
    response = client.get("/users")
    assert "signin?next=%2Fusers" in response.headers["Location"]
