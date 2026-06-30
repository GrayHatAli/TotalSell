from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ProductTag(Base):
    __tablename__ = "product_tags"

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
