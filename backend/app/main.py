from fastapi import FastAPI
from sqlalchemy.orm import Session

from .db.postgres import Base, engine
from .models import user as _user_model  # noqa: F401
from .models import password_reset as _password_reset_model  # noqa: F401
from .models import task as _task_model  # noqa: F401
from .api.v1.routes.auth import router as auth_router
from .api.v1.routes.users import router as users_router
from .api.v1.routes.tasks import router as tasks_router


def create_app() -> FastAPI:
	tags_metadata = [
		{"name": "auth", "description": "Authentication: register and login to obtain a JWT (OAuth2 password flow). Use the 'Authorize' button in Swagger to set your Bearer token."},
		{"name": "users", "description": "User profile endpoints. Requires Bearer token."},
	]
	app = FastAPI(
		title="AxionOS Alpha API",
		version="0.1.0",
		description=(
			"AxionOS Alpha backend API.\n\n"
			"Quick start in Swagger:\n"
			"1) POST /api/v1/auth/register to create a user.\n"
			"2) POST /api/v1/auth/login with form fields username and password to get a token.\n"
			"3) Click 'Authorize' in the top right and paste 'Bearer <token>'.\n"
			"4) Call /api/v1/users/me to verify authentication."
		),
		openapi_tags=tags_metadata,
	)

	# Create DB tables if not exist (dev convenience)
	Base.metadata.create_all(bind=engine)

	app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
	app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
	app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])

	@app.get("/health")
	def health():
		return {"status": "ok"}

	return app


app = create_app()

