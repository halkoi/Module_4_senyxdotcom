import allure
import pytest
from faker import Faker
from models.base_models import MoviesListResponse, MovieResponse

fake = Faker()


@allure.feature("Movies")
class TestMoviesPositive:

    @allure.story("Создание фильма")
    @allure.title("Создать фильм с валидными данными")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_movie(self, super_admin, movie_data):
        response = super_admin.api.movies_api.create_movie(
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

    @allure.story("Получение фильма")
    @allure.title("Получить фильм по ID")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movie_by_id(self, super_admin, created_movie):
        response = super_admin.api.movies_api.get_movie_by_id(
            created_movie["id"]
        )
        data = response.json()

        assert data["id"] == created_movie["id"]
        assert data["name"] == created_movie["name"]
        assert data["price"] == created_movie["price"]

    @allure.story("Получение списка фильмов")
    @allure.title("Получить список всех фильмов и проверить схему ответа")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_movies(self, super_admin):
        response = super_admin.api.movies_api.get_movies()

        movies_data = MoviesListResponse(**response.json())

        assert movies_data.count >= 0
        assert isinstance(movies_data.movies, list)

    @allure.story("Получение списка фильмов")
    @allure.title("Получить фильмы с фильтрами: цена, локация, жанр")
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("params", [
        {"minPrice": 1, "maxPrice": 500},
        {"locations": ["MSK"]},
        {"genreId": 1},
    ])
    def test_get_movies_with_filters(self, super_admin, params):
        response = super_admin.api.movies_api.get_movies(params=params)
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data["movies"], list)

        for movie in data["movies"]:
            if "minPrice" in params:
                assert params["minPrice"] <= movie["price"] <= params["maxPrice"]
            if "locations" in params:
                assert movie["location"] in params["locations"]
            if "genreId" in params:
                assert movie["genreId"] == params["genreId"]

    @allure.story("Получение списка фильмов")
    @allure.title("Получить фильмы с пагинацией: страница 1, размер 5")
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_movies_with_filter(self, super_admin):
        response = super_admin.api.movies_api.get_movies(
            params={"page": 1, "pageSize": 5}
        )
        data = response.json()

        assert "movies" in data
        assert isinstance(data["movies"], list)
        assert len(data["movies"]) <= 5

    @allure.story("Обновление фильма")
    @allure.title("Обновить название и цену фильма")
    @pytest.mark.api
    @pytest.mark.regression
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

    @allure.story("Удаление фильма")
    @allure.title("Удалить фильм — проверка прав для разных ролей")
    @pytest.mark.api
    @pytest.mark.regression
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

    @allure.story("Обновление фильма")
    @allure.title("Частичное обновление — изменить только цену")
    @pytest.mark.api
    @pytest.mark.regression
    def test_partial_update_movie(self, super_admin, created_movie):
        new_price = fake.random_int(min=100, max=1000)

        response = super_admin.api.movies_api.update_movie(
            created_movie["id"],
            {"price": new_price}
        )
        data = response.json()

        assert data["price"] == new_price
        assert data["name"] == created_movie["name"]

    @allure.story("Создание фильма")
    @allure.title("Создать фильм с published=False")
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_movie_with_published_false(self, super_admin, movie_data):
        movie_data["published"] = False

        response = super_admin.api.movies_api.create_movie(movie_data)
        data = response.json()

        assert data["published"] is False

        movie_id = data["id"]
        get_response = super_admin.api.movies_api.get_movie_by_id(movie_id)
        get_data = get_response.json()

        assert get_data["published"] is False

    @allure.story("Создание фильма")
    @allure.title("Создать фильм и проверить наличие в базе данных")
    @pytest.mark.api
    @pytest.mark.db
    @pytest.mark.smoke
    def test_create_movie_check_in_db(self, super_admin, movie_data, db_helper):
        response = super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=201
        )
        movie_id = response.json()["id"]

        db_movie = db_helper.get_movie_by_id(movie_id)

        assert db_movie is not None, "Фильм не найден в БД"
        assert db_movie.id == int(movie_id)
        assert db_movie.name == movie_data["name"]
        assert db_movie.price == movie_data["price"]
