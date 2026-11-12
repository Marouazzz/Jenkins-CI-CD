from app import app


def test_home_page_status():
    """Check that the home page loads successfully."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_hello_route():
    """Check that the hello route responds successfully."""
    client = app.test_client()
    response = client.post("/hello", data={"username": "Ouiam"})
    assert response.status_code == 200


def test_sum_route():
    """Check that the calculator route responds successfully."""
    client = app.test_client()
    response = client.post("/sum", data={"a": "5", "b": "3"})
    assert response.status_code == 200