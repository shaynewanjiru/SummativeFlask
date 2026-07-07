from app import app


def get_test_client():
    app.config["TESTING"] = True
    return app.test_client()