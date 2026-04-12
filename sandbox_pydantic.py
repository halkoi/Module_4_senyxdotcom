from models.user import RegistrationUserData
from constants.roles import Roles

# Успешно
try:
    user = RegistrationUserData(
        email="test@mail.com",
        fullName="Ivan Ivanov",
        password="12345678",
        passwordRepeat="12345678",
        roles=[Roles.USER]
    )
    print("Успех:", user)
except Exception as e:
    print("Ошибка:", e)

# Ошибка — нет @ в email
try:
    user = RegistrationUserData(
        email="testmail.com",
        fullName="Ivan Ivanov",
        password="12345678",
        passwordRepeat="12345678",
        roles=[Roles.USER]
    )
    print("Успех:", user)
except Exception as e:
    print("Ошибка:", e)

# Ошибка — пароль меньше 8 символов
try:
    user = RegistrationUserData(
        email="test@mail.com",
        fullName="Ivan Ivanov",
        password="123",
        passwordRepeat="123",
        roles=[Roles.USER]
    )
    print("Успех:", user)
except Exception as e:
    print("Ошибка:", e)
