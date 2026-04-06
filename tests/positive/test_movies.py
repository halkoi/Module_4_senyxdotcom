from api.api_manager import ApiManager
from faker import Faker
fake = Faker()

class TestMoviesPositive:

    def test_create_movie(self, api_manager: ApiManager, movie_data):
        response = api_manager.movies_api.create_movie(
            movie_data,
            expected_status=201
        )
        data = response.json()

        assert data["id"] is not None
        assert data["name"] == movie_data["name"]
        assert data["price"] == movie_data["price"]
        assert data["location"] == movie_data["location"]
        assert data["genreId"] == movie_data["genreId"]
        assert data["published"] == movie_data["published"]

    def test_get_movie_by_id(self, api_manager: ApiManager, created_movie):
        response = api_manager.movies_api.get_movie_by_id(
            created_movie["id"]
        )
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == created_movie["name"]
        assert data["price"] == created_movie["price"]

    def test_get_movies(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movies()
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert data["count"] >= 0

    def test_get_movies_with_filter(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movies(
            params={"page": 1, "pageSize": 5}
        )
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert len(data["movies"]) <= 5

    def test_update_movie(self, api_manager: ApiManager, auth_admin, created_movie):
        updated_data = {
            "name": fake.sentence(nb_words=3),
            "price": fake.random_int(min=100, max=1000)
        }

        response = api_manager.movies_api.update_movie(
            created_movie["id"],
            updated_data,
            expected_status=200
        )
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == updated_data["name"]
        assert data["price"] == updated_data["price"]

    def test_delete_movie(self, api_manager: ApiManager, auth_admin, created_movie):
        response = api_manager.movies_api.delete_movie(
            created_movie["id"],
            expected_status=200
        )

        data = response.json()
        assert data["id"] == created_movie["id"]

        # Проверяем что удалился
        api_manager.movies_api.get_movie_by_id(
            created_movie["id"],
            expected_status=404
        )

    def test_partial_update_movie(self, api_manager: ApiManager, created_movie):
        new_price = fake.random_int(min=100, max=1000)

        response = api_manager.movies_api.update_movie(
            created_movie["id"],
            {"price": new_price}
        )
        data = response.json()

        assert data["price"] == new_price
        assert data["name"] == created_movie["name"]  # не изменилось

    def test_movie_response_structure(self, api_manager: ApiManager, created_movie):
        response = api_manager.movies_api.get_movie_by_id(created_movie["id"])
        data = response.json()

        expected_fields = [
            "id", "name", "price", "description",
            "location", "published", "genreId", "createdAt"
        ]

        for field in expected_fields:
            assert field in data

    def test_create_movie_with_published_false(self, api_manager: ApiManager, movie_data):
        movie_data["published"] = False

        response = api_manager.movies_api.create_movie(movie_data)
        data = response.json()

        assert data["published"] is False

        # проверка сохранения через гет
        movie_id = data["id"]

        get_response = api_manager.movies_api.get_movie_by_id(movie_id)
        get_data = get_response.json()

        assert get_data["published"] is False