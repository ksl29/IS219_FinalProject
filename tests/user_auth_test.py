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
    
    
def test_successful_login(client):
    # test that viewing the page renders without template errors
    assert client.get("/signin").status_code == 200
    client.post("/signup",
                data={"f_name": "Abe", "l_name": "Def", "email": "abe@def", "password": "Abcdef123",
                      "confirm": "Abcdef123"})
    response = client.post("/signin", data={"email": "abe@def", "password": "Abcdef123"}, follow_redirects=True)
    assert b"Welcome" in response.data


def test_bad_login(client):
    assert client.get("/signin").status_code == 200
    response = client.post("/signin",
                           data={"email": "random@email", "password": "random123"})
    # incorrect signin redirects to signin page
    assert "/signin" == response.headers["Location"]


def test_bad_email(client):
    #testing to see what happens when the email doesnt match email format
    response = client.post("/signup", data={"f_name": "Abel", "l_name": "Daft", "email": "", "password": "Sobad1234", "confirm": "Sobad1234"},
                           follow_redirects=True)
    assert b'This field is required' in response.data


def test_password_confirmation(client):
    #tests to see that passwords need to match
    response = client.post(
        "/signup", data={"f_name": "Abel", "l_name": "Daft", "email": "a@d", "password": "Sobad1234", "confirm": ""}
    )
    # tests that this error message shows when passwords don't match
    assert b"Passwords must match" in response.data
    
    
def test_duplicate_registration(client):
    #testing that trying to create the same account twice results in an error
    response = client.post("/signup",
                           data={"f_name": "Abel", "l_name": "Daft", "email": "hate@twice", "password": "Sobad1234", "confirm": "Sobad1234"},
                           follow_redirects=True)
    response = client.post("/signup",
                           data={"f_name": "Abel", "l_name": "Daft", "email": "hate@twice", "password": "Sobad1234", "confirm": "Sobad1234"},
                           follow_redirects=True)
    assert b'Already Registered' in response.data


def test_access_denied(client):
    # trying to access a @login.required page while not logged in
    response = client.get("/home", follow_redirects = True)
    assert b"Please log in to access this page." in response.data


def test_access_granted(client):
    #allows signed in users to see the home page
    client.post("/signup",
                data={"f_name": "Abe", "l_name": "Def", "email": "abe@def", "password": "Abcdef123",
                      "confirm": "Abcdef123"})
    client.post("/signin", data={"email": "abe@def", "password": "Abcdef123"}, follow_redirects=True)
    response = client.get("/home")
    assert response.status_code == 200
    
    
def test_edit_account_info(client):
    #testing to see if updating account info works without errors
    client.post("/signup",
                data={"f_name": "Abe", "l_name": "Def", "email": "abe@def", "password": "Abcdef123",
                      "confirm": "Abcdef123"},follow_redirects = True)
    client.post("/signin", data={"email": "abe@def", "password": "Abcdef123"},follow_redirects = True)
    response = client.post("/account", data={"email": "abe@def", "password": "Abcde1234","confirm": "Abcde1234"},follow_redirects = True)
    assert b"You Successfully Updated your Password or Email" in response.data