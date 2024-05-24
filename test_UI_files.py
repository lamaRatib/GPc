from streamlit.testing.v1 import AppTest

def test_login():
    at = AppTest.from_file("login.py").run()
    
    assert not at.exception

def test_front():
    at = AppTest.from_file("front.py").run()
    assert not at.exception

def test_dashboard():
    at = AppTest.from_file("dashboard.py").run()
    assert not at.exception

def test_sentiment():
    at = AppTest.from_file("sentiment.py").run()
    assert not at.exception