import os
import re
import urllib.parse
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict

from . import db
from .models import Contact, Message, SendRun, Delivery


def normalize_phone(raw: str, default_country: str = "+1") -> str:
    """Normalize a phone number to E.164 using simple rules."""
    if raw is None:
        raise ValueError("no phone provided")
    digits = re.sub(r"\D", "", raw)
    if raw.strip().startswith("+"):
        e164 = "+" + digits
    else:
        e164 = default_country + digits
    if len(digits) < 7:
        raise ValueError("too few digits")
    return e164


def generate_wa_link(phone_e164: str, text: str) -> str:
    phone = phone_e164.lstrip("+")
    encoded = urllib.parse.quote(text)
    return f"https://wa.me/{phone}?text={encoded}"


def render_message(template: str, contact: Contact) -> str:
    """Render a message template with contact fields."""
    mapping = {
        "FirstName": contact.first_name or "",
        "LastName": contact.last_name or "",
        "FullName": contact.full_name or "",
        "Custom1": contact.custom1 or "",
        "Custom2": contact.custom2 or "",
    }
    pattern = re.compile(r"{([^{}]+)}")

    def repl(match):
        key = match.group(1)
        return mapping.get(key, "")

    return pattern.sub(repl, template)


# Minimal XLSX reader for files created by sample script
NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def read_xlsx(path: str) -> List[Dict[str, str]]:
    with zipfile.ZipFile(path) as zf:
        xml_bytes = zf.read("xl/worksheets/sheet1.xml")
    root = ET.fromstring(xml_bytes)
    rows = []
    for row in root.find("main:sheetData", NS):
        cells = []
        for c in row.findall("main:c", NS):
            is_elem = c.find("main:is", NS)
            if is_elem is not None:
                text = is_elem.find("main:t", NS).text or ""
            else:
                v = c.find("main:v", NS)
                text = v.text if v is not None else ""
            cells.append(text)
        rows.append(cells)
    headers = rows[0]
    data = []
    for r in rows[1:]:
        data.append(dict(zip(headers, r)))
    return data


def sync_contacts_from_excel(path: str, default_country: str = "+1") -> Dict[str, int]:
    rows = read_xlsx(path)
    summary = {"added": 0, "updated": 0, "invalid": 0}
    for row in rows:
        try:
            phone = normalize_phone(row.get("Phone", ""), default_country)
        except ValueError:
            summary["invalid"] += 1
            continue
        first = row.get("FirstName", "").strip()
        last = row.get("LastName", "").strip()
        tag = row.get("Tag", "").strip()
        full = f"{first} {last}".strip()
        custom1 = row.get("Custom1")
        custom2 = row.get("Custom2")
        contact = Contact.query.filter_by(phone_e164=phone).first()
        if contact:
            contact.first_name = first
            contact.last_name = last
            contact.full_name = full
            contact.tags = tag
            contact.custom1 = custom1
            contact.custom2 = custom2
            contact.last_synced_at = datetime.utcnow()
            summary["updated"] += 1
        else:
            link = generate_wa_link(phone, "")
            contact = Contact(
                first_name=first,
                last_name=last,
                full_name=full,
                phone_e164=phone,
                whatsapp_link=link,
                tags=tag,
                custom1=custom1,
                custom2=custom2,
                last_synced_at=datetime.utcnow(),
            )
            db.session.add(contact)
            summary["added"] += 1
    db.session.commit()
    return summary


def start_safe_send_run(message: Message, contacts: List[Contact]) -> SendRun:
    run = SendRun(message_id=message.id, mode="safe")
    db.session.add(run)
    db.session.commit()
    for contact in contacts:
        text = render_message(message.body_template, contact)
        link = generate_wa_link(contact.phone_e164, text)
        contact.whatsapp_link = link
        delivery = Delivery(
            contact_id=contact.id,
            message_id=message.id,
            run_id=run.id,
            status="PENDING",
        )
        db.session.add(delivery)
    db.session.commit()
    return run

