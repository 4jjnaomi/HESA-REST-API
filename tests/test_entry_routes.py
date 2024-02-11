# Test GET /entry
def test_get_entries(client):
    response = client.get('/entry')
    assert response.status_code == 200
    assert response.is_json

# Test GET /entry/<id>
def test_get_entry(client):
    response = client.get('/entry/755')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['entry_id'] == 755
    

# Test POST /entry
def test_add_entry(client):
    response_json = {
        "entry_id": "100000",
        "academic_year": "20/20",
        "classification": "dummy",
        "category_marker": "dummy",
        "category": "dummy",
        "value": "70",
        "UKPRN": "111111",
        "he_name": "University of Naomi"
    }
    response = client.post('/entry', json=response_json, content_type='application/json')
    assert response.status_code == 200

# Test DELETE /entry/<id>
def test_delete_entry(client, new_entry):
    entry_id = new_entry['entry_id']
    response = client.delete(f'/entry/{entry_id}')
    assert response.status_code == 200
    assert response.json == {"message": f"Entry {entry_id} deleted successfully"}

# Test DELETE /entry/<id> for nonexistent entry
def test_delete_nonexistent_entry(client):
    response = client.delete('/entry/123456')
    assert response.status_code == 404
    assert response.json == {'message': 'Entry with id 123456 not found.'}

# Test PATCH /entry/<id>
def test_patch_entry(client, new_entry):
    entry_id = new_entry['entry_id']
    response_json = {
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.patch(f'/entry/{entry_id}', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": f"Entry with entry_id {entry_id} updated successfully"}

# Test PATCH /entry/<id> for nonexistent entry
def test_patch_nonexistent_entry(client):
    response_json = {
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.patch('/entry/123456', json=response_json, content_type='application/json')
    assert response.status_code == 404
    assert response.json == {'message': 'No result found for entry_id: 123456'}

# Test PUT /entry/<id>
def test_put_update_entry(client, new_entry):
    entry_id = new_entry['entry_id']
    response_json = {
        "entry_id": entry_id,
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.put(f'/entry/{entry_id}', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"message": f"Entry with entry_id {entry_id} updated successfully"}

# Test PUT /entry/<id> for nonexistent entry
def test_put_new_entry(client):
    response_json = {
        "entry_id": "123456",
        "academic_year": "21/22",
        "classification": "updated",
        "category_marker": "updated",
        "category": "updated",
        "value": "80",
        "UKPRN": "222222",
        "he_name": "Updated University"
    }
    response = client.put('/entry/123456', json=response_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'message': 'Entry with entry_id 123456 updated successfully'}