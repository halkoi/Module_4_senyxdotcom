from faker import Faker
import random
import uuid
fake = Faker()

class DataGenerator:

    @staticmethod
    def generate_movie(genre_id):
        return {
            "name":f"{fake.sentence(nb_words=3)} {uuid.uuid4()}",
            "imageUrl": "https://image.url",
            "price": random.randint(100, 1000),
            "description": fake.text(),
            "location": random.choice(["MSK", "SPB"]),
            "published": random.choice([True, False]),
            "genreId": genre_id
        }