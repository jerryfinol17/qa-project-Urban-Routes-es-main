import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages import UrbanRoutesPage
import data


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        chrome_options.add_experimental_option('w3c', True)
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.maximize_window()

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            cls.driver.quit()

    def test_complete_taxi_request(self):
        page = UrbanRoutesPage(self.driver)
        self.driver.get(data.urban_routes_url)
        page.set_route(data.address_from, data.address_to)
        assert page.get_from() == data.address_from, "La dirección 'from' no coincide"
        assert page.get_to() == data.address_to, "La dirección 'to' no coincide"
        page.click_order_taxi_button()
        page.select_comfort_tariff()
        page.fill_phone_number(data.phone_number)
        page.add_credit_card(data.card_number, data.card_code, "dummy_code")
        page.set_message(data.message_for_driver)
        page.request_blanket_tissues()
        page.request_ice_creams(2)
        page.request_taxi()
        assert page.validate_taxi_order(), "El pedido de taxi no se validó correctamente"


if __name__ == "__main__":
    pytest.main([__file__])