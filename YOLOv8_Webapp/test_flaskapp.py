import pytest
from flask import template_rendered
from flaskapp import app

# Fixture for client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)



# Test for home route
def test_home_route(client):
    rv = client.get('/home')
    print("Status code:", rv.status_code)
    print("Data:", rv.data)
    assert rv.status_code == 200
    assert b'PROJECT OBJECT DETECTION' in rv.data

# Test for front route
def test_front_route(client, captured_templates):
    rv = client.get('/FrontPage')
    assert rv.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'videoprojectnew.html'


# Test for video route
def test_video_route(client):
    with client.session_transaction() as sess:
        sess['video_path'] = './test/test_video.mp4'
    rv = client.get('/video')
    assert rv.status_code == 200
    assert rv.mimetype == 'multipart/x-mixed-replace'


# Test for webapp route
def test_webapp_route(client):
    rv = client.get('/webapp')
    assert rv.status_code == 200
    assert rv.mimetype == 'multipart/x-mixed-replace'
