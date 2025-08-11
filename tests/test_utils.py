from app.utils import (
    normalize_phone,
    render_message,
    generate_wa_link,
    read_xlsx,
    sync_contacts_from_excel,
    start_safe_send_run,
)
from app.models import Contact, Message
from app import db


def test_normalize_phone_default():
    assert normalize_phone("123-456-7890") == "+11234567890"


def test_normalize_phone_with_plus():
    assert normalize_phone("+1 (234) 567-8900") == "+12345678900"


def test_normalize_phone_invalid():
    try:
        normalize_phone("123")
        assert False, "should raise"
    except ValueError:
        assert True


def test_render_message_basic(session):
    c = Contact(first_name="Alice", last_name="Smith", full_name="Alice Smith")
    msg = render_message("Hi {FirstName} {LastName}", c)
    assert msg == "Hi Alice Smith"


def test_render_message_missing_field(session):
    c = Contact(first_name="Bob", last_name="Jones", full_name="Bob Jones")
    msg = render_message("Hello {FullName} {Unknown}", c)
    assert msg == "Hello Bob Jones "


def test_generate_wa_link_encoding():
    link = generate_wa_link("+1234567890", "Hello World")
    assert link == "https://wa.me/1234567890?text=Hello%20World"


def test_read_xlsx(sample_xlsx):
    rows = read_xlsx(sample_xlsx)
    assert rows[0]["FirstName"] == "Alice"
    assert rows[-1]["Phone"] == "invalid"


def test_sync_contacts_from_excel(session, sample_xlsx):
    summary = sync_contacts_from_excel(sample_xlsx)
    assert summary["added"] == 4  # one invalid
    assert summary["invalid"] == 1


def test_sync_contacts_upsert(session, sample_xlsx):
    sync_contacts_from_excel(sample_xlsx)
    # second time should update existing
    summary = sync_contacts_from_excel(sample_xlsx)
    assert summary["updated"] == 4


def test_start_safe_send_run(session, sample_xlsx):
    sync_contacts_from_excel(sample_xlsx)
    contacts = Contact.query.all()[:2]
    msg = Message(template_name="test", body_template="Hi {FirstName}")
    db.session.add(msg)
    db.session.commit()
    run = start_safe_send_run(msg, contacts)
    assert run.mode == "safe"
    for c in contacts:
        assert "https://wa.me/" in c.whatsapp_link

