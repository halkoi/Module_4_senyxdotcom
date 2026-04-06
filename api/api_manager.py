from api.movies_api import MoviesAPI
from api.auth_api import AuthAPI
from config.hosts import BASE_URL, LOGIN_URL

class ApiManager:

    def __init__(self, session):
        self.session = session
        self.movies_api = MoviesAPI(session, BASE_URL)
        self.auth_api = AuthAPI(session, LOGIN_URL)