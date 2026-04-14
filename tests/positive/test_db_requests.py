# Можете сделать рандомный тестовый файл для проверки работы фикстуры
# Так сказать - поиграться


class TestDB:

    def test_movie_create_and_delete_in_db(self, super_admin, db_helper, movie_data):
        # ДО создания — фильма нет в БД
        # создаём через API
        response = super_admin.api.movies_api.create_movie(movie_data)
        movie_id = response.json()["id"]

        # ПОСЛЕ создания — фильм есть в БД
        assert db_helper.movie_exists_by_id(movie_id), "Фильм должен быть в БД после создания"

        db_movie = db_helper.get_movie_by_id(movie_id)
        assert db_movie.name == movie_data["name"]
        assert db_movie.price == movie_data["price"]

        # Удаляем через API
        super_admin.api.movies_api.delete_movie(movie_id)

        # Сбрасываем кэш SQLAlchemy чтобы получить актуальные данные из БД
        db_helper.db_session.expire_all()

        # ПОСЛЕ удаления — фильма нет в БД
        assert not db_helper.movie_exists_by_id(movie_id), "Фильм должен быть удалён из БД"


    def test_db_requests(self, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")