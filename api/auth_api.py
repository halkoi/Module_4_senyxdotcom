from api.custom_requester import CustomRequester


class AuthAPI(CustomRequester):

    def login_user(self, data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint="/login",
            data=data,
            expected_status=expected_status
        )

    def authenticate(self, creds):
        email, password = creds

        response = self.login_user({
            "email": email,
            "password": password
        })

        tokens = response.json()
        access_token = tokens["accessToken"]

        # ТОКЕН
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

        return tokens