from app import create_app


def test_message_crud():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    client = app.test_client()

    # create
    res = client.post("/messages", json={"template_name": "Invite", "body_template": "Hi"})
    assert res.status_code == 200
    msg_id = res.get_json()["id"]

    # list
    res = client.get("/messages")
    msgs = res.get_json()
    assert any(m["id"] == msg_id for m in msgs)

    # update
    res = client.put(f"/messages/{msg_id}", json={"template_name": "Updated"})
    assert res.status_code == 200

    # retrieve
    res = client.get(f"/messages/{msg_id}")
    assert res.get_json()["template_name"] == "Updated"

    # delete
    res = client.delete(f"/messages/{msg_id}")
    assert res.status_code == 200
    res = client.get("/messages")
    assert not any(m["id"] == msg_id for m in res.get_json())
