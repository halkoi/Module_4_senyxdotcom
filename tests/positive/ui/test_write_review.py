import time
from playwright.sync_api import sync_playwright
import allure
import pytest

from models.page_object_models import CinescopeRegisterPage
from data.data_generator import DataGenerator
from faker import Faker
from models.page_object_models import CinescopeMoviePage

fake = Faker()
import uuid

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie")
@pytest.mark.ui
class TestMoviePage:
   @allure.title("Успешная публикация отзыва")
   def test_post_review_by_ui(self, logined_test_user_ui, created_movie):
           #Подготовка текста отзыва
           random_review = f"{fake.sentence(nb_words=3)} {uuid.uuid4()}"
           movie_id = created_movie["id"]

           movie_page = CinescopeMoviePage(logined_test_user_ui) # Создаем объект страницы регистрации cinescope
           movie_page.open(movie_id=movie_id)
           movie_page.write_and_send_review(random_review)
           movie_page.assert_allert_was_pop_up()
           movie_page.make_screenshot_and_attach_to_allure("test_post_review")

           time.sleep(5)




