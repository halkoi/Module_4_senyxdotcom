import pytest
import requests
from config.hosts import BASE_URL
from faker import Faker
from api.api_manager import ApiManager
from data.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.user import RegistrationUserData
from models.base_models import TestUser
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper



fake = Faker(locale='en_US')

@pytest.fixture()
def created_genre(super_admin):
    data = {
  "name": f"genre -{fake.word()}"
}
    response = super_admin.api.session.post(f"{BASE_URL}/genres", json=data)
    assert response.status_code == 201

    genre = response.json()


    yield genre

    genre_id = genre["id"]

    super_admin.api.session.delete(f"{BASE_URL}/genres/{genre_id}")


@pytest.fixture
def movie_data(created_genre):
    return DataGenerator.generate_movie(created_genre["id"])

@pytest.fixture
def created_movie(super_admin, movie_data):
    response = super_admin.api.movies_api.create_movie(movie_data)
    movie = response.json()

    yield movie

    # проверяем без падения
    response = super_admin.api.session.get(
        f"{super_admin.api.movies_api.base_url}/movies/{movie['id']}"
    )

    if response.status_code == 200:
        super_admin.api.movies_api.delete_movie(movie["id"])


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    creation_user_data.roles = [Roles.ADMIN]

    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture
def creation_user_data():
    user_data = DataGenerator.generate_user()
    user = RegistrationUserData(
        email=user_data["email"],
        fullName=user_data["fullName"],
        password=user_data["password"],
        passwordRepeat=user_data["passwordRepeat"],
        roles=[Roles.USER],
        verified=True,
        banned=False
    )
    print(user.model_dump_json())
    return user


@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()
    return RegistrationUserData(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)