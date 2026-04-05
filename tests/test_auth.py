class TestRegister:
    def test_register_success(self, client):
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "password123",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["username"] == "newuser"
        assert data["data"]["role"] == "viewer"
    def test_register_duplicate_username(self, client, admin_user):
        response = client.post("/api/auth/register", json={
            "username": "testadmin",
            "email": "unique@test.com",
            "password": "password123",
        })
        assert response.status_code == 409
    def test_register_duplicate_email(self, client, admin_user):
        response = client.post("/api/auth/register", json={
            "username": "uniqueuser",
            "email": "admin@test.com",
            "password": "password123",
        })
        assert response.status_code == 409
    def test_register_invalid_email(self, client):
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "not-an-email",
            "password": "password123",
        })
        assert response.status_code == 422
    def test_register_short_password(self, client):
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "12",
        })
        assert response.status_code == 422
class TestLogin:
    def test_login_success(self, client, admin_user):
        response = client.post("/api/auth/login", data={
            "username": "testadmin",
            "password": "admin123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    def test_login_wrong_password(self, client, admin_user):
        response = client.post("/api/auth/login", data={
            "username": "testadmin",
            "password": "wrongpassword",
        })
        assert response.status_code == 401
    def test_login_nonexistent_user(self, client):
        response = client.post("/api/auth/login", data={
            "username": "nobody",
            "password": "password",
        })
        assert response.status_code == 401
class TestGetMe:
    def test_get_me_success(self, client, admin_token):
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        assert response.json()["data"]["username"] == "testadmin"
    def test_get_me_no_token(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 401
    def test_get_me_invalid_token(self, client):
        response = client.get("/api/auth/me", headers={
            "Authorization": "Bearer invalid-token"
        })
        assert response.status_code == 401