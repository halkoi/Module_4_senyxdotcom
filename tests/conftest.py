import pytest
import requests
from config.hosts import BASE_URL, LOGIN_URL
from config.credentials import ADMIN_USERNAME, ADMIN_PASSWORD
from faker import Faker
from api.api_manager import ApiManager
from data.data_generator import DataGenerator


fake = Faker(locale='en_US')


@pytest.fixture
def auth_session_admin():
    session = requests.Session()

    auth_data = {
  "email": ADMIN_USERNAME,
  "password": ADMIN_PASSWORD
}
    auth_response = session.post(f"{LOGIN_URL}/login", json=auth_data)
    access_token = auth_response.json()["accessToken"]

    session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    return session



@pytest.fixture()
def created_genre(auth_session_admin):
    data = {
  "name": f"genre -{fake.word()}"
}
    response = auth_session_admin.post(f"{BASE_URL}/genres", json=data)
    assert response.status_code == 201

    genre = response.json()


    yield genre

    genre_id = genre["id"]

    auth_session_admin.delete(f"{BASE_URL}/genres/{genre_id}")


@pytest.fixture
def api_manager(auth_session_admin):
    return ApiManager(auth_session_admin)

@pytest.fixture
def movie_data(created_genre):
    return DataGenerator.generate_movie(created_genre["id"])

@pytest.fixture
def created_movie(api_manager, movie_data):
    response = api_manager.movies_api.create_movie(movie_data)
    movie = response.json()

    yield movie

    # проверяем без падения
    response = api_manager.session.get(
        f"{api_manager.movies_api.base_url}/movies/{movie['id']}"
    )

    if response.status_code == 200:
        api_manager.movies_api.delete_movie(movie["id"])


@pytest.fixture
def auth_admin(api_manager):
    creds = (ADMIN_USERNAME, ADMIN_PASSWORD)
    api_manager.auth_api.authenticate(creds)