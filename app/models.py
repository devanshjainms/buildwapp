from datetime import datetime
from . import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    full_name = db.Column(db.String(200))
    phone_e164 = db.Column(db.String(20), unique=True)
    whatsapp_link = db.Column(db.String(255))
    tags = db.Column(db.String(200))
    last_synced_at = db.Column(db.DateTime)
    opt_out = db.Column(db.Boolean, default=False)
    custom1 = db.Column(db.String(200))
    custom2 = db.Column(db.String(200))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100))
    body_template = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SendRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    run_started_at = db.Column(db.DateTime, default=datetime.utcnow)
    mode = db.Column(db.String(20))  # 'safe' or 'experimental'


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    run_id = db.Column(db.Integer, db.ForeignKey('send_run.id'))
    status = db.Column(db.String(20))
    status_reason = db.Column(db.Text)
    opened_at = db.Column(db.DateTime)
    sent_at = db.Column(db.DateTime)
    error = db.Column(db.Text)

