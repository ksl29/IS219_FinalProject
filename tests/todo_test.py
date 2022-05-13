from app import db
from app.db.models import Task
from faker import Faker
import datetime
"""This test the homepage"""

def test_todo_pages(client):
    """testing todo pages"""
    response = client.get("/home")
    assert response.status_code == 302
    response = client.get("/tasks")
    assert response.status_code == 302
    response = client.get("/tasks/new")
    assert response.status_code == 302
    
    
def test_task_page_post(client):
    """testing post requests to get methods"""
    response = client.post("/tasks")
    assert response.status_code == 405
    assert b"Browse: Tasks" not in response.data
    

"""def test_delete_task(client):
    client.post("/signup",
            data={"f_name": "Abe", "l_name": "Def", "email": "abe@def", "password": "Abcdef123",
                    "confirm": "Abcdef123"})
    client.post("/signin", data={"email": "abe@def", "password": "Abcdef123"}, follow_redirects=True)
    client.post("/tasks/new",
                        data={"title": "test", "description": "this is a test",
                                "due_date": datetime.datetime(2022,5,19),"is_important": 1,"is_complete": 0}, follow_redirects=True)
    response = client.post("/tasks/1/delete", follow_redirects= True)
    assert b"Task Deleted" in response.data"""