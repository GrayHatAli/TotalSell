from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class JournalEntry(TimestampMixin, Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_id: Mapped[int | None] = mapped_column(nullable=True)
    created_by: Mapped[int | None] = mapped_column(nullable=True)

    lines: Mapped[list["JournalLine"]] = relationship(back_populates="entry", cascade="all, delete-orphan")


class JournalLine(Base):
    __tablename__ = "journal_lines"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("journal_entries.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[int] = mapped_column(nullable=False, index=True)
    debit: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    credit: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    entry: Mapped[JournalEntry] = relationship(back_populates="lines")
