from api.api_manager import ApiManager
from faker import Faker
fake = Faker()


class TestMoviesNegative:

    def test_create_movie_without_name(self, super_admin, movie_data):
        movie_data.pop("name")

        super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=400
        )

    def test_create_movie_invalid_location(self, super_admin, movie_data):
        movie_data["location"] = "USA"

        super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=400
        )

    def test_create_movie_duplicate_name(self, super_admin, movie_data):
        # создаем первый фильм
        super_admin.api.movies_api.create_movie(movie_data)

        # пробуем создать с тем же name
        super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=409
        )

    def test_get_movie_not_found(self, super_admin):
        super_admin.api.movies_api.get_movie_by_id(
            movie_id=999999999,
            expected_status=404
        )

    def test_delete_movie_not_found(self, super_admin):
        super_admin.api.movies_api.delete_movie(
            movie_id=999999999,
            expected_status=404
        )

    def test_update_movie_not_found(self, super_admin):
        super_admin.api.movies_api.update_movie(
            movie_id=999999999,
            data={"name": fake.word()},
            expected_status=404
        )

    def test_create_movie_common_user(self, common_user, movie_data):
        common_user.api.movies_api.create_movie(
            movie_data,
            expected_status=403
        )
