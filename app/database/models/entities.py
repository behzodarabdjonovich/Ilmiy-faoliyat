from datetime import datetime
from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey, Integer, Boolean, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    telegram_id: Mapped[int]=mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str|None]=mapped_column(String(255))
    full_name: Mapped[str]=mapped_column(String(255), default="")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())

class Organization(Base):
    __tablename__="organizations"
    id: Mapped[int]=mapped_column(primary_key=True)
    full_name: Mapped[str]=mapped_column(String(500))
    short_name: Mapped[str|None]=mapped_column(String(255))
    address: Mapped[str|None]=mapped_column(String(500))
    phone: Mapped[str|None]=mapped_column(String(100))
    email: Mapped[str|None]=mapped_column(String(255))
    website: Mapped[str|None]=mapped_column(String(255))
    stir: Mapped[str|None]=mapped_column(String(50))
    bank_details: Mapped[str|None]=mapped_column(Text)
    leader_name: Mapped[str|None]=mapped_column(String(255))
    leader_position: Mapped[str|None]=mapped_column(String(255))
    logo_path: Mapped[str|None]=mapped_column(String(500))
    default_signer: Mapped[str|None]=mapped_column(String(255))
    number_prefix: Mapped[str]=mapped_column(String(50), default="01-12")
    reset_yearly: Mapped[bool]=mapped_column(Boolean, default=True)

class OrganizationMember(Base):
    __tablename__="organization_members"
    __table_args__=(UniqueConstraint("organization_id","user_id"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    organization_id: Mapped[int]=mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str]=mapped_column(String(30), default="member")

class Letter(Base):
    __tablename__="letters"
    __table_args__=(UniqueConstraint("organization_id","letter_number", name="uq_org_letter_number"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int|None]=mapped_column(ForeignKey("organizations.id"))
    letter_number: Mapped[str|None]=mapped_column(String(100), index=True)
    letter_type: Mapped[str]=mapped_column(String(100))
    recipient: Mapped[str]=mapped_column(String(500))
    recipient_person: Mapped[str|None]=mapped_column(String(255))
    recipient_position: Mapped[str|None]=mapped_column(String(255))
    subject: Mapped[str]=mapped_column(String(500))
    content: Mapped[str]=mapped_column(Text)
    signer_name: Mapped[str|None]=mapped_column(String(255))
    signer_position: Mapped[str|None]=mapped_column(String(255))
    attachments: Mapped[str|None]=mapped_column(Text)
    status: Mapped[str]=mapped_column(String(30), default="draft")
    prompt_tokens: Mapped[int|None]=mapped_column(Integer)
    completion_tokens: Mapped[int|None]=mapped_column(Integer)
    total_tokens: Mapped[int|None]=mapped_column(Integer)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class LetterVersion(Base):
    __tablename__="letter_versions"
    __table_args__=(UniqueConstraint("letter_id","version_number"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    letter_id: Mapped[int]=mapped_column(ForeignKey("letters.id", ondelete="CASCADE"))
    version_number: Mapped[int]=mapped_column(Integer)
    content: Mapped[str]=mapped_column(Text)
    edit_instruction: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())

class LetterCounter(Base):
    __tablename__="letter_counters"
    __table_args__=(UniqueConstraint("organization_id","year"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    organization_id: Mapped[int]=mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    year: Mapped[int]=mapped_column(Integer)
    value: Mapped[int]=mapped_column(Integer, default=0)

class Setting(Base):
    __tablename__="settings"
    id: Mapped[int]=mapped_column(primary_key=True)
    key: Mapped[str]=mapped_column(String(255), unique=True)
    value: Mapped[str]=mapped_column(Text)

class AuditLog(Base):
    __tablename__="audit_logs"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int|None]=mapped_column(ForeignKey("users.id"))
    action: Mapped[str]=mapped_column(String(255))
    details: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
