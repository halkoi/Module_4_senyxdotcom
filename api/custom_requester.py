class CustomRequester:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def send_request(
        self,
        method,
        endpoint,
        data=None,
        params=None,
        expected_status=200
    ):
        url = f"{self.base_url.rstrip('/')}{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params
        )

        # логирование
        print(f"\n--- REQUEST ---")
        print(f"{method} {url}")
        print(f"BODY: {data}")
        print(f"PARAMS: {params}")

        print(f"\n--- RESPONSE ---")
        print(f"STATUS: {response.status_code}")
        print(f"BODY: {response.text}")

        if response.status_code != expected_status:
            raise AssertionError(
                f"\n{method} {endpoint}"
                f"\nExpected: {expected_status}"
                f"\nActual: {response.status_code}"
                f"\nResponse: {response.text}"
            )

        return response