class TestListUsers:
    def test_admin_can_list_users(self, client, admin_token, analyst_user, viewer_user):
        response = client.get("/api/users/", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        assert len(response.json()["data"]) >= 3
    def test_analyst_cannot_list_users(self, client, analyst_token):
        response = client.get("/api/users/", headers={
            "Authorization": f"Bearer {analyst_token}"
        })
        assert response.status_code == 403
    def test_viewer_cannot_list_users(self, client, viewer_token):
        response = client.get("/api/users/", headers={
            "Authorization": f"Bearer {viewer_token}"
        })
        assert response.status_code == 403
class TestGetUser:
    def test_admin_can_get_user(self, client, admin_token, analyst_user):
        response = client.get(f"/api/users/{analyst_user.id}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        assert response.json()["data"]["username"] == "testanalyst"
    def test_get_nonexistent_user(self, client, admin_token):
        response = client.get("/api/users/9999", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 404
class TestUpdateRole:
    def test_admin_can_update_role(self, client, admin_token, viewer_user):
        response = client.patch(f"/api/users/{viewer_user.id}/role", json={
            "role": "analyst"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["data"]["role"] == "analyst"
    def test_invalid_role_rejected(self, client, admin_token, viewer_user):
        response = client.patch(f"/api/users/{viewer_user.id}/role", json={
            "role": "superadmin"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 422
    def test_analyst_cannot_update_role(self, client, analyst_token, viewer_user):
        response = client.patch(f"/api/users/{viewer_user.id}/role", json={
            "role": "admin"
        }, headers={"Authorization": f"Bearer {analyst_token}"})
        assert response.status_code == 403
class TestUpdateStatus:
    def test_admin_can_deactivate_user(self, client, admin_token, viewer_user):
        response = client.patch(f"/api/users/{viewer_user.id}/status", json={
            "is_active": False
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["data"]["is_active"] is False
    def test_admin_can_reactivate_user(self, client, admin_token, viewer_user):
        client.patch(f"/api/users/{viewer_user.id}/status", json={
            "is_active": False
        }, headers={"Authorization": f"Bearer {admin_token}"})
        response = client.patch(f"/api/users/{viewer_user.id}/status", json={
            "is_active": True
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["data"]["is_active"] is True