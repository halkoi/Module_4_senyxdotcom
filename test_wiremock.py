import datetime
import pytz
import requests
from pydantic import BaseModel, Field, ConfigDict


# Модель Pydantic для ответа сервера worldclockapi
class WorldClockResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="$id")
    currentDateTime: str
    utcOffset: str
    isDayLightSavingsTime: bool
    dayOfTheWeek: str
    timeZoneName: str
    currentFileTime: int
    ordinalDate: str
    serviceResponse: None


# Модель для запроса к сервису TodayIsHoliday
class DateTimeRequest(BaseModel):
    currentDateTime: str  # Формат: "2025-02-13T21:43Z"


# Модель для ответа от сервиса TodayIsHoliday
class WhatIsTodayResponse(BaseModel):
    message: str


# Функция выполняющая запрос в сервис worldclockapi для получения текущей даты
def get_worldclockap_time() -> WorldClockResponse:
    response = requests.get("http://worldclockapi.com/api/json/utc/now")
    assert response.status_code == 200, "Удаленный сервис недоступен"
    return WorldClockResponse(**response.json())


class TestTodayIsHolidayServiceAPI:

    def test_worldclockap(self):
        world_clock_response = get_worldclockap_time()
        current_date_time = world_clock_response.currentDateTime
        print(f"Текущая дата и время: {current_date_time=}")
        assert current_date_time == datetime.datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"

    def test_what_is_today(self):
        world_clock_response = get_worldclockap_time()

        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            json=DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump()
        )

        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "Сегодня нет праздников в России.", "Сегодня нет праздника!"


class TestWireMockWorldClock:

    def run_wiremock_worldclockap_time(self):
        wiremock_url = "http://localhost:8080/__admin/mappings"
        mapping = {
            "request": {
                "method": "GET",
                "url": "/wire/mock/api/json/utc/now"
            },
            "response": {
                "status": 200,
                "body": '''{
                    "$id": "1",
                    "currentDateTime": "2025-03-08T00:00Z",
                    "utcOffset": "00:00",
                    "isDayLightSavingsTime": false,
                    "dayOfTheWeek": "Wednesday",
                    "timeZoneName": "UTC",
                    "currentFileTime": 1324567890123,
                    "ordinalDate": "2025-1",
                    "serviceResponse": null
                }'''
            }
        }
        response = requests.post(wiremock_url, json=mapping)
        assert response.status_code == 201, "Не удалось настроить WireMock"

    def test_what_is_today_BY_WIREMOCK(self):
        self.run_wiremock_worldclockap_time()

        world_clock_response = requests.get("http://localhost:8080/wire/mock/api/json/utc/now")
        assert world_clock_response.status_code == 200, "Удаленный сервис недоступен"

        current_date_time = WorldClockResponse(**world_clock_response.json()).currentDateTime

        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            json=DateTimeRequest(currentDateTime=current_date_time).model_dump()
        )

        assert what_is_today_response.status_code == 200
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        assert what_is_today_data.message == "Международный женский день", "8 марта же?"
