from app.models import Contact, Message
from app.utils import sync_contacts_from_excel


def test_full_safe_mode_flow(client, session, sample_xlsx):
    # Import contacts
    summary = sync_contacts_from_excel(sample_xlsx)
    assert summary["added"] == 4

    # Create message via API
    res = client.post("/messages", json={"template_name": "Invite", "body_template": "Hello {FirstName}"})
    msg_id = res.get_json()["id"]

    # Start send run via API using first two contacts
    contacts = [c.id for c in Contact.query.limit(2).all()]
    res = client.post(f"/send/{msg_id}", json={"contact_ids": contacts})
    data = res.get_json()
    assert data["deliveries"] == 2
    assert data["run_id"] >= 1

