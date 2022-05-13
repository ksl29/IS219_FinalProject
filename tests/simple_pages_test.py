"""This test the homepage"""

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/contact"' in response.data
    #assert b'href="/tasks"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


def test_request_index(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Index" in response.data

def test_request_about(client):
    """This makes the index page"""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data

def test_request_contact(client):
    """This makes the index page"""
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"Contact" in response.data

def test_request_page_not_found(client):
    """This makes the index page"""
    response = client.get("/freebitcoin")
    assert response.status_code == 404