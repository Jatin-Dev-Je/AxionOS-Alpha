from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ....db.postgres import get_db
from ....models.user import User
from ....models.password_reset import PasswordResetToken
from ....core.security import (
	get_password_hash,
	verify_password,
	create_access_token,
	generate_reset_token,
	hash_reset_token,
)
from ....core.auth import get_current_user
from ....config import MIN_PASSWORD_LENGTH, SMTP_HOST, APP_BASE_URL
from ....utils.mailer import send_email  # type: ignore


router = APIRouter()


class RegisterRequest(BaseModel):
	email: EmailStr
	password: str
	full_name: str | None = None


class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
	existing = db.query(User).filter(User.email == payload.email).first()
	if existing:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
	user = User(
		email=payload.email,
		hashed_password=get_password_hash(payload.password),
		full_name=payload.full_name,
		is_active=True,
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	token = create_access_token(subject=user.email)
	return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == form_data.username).first()
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
	token = create_access_token(subject=user.email)
	return TokenResponse(access_token=token)


class ForgotPasswordRequest(BaseModel):
	email: EmailStr


class ForgotPasswordResponse(BaseModel):
	message: str
	# For dev/testing only, we return token here; in prod, send via email
	reset_token: str | None = None


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == payload.email).first()
	# Always respond 200 to avoid user enumeration
	if not user:
		return ForgotPasswordResponse(message="If the email exists, a reset link has been sent.")
	# Generate and store hashed token
	plain_token = generate_reset_token()
	token_hash = hash_reset_token(plain_token)
	expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
	reset = PasswordResetToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at)
	db.add(reset)
	db.commit()
	# Send email if SMTP configured
	try:
		if SMTP_HOST:
			base = APP_BASE_URL or "http://localhost:3000"
			reset_link = f"{base}/reset-password?token={plain_token}"
			subject = "Reset your AxionOS password"
			html = f"<p>Click the link to reset your password:</p><p><a href='{reset_link}'>{reset_link}</a></p>"
			try:
				send_email(to=payload.email, subject=subject, html=html)
			except Exception:
				# fail closed to avoid leaking existence, but continue response
				pass
	except Exception:
		pass
	return ForgotPasswordResponse(message="If the email exists, a reset link has been sent.", reset_token=plain_token)


class ResetPasswordRequest(BaseModel):
	token: str
	new_password: str


@router.post("/reset-password", response_model=ForgotPasswordResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
	if len(payload.new_password) < MIN_PASSWORD_LENGTH:
		raise HTTPException(status_code=400, detail=f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
	token_hash = hash_reset_token(payload.token)
	reset = (
		db.query(PasswordResetToken)
		.filter(PasswordResetToken.token_hash == token_hash)
		.first()
	)
	if not reset or reset.used_at is not None or reset.expires_at < datetime.now(timezone.utc):
		raise HTTPException(status_code=400, detail="Invalid or expired token")
	user = db.query(User).filter(User.id == reset.user_id).first()
	if not user:
		raise HTTPException(status_code=400, detail="Invalid token")
	user.hashed_password = get_password_hash(payload.new_password)
	reset.used_at = datetime.now(timezone.utc)
	db.add_all([user, reset])
	db.commit()
	return ForgotPasswordResponse(message="Password has been reset successfully.")


class ChangePasswordRequest(BaseModel):
	old_password: str
	new_password: str


@router.post("/change-password", response_model=ForgotPasswordResponse)
def change_password(
	payload: ChangePasswordRequest,
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user),
):
	if not verify_password(payload.old_password, current_user.hashed_password):
		raise HTTPException(status_code=400, detail="Old password is incorrect")
	if len(payload.new_password) < MIN_PASSWORD_LENGTH:
		raise HTTPException(status_code=400, detail=f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
	current_user.hashed_password = get_password_hash(payload.new_password)
	db.add(current_user)
	db.commit()
	return ForgotPasswordResponse(message="Password changed successfully.")

