# тут делал задание с метками

from api.api_manager import ApiManager
from faker import Faker
import pytest
from tests.conftest import super_admin

fake = Faker()

class TestMoviesPositive:

    @pytest.mark.skip(reason="Временно отключён")
    def test_create_movie(self, super_admin, movie_data):
        response = super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=202
        )
        data = response.json()

        assert data["id"] is not None
        assert data["name"] == movie_data["name"]
        assert data["price"] == movie_data["price"]
        assert data["location"] == movie_data["location"]
        assert data["genreId"] == movie_data["genreId"]
        assert data["published"] == movie_data["published"]

    skip_test = True

    @pytest.mark.skipif(skip_test, reason="Тест отключён вручную")
    def test_get_movie_by_id(self,super_admin, created_movie):
        response = super_admin.api.movies_api.get_movie_by_id(
            created_movie["id"]
        )
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == created_movie["name"]
        assert data["price"] == created_movie["price"]

    def test_get_movies(self, super_admin):
        response = super_admin.api.movies_api.get_movies()
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert data["count"] >= 0

    @pytest.mark.xfail(reason="Функция ещё не реализована")
    @pytest.mark.parametrize("params", [
        {"minPrice": 1, "maxPrice": 500},
        {"locations": ["MSK"]},
        {"genreId": 1},
    ])
    def test_get_movies_with_filters(self, super_admin, params):
        response = super_admin.api.movies_api.get_movies(params=params)
        data = response.json()

        assert response.status_code == 205
        assert isinstance(data["movies"], list)

        for movie in data["movies"]:
            if "minPrice" in params:
                assert params["minPrice"] <= movie["price"] <= params["maxPrice"]
            if "locations" in params:
                assert movie["location"] in params["locations"]
            if "genreId" in params:
                assert movie["genreId"] == params["genreId"]

    @pytest.mark.usefixtures("super_admin") # тут она должна была работать но какая то хуйня
    def test_get_movies_with_filter(self, super_admin):
        response = super_admin.api.movies_api.get_movies(
            params={"page": 1, "pageSize": 5}
        )
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert len(data["movies"]) <= 5

    def test_update_movie(self, super_admin, created_movie):
        updated_data = {
            "name": fake.sentence(nb_words=3),
            "price": fake.random_int(min=100, max=1000)
        }

        response = super_admin.api.movies_api.update_movie(
            created_movie["id"],
            updated_data,
            expected_status=200
        )
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == updated_data["name"]
        assert data["price"] == updated_data["price"]

    @pytest.mark.parametrize("role,expected_delete,expected_get", [
        ("super_admin", 200, 404),
        ("common_user", 403, 200),
        ("admin", 403, 200),
    ])
    def test_delete_movie(self, role, expected_delete, expected_get, created_movie, request):
        user = request.getfixturevalue(role)

        response = user.api.movies_api.delete_movie(
            created_movie["id"],
            expected_status=expected_delete
        )

        if expected_delete == 200:
            assert response.json()["id"] == created_movie["id"]

        user.api.movies_api.get_movie_by_id(
            created_movie["id"],
            expected_status=expected_get
        )

    def test_partial_update_movie(self, super_admin, created_movie):
        new_price = fake.random_int(min=100, max=1000)

        response = super_admin.api.movies_api.update_movie(
            created_movie["id"],
            {"price": new_price}
        )
        data = response.json()

        assert data["price"] == new_price
        assert data["name"] == created_movie["name"]  # не изменилось

    def test_movie_response_structure(self, super_admin, created_movie):
        response = super_admin.api.movies_api.get_movie_by_id(created_movie["id"])
        data = response.json()

        expected_fields = [
            "id", "name", "price", "description",
            "location", "published", "genreId", "createdAt"
        ]

        for field in expected_fields:
            assert field in data

    def test_create_movie_with_published_false(self, super_admin, movie_data):
        movie_data["published"] = False

        response = super_admin.api.movies_api.create_movie(movie_data)
        data = response.json()

        assert data["published"] is False

        # проверка сохранения через гет
        movie_id = data["id"]

        get_response = super_admin.api.movies_api.get_movie_by_id(movie_id)
        get_data = get_response.json()

        assert get_data["published"] is False

