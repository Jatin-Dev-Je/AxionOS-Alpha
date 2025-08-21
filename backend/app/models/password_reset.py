from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from ..db.postgres import Base


class PasswordResetToken(Base):	
	__tablename__ = "password_reset_tokens"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
	token_hash = Column(String(128), nullable=False, unique=True, index=True)
	expires_at = Column(DateTime, nullable=False)
	used_at = Column(DateTime, nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

	# No explicit Index; 'index=True' on token_hash already creates one.
