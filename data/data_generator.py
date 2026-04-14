#data_generator.py
from faker import Faker
import random
import uuid
import datetime

fake = Faker()

class DataGenerator:

    # --- USER ---
    @staticmethod
    def generate_random_email():
        return f"{uuid.uuid4()}@test.com"

    @staticmethod
    def generate_random_name():
        return fake.name()

    @staticmethod
    def generate_random_password():
        return "Test1234"

    @staticmethod
    def generate_user():
        password = DataGenerator.generate_random_password()
        return {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": ["USER"]
        }

    # --- MOVIE ---
    @staticmethod
    def generate_movie(genre_id):
        return {
            "name": f"{fake.sentence(nb_words=3)} {uuid.uuid4()}",
            "imageUrl": "https://image.url",
            "price": random.randint(100, 1000),
            "description": fake.text(),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": genre_id
        }

    # data_generator.py
    """
    Добавим метод в DataGenerator который сразу делает рандомные данные
    которые можно сразу передать в метод создания юзера через БД
    """

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_user_db_data():
        return {
            "email": DataGenerator.generate_random_email(),
            "full_name": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password(),
            "verified": True,
            "banned": False,
            "roles": "USER"
        }

    @staticmethod
    def generate_random_int(digits: int) -> int:
        return random.randint(10 ** (digits - 1), 10 ** digits - 1)
