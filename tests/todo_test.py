"""This test the homepage"""

def test_todo_pages(client):
    """testing todo pages"""
    response = client.get("/home")
    assert response.status_code == 200
    response = client.get("/tasks")
    assert response.status_code == 200
    response = client.get("/tasks/new")
    assert response.status_code == 302
    
    
def test_task_page_post(client):
    """testing post requests to get methods"""
    response = client.post("/tasks")
    assert response.status_code == 405
    assert b"Browse: Tasks" not in response.data
    
    
