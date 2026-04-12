from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from constants.roles import Roles


class RegistrationUserData(BaseModel):
    email: str = Field(..., description="Email пользователя")
    fullName: str
    password: str = Field(..., min_length=8, description="Пароль минимум 8 символов")
    passwordRepeat: str
    roles: List[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email должен содержать @")
        return value
