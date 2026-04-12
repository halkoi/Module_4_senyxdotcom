#data_generator.py
from faker import Faker
import random
import uuid

fake = Faker()

class DataGenerator:

    # --- USER ---
    @staticmethod
    def generate_random_email():
        return fake.email()

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