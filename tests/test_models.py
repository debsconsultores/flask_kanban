from src.models import User

def test_password_hashing(app):

    user = User(
        username="test",
        email="test@example.com"
    )

    user.set_password("flask123")

    assert user.password_hash != "flask123"
    assert user.check_password("flask123") is True
    assert user.check_password("wrong") is False

