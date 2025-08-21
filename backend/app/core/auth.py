from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..db.postgres import get_db
from ..models.user import User
from .security import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = decode_token(token)
		email: str | None = payload.get("sub")
		if email is None:
			raise credentials_exception
	except Exception:
		raise credentials_exception

	user = db.query(User).filter(User.email == email).first()
	if user is None or not user.is_active:
		raise credentials_exception
	return user

