"""This test the homepage"""

def test_request_main_menu_links(client):
    """tests menu links"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/signin"' in response.data
    assert b'href="/signup"' in response.data

def test_auth_pages(client):
    """testing auth pages"""
    response = client.get("/signin")
    assert response.status_code == 200
    response = client.get("/signup")
    assert response.status_code == 200
    response = client.get("/profile")
    assert response.status_code == 200
    response = client.get("/account")
    assert response.status_code == 200
    
def test_auth_pages_post(client):
    """testing post requests to get methods"""
    response = client.post("/profile")
    assert response.status_code == 405
    assert b"User Profile" not in response.data
    
    

