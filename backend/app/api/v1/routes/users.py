from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from ....core.auth import get_current_user
from ....models.user import User


router = APIRouter()


class UserOut(BaseModel):
	id: int
	email: EmailStr
	full_name: str | None = None
	is_active: bool

	class Config:
		from_attributes = True


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
	return current_user

