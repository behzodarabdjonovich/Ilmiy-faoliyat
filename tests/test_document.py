from pathlib import Path
from types import SimpleNamespace
from app.services.document_service import create_docx
def test_docx(tmp_path:Path):
    l=SimpleNamespace(letter_number="01/001",recipient="Test",recipient_person=None,subject="Mavzu",content="Matn",signer_position="Direktor",signer_name="A.A.",attachments=None)
    p=create_docx(l,None,tmp_path/'x.docx'); assert p.exists() and p.stat().st_size>0
