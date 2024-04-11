import pytest
from flask import template_rendered
from flask_login import LoginManager,current_user
from modelos.usuarios_modelo import Usuario
from database import db
from app import create_app
import os
import sys
sys.path.insert(1, os.getcwd())


@pytest.fixture()
def app():
    app = create_app('sqlite://')
    app.config.update({
        "TESTING": True,
    })
  
    with app.app_context():
        db.create_all()
    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append(template)

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


