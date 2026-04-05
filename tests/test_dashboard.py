class TestSummary:
    def test_all_roles_can_view_summary(self, client, admin_token, analyst_token, viewer_token, sample_records):
        for token in [admin_token, analyst_token, viewer_token]:
            response = client.get("/api/dashboard/summary", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            data = response.json()
            assert "total_income" in data
            assert "total_expenses" in data
            assert "net_balance" in data
    def test_summary_values_are_correct(self, client, admin_token, sample_records):
        response = client.get("/api/dashboard/summary", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        data = response.json()
        assert data["total_income"] == 11200.0
        assert data["total_expenses"] == 2400.0
        assert data["net_balance"] == 8800.0
        assert data["total_records"] == 6
    def test_unauthenticated_cannot_view_summary(self, client):
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 401
class TestCategorySummary:
    def test_analyst_can_view_category_summary(self, client, analyst_token, sample_records):
        response = client.get("/api/dashboard/category-summary", headers={
            "Authorization": f"Bearer {analyst_token}"
        })
        assert response.status_code == 200
        assert "categories" in response.json()
    def test_viewer_cannot_view_category_summary(self, client, viewer_token, sample_records):
        response = client.get("/api/dashboard/category-summary", headers={
            "Authorization": f"Bearer {viewer_token}"
        })
        assert response.status_code == 403
class TestTrends:
    def test_admin_can_view_trends(self, client, admin_token, sample_records):
        response = client.get("/api/dashboard/trends", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert "trends" in data
        assert len(data["trends"]) >= 1
    def test_viewer_cannot_view_trends(self, client, viewer_token, sample_records):
        response = client.get("/api/dashboard/trends", headers={
            "Authorization": f"Bearer {viewer_token}"
        })
        assert response.status_code == 403
class TestRecent:
    def test_all_roles_can_view_recent(self, client, admin_token, viewer_token, sample_records):
        for token in [admin_token, viewer_token]:
            response = client.get("/api/dashboard/recent", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            assert "records" in response.json()
    def test_recent_returns_limited_records(self, client, admin_token, sample_records):
        response = client.get("/api/dashboard/recent", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert len(response.json()["records"]) <= 10