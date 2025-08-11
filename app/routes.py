import os
from flask import Blueprint, jsonify, request

from .models import Contact, Message, Delivery
from .utils import sync_contacts_from_excel, start_safe_send_run
from . import db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Simple health check endpoint."""
    return {"status": "ok"}


@bp.route("/contacts")
def contacts_list():
    contacts = Contact.query.all()
    data = [
        {"id": c.id, "full_name": c.full_name, "phone": c.phone_e164, "tags": c.tags}
        for c in contacts
    ]
    return jsonify(data)


@bp.route("/contacts/sync", methods=["POST"])
def contacts_sync():
    """Upload an Excel file and sync contacts, returning a summary."""
    file = request.files.get("file")
    if not file:
        return {"error": "file required"}, 400
    path = "_upload.xlsx"
    file.save(path)
    summary = sync_contacts_from_excel(path)
    os.remove(path)
    return summary


@bp.route("/messages", methods=["GET"])
def list_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    data = [
        {"id": m.id, "template_name": m.template_name, "body_template": m.body_template}
        for m in messages
    ]
    return jsonify(data)


@bp.route("/messages", methods=["POST"])
def create_message():
    data = request.json
    msg = Message(template_name=data.get("template_name"), body_template=data.get("body_template"))
    db.session.add(msg)
    db.session.commit()
    return {"id": msg.id}


@bp.route("/messages/<int:message_id>", methods=["GET"])
def get_message(message_id):
    msg = Message.query.get_or_404(message_id)
    return {"id": msg.id, "template_name": msg.template_name, "body_template": msg.body_template}


@bp.route("/messages/<int:message_id>", methods=["PUT"])
def update_message(message_id):
    data = request.json
    msg = Message.query.get_or_404(message_id)
    msg.template_name = data.get("template_name", msg.template_name)
    msg.body_template = data.get("body_template", msg.body_template)
    db.session.commit()
    return {"status": "updated"}


@bp.route("/messages/<int:message_id>", methods=["DELETE"])
def delete_message(message_id):
    msg = Message.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    return {"status": "deleted"}


@bp.route("/send/<int:message_id>", methods=["POST"])
def send_safe(message_id):
    message = Message.query.get_or_404(message_id)
    ids = request.json.get("contact_ids", [])
    contacts = Contact.query.filter(Contact.id.in_(ids)).all()
    run = start_safe_send_run(message, contacts)
    return {"run_id": run.id, "deliveries": len(contacts)}

