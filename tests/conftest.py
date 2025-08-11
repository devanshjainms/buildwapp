import pytest
from app import create_app, db
import zipfile


@pytest.fixture
def sample_xlsx(tmp_path):
    xml = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><worksheet "
        "xmlns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'><sheetData>"
        "<row r='1'><c r='A1' t='inlineStr'><is><t>FirstName</t></is></c>"
        "<c r='B1' t='inlineStr'><is><t>LastName</t></is></c>"
        "<c r='C1' t='inlineStr'><is><t>Phone</t></is></c>"
        "<c r='D1' t='inlineStr'><is><t>Tag</t></is></c>"
        "<c r='E1' t='inlineStr'><is><t>Custom1</t></is></c></row>"
        "<row r='2'><c r='A2' t='inlineStr'><is><t>Alice</t></is></c>"
        "<c r='B2' t='inlineStr'><is><t>Smith</t></is></c>"
        "<c r='C2' t='inlineStr'><is><t>1234567890</t></is></c>"
        "<c r='D2' t='inlineStr'><is><t>Family</t></is></c>"
        "<c r='E2' t='inlineStr'><is><t>Vegetarian</t></is></c></row>"
        "<row r='3'><c r='A3' t='inlineStr'><is><t>Bob</t></is></c>"
        "<c r='B3' t='inlineStr'><is><t>Jones</t></is></c>"
        "<c r='C3' t='inlineStr'><is><t>9876543210</t></is></c>"
        "<c r='D3' t='inlineStr'><is><t>Friend</t></is></c>"
        "<c r='E3' t='inlineStr'><is><t>Vegan</t></is></c></row>"
        "<row r='4'><c r='A4' t='inlineStr'><is><t>Carol</t></is></c>"
        "<c r='B4' t='inlineStr'><is><t>Lee</t></is></c>"
        "<c r='C4' t='inlineStr'><is><t>5551234567</t></is></c>"
        "<c r='D4' t='inlineStr'><is><t>Coworker</t></is></c>"
        "<c r='E4' t='inlineStr'><is><t>None</t></is></c></row>"
        "<row r='5'><c r='A5' t='inlineStr'><is><t>David</t></is></c>"
        "<c r='B5' t='inlineStr'><is><t>Kim</t></is></c>"
        "<c r='C5' t='inlineStr'><is><t>+14155550123</t></is></c>"
        "<c r='D5' t='inlineStr'><is><t>Family</t></is></c>"
        "<c r='E5' t='inlineStr'><is><t>None</t></is></c></row>"
        "<row r='6'><c r='A6' t='inlineStr'><is><t>Eve</t></is></c>"
        "<c r='B6' t='inlineStr'><is><t>Wong</t></is></c>"
        "<c r='C6' t='inlineStr'><is><t>invalid</t></is></c>"
        "<c r='D6' t='inlineStr'><is><t>Other</t></is></c>"
        "<c r='E6' t='inlineStr'><is><t>GlutenFree</t></is></c></row>"
        "</sheetData></worksheet>"
    )
    path = tmp_path / "contacts.xlsx"
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("xl/worksheets/sheet1.xml", xml)
    return str(path)


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session
        db.session.close()
