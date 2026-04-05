class TestCreateRecord:
    def test_admin_can_create_record(self, client, admin_token):
        response = client.post("/api/records/", json={
            "amount": 5000,
            "type": "income",
            "category": "salary",
            "date": "2025-01-01",
            "description": "Test salary",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201
        assert response.json()["data"]["amount"] == 5000
    def test_analyst_cannot_create_record(self, client, analyst_token):
        response = client.post("/api/records/", json={
            "amount": 100,
            "type": "expense",
            "category": "food",
            "date": "2025-01-01",
        }, headers={"Authorization": f"Bearer {analyst_token}"})
        assert response.status_code == 403
    def test_viewer_cannot_create_record(self, client, viewer_token):
        response = client.post("/api/records/", json={
            "amount": 100,
            "type": "expense",
            "category": "food",
            "date": "2025-01-01",
        }, headers={"Authorization": f"Bearer {viewer_token}"})
        assert response.status_code == 403
    def test_invalid_amount_rejected(self, client, admin_token):
        response = client.post("/api/records/", json={
            "amount": -100,
            "type": "expense",
            "category": "food",
            "date": "2025-01-01",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 422
    def test_invalid_type_rejected(self, client, admin_token):
        response = client.post("/api/records/", json={
            "amount": 100,
            "type": "donation",
            "category": "food",
            "date": "2025-01-01",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 422
class TestListRecords:
    def test_analyst_can_list_records(self, client, analyst_token, sample_records):
        response = client.get("/api/records/", headers={
            "Authorization": f"Bearer {analyst_token}"
        })
        assert response.status_code == 200
        assert response.json()["total"] == 6
    def test_viewer_cannot_list_records(self, client, viewer_token, sample_records):
        response = client.get("/api/records/", headers={
            "Authorization": f"Bearer {viewer_token}"
        })
        assert response.status_code == 403
    def test_filter_by_type(self, client, admin_token, sample_records):
        response = client.get("/api/records/?type=income", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        records = response.json()["records"]
        assert all(r["type"] == "income" for r in records)
    def test_filter_by_category(self, client, admin_token, sample_records):
        response = client.get("/api/records/?category=salary", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        records = response.json()["records"]
        assert all(r["category"] == "salary" for r in records)
    def test_filter_by_date_range(self, client, admin_token, sample_records):
        response = client.get(
            "/api/records/?start_date=2025-01-01&end_date=2025-01-31",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        assert response.json()["total"] == 4                        
    def test_pagination(self, client, admin_token, sample_records):
        response = client.get("/api/records/?page=1&limit=2", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["records"]) == 2
        assert data["total"] == 6
        assert data["pages"] == 3
class TestUpdateRecord:
    def test_admin_can_update_record(self, client, admin_token, sample_records):
        record_id = sample_records[0].id
        response = client.put(f"/api/records/{record_id}", json={
            "amount": 6000,
            "description": "Updated salary",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["data"]["amount"] == 6000
    def test_analyst_cannot_update_record(self, client, analyst_token, sample_records):
        record_id = sample_records[0].id
        response = client.put(f"/api/records/{record_id}", json={
            "amount": 6000,
        }, headers={"Authorization": f"Bearer {analyst_token}"})
        assert response.status_code == 403
class TestDeleteRecord:
    def test_admin_can_delete_record(self, client, admin_token, sample_records):
        record_id = sample_records[0].id
        response = client.delete(f"/api/records/{record_id}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        list_response = client.get("/api/records/", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert list_response.json()["total"] == 5
    def test_viewer_cannot_delete_record(self, client, viewer_token, sample_records):
        record_id = sample_records[0].id
        response = client.delete(f"/api/records/{record_id}", headers={
            "Authorization": f"Bearer {viewer_token}"
        })
        assert response.status_code == 403