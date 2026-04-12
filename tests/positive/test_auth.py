from api.api_manager import ApiManager
from models.base_models import RegisterUserResponse
from tests.conftest import super_admin


class TestAuth:

    def test_register_user(self, super_admin, registration_user_data):
        response = super_admin.api.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email, "Email не совпадает"

