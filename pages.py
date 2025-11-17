from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from helpers import retrieve_phone_code
import time


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.from_field = (By.ID, 'from')
        self.to_field = (By.ID, 'to')
        self.order_taxi_button = (By.XPATH, "//*[contains(translate(text(), 'PEDIR UN TAXI', 'pedir un taxi'), 'pedir un taxi')]")
        self.comfort_tariff = (By.XPATH, "//*[contains(translate(text(), 'COMFORT', 'comfort'), 'comfort')]")
        self.phone_field = (By.CLASS_NAME, 'np-text')
        self.phone_input_field = (By.ID, 'phone')
        self.next_button_phone = (By.CSS_SELECTOR, 'button[type="submit"].button.full')
        self.next_button_card = (By.CSS_SELECTOR, '#root > div > div.payment-picker.open > div.modal.unusual > div.section.active.unusual > form > div.pp-buttons > button:nth-child(1)')
        self.code_field = (By.XPATH, '//*[@id="code"]')
        self.confirm_button = (By.CSS_SELECTOR, '#root > div > div.number-picker.open > div.modal > div.section.active > form > div.buttons > button:nth-child(1)')
        self.close_code_modal = (By.CSS_SELECTOR, '#root > div > div.number-picker.open > div.modal > div.section.active > button')
        self.payment_method_button = (By.CLASS_NAME, 'pp-button.filled')
        self.add_card_button = (By.CSS_SELECTOR, '#root > div > div.payment-picker.open > div.modal > div.section.active > div.pp-selector > div.pp-row.disabled > div.pp-title')
        self.card_number_field = (By.ID, 'number')
        self.card_code_field = (By.XPATH, '//*[@id="code" and contains(@class, "card-input")]')
        self.exit_button = (By.CSS_SELECTOR, '#root > div > div.payment-picker.open > div.modal > div.section.active > button')
        self.message_field = (By.ID, 'comment')
        self.reqs_button = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-header > div.reqs-head')
        self.reqs_open_class = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open')
        self.blanket_tissues_slider = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
        self.blanket_tissues_container = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw-label')
        self.ice_cream_plus = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div.r.r-type-group > div > div.r-group-items > div:nth-child(1) > div > div.r-counter > div > div.counter-plus')
        self.order_button = (By.CSS_SELECTOR, '#root > div > div.workflow > div.smart-button-wrapper > button > span.smart-button-main')
        self.modal_search = (By.CSS_SELECTOR, '#root > div > div.order.shown > div.order-body > div.order-header')
        self.payment_modal = (By.CSS_SELECTOR, 'div.payment-picker.open > div.modal.unusual')

    def _click_element(self, locator, description, screenshot_name=None):
        """Maneja clics con reintentos y captura de pantalla opcional."""
        element = self.wait.until(EC.element_to_be_clickable(locator), message=f"No se encontró {description}")
        try:
            element.click()
        except ElementClickInterceptedException:
            print(f"Clic interceptado en {description}, intentando con JavaScript")
            self.driver.execute_script("arguments[0].click();", element)
            if screenshot_name:
                self._take_screenshot(screenshot_name)
        return element

    def _take_screenshot(self, name):
        """Toma una captura de pantalla con un nombre específico."""
        self.driver.save_screenshot(f"{name}.png")
        print(f"Captura de pantalla tomada: {name}.png")

    def _ensure_phone_modal_closed(self):
        """Cierra el submenú de teléfono si está abierto."""
        try:
            self.wait.until_not(EC.presence_of_element_located(self.close_code_modal), message="Submenú de teléfono sigue abierto")
            print("Submenú de teléfono cerrado.")
        except TimeoutException:
            try:
                self._click_element(self.close_code_modal, "botón de cierre del submenú de código", "after_close_phone_modal")
                print("Submenú de teléfono cerrado manualmente.")
            except TimeoutException:
                print("No se pudo cerrar el submenú de teléfono, continuando...")

    def set_route(self, from_address, to_address):
        self.wait.until(EC.presence_of_element_located(self.from_field), message="No se encontró el campo 'from'").send_keys(from_address)
        self.wait.until(EC.presence_of_element_located(self.to_field), message="No se encontró el campo 'to'").send_keys(to_address)

    def get_from(self):
        return self.wait.until(EC.presence_of_element_located(self.from_field), message="No se encontró el campo 'from'").get_property('value')

    def get_to(self):
        return self.wait.until(EC.presence_of_element_located(self.to_field), message="No se encontró el campo 'to'").get_property('value')

    def click_order_taxi_button(self):
        self._click_element(self.order_taxi_button, "botón 'Pedir un taxi'")

    def select_comfort_tariff(self):
        self._click_element(self.comfort_tariff, "tarifa 'Comfort'")

    def fill_phone_number(self, phone_number):
        self._click_element(self.phone_field, "campo 'np-text'")
        phone_input = self.wait.until(EC.presence_of_element_located(self.phone_input_field), message="No se encontró el campo 'phone'")
        self.driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].focus();", phone_input)
        phone_input.clear()
        phone_input.send_keys(phone_number.replace(" ", ""))
        self.wait.until(lambda driver: phone_input.get_attribute('value') == phone_number.replace(" ", ""), message="El número de teléfono no se ingresó correctamente")
        print(f"Número de teléfono ingresado: {phone_input.get_attribute('value')}")
        self._click_element(self.next_button_phone, "botón 'Siguiente' después de ingresar el número", "after_next_button")
        phone_code = retrieve_phone_code(self.driver)
        code_element = self.wait.until(EC.element_to_be_clickable(self.code_field), message="No apareció el campo de código")
        code_element.clear()
        code_element.send_keys(phone_code)
        print(f"Código ingresado: {phone_code}")
        self._click_element(self.confirm_button, "botón 'Confirmar'", "after_confirm")
        try:
            self.wait.until(EC.visibility_of_element_located(self.payment_modal), message="No se encontró el modal de método de pago")
            print("Modal de método de pago encontrado.")
            self._ensure_phone_modal_closed()
        except TimeoutException:
            print("Timeout esperando el modal de método de pago.")
            self._take_screenshot("after_confirm_failed")
            self._ensure_phone_modal_closed()

    def add_credit_card(self, card_number, card_code, phone_code):
        try:
            self.wait.until(EC.visibility_of_element_located(self.payment_modal), message="No se encontró el modal de método de pago")
            print("Modal de método de pago encontrado.")
        except TimeoutException:
            print("Timeout esperando el modal de método de pago.")
            self._take_screenshot("payment_modal_timeout")
        self._click_element(self.payment_method_button, "botón 'pp-button.filled'", "payment_button_error")
        self._click_element(self.add_card_button, "botón 'Agregar tarjeta'", "add_card_button_error")
        card_number_element = self.wait.until(EC.element_to_be_clickable(self.card_number_field), message="No se encontró el campo 'number'")
        card_number_element.clear()
        card_number_element.send_keys(card_number)
        print(f"Número de tarjeta ingresado: {card_number_element.get_attribute('value')}")
        card_code_element = self.wait.until(EC.element_to_be_clickable(self.card_code_field), message="No se encontró el campo 'code' para la tarjeta")
        try:
            card_code_element.clear()
            card_code_element.send_keys(card_code)
        except Exception as e:
            print(f"Error al interactuar con el campo de código de tarjeta: {str(e)}")
            self.driver.execute_script("arguments[0].value = arguments[1];", card_code_element, card_code)
            self._take_screenshot("card_code_error")
        print(f"Código de tarjeta ingresado: {card_code_element.get_attribute('value')}")
        confirmation_element = self.wait.until(EC.element_to_be_clickable(self.card_code_field), message="No se encontró el campo de confirmación de la tarjeta")
        try:
            confirmation_element.clear()
            confirmation_element.send_keys(phone_code)
        except Exception as e:
            print(f"Error al interactuar con el campo de confirmación: {str(e)}")
            self.driver.execute_script("arguments[0].value = arguments[1];", confirmation_element, phone_code)
            self._take_screenshot("card_confirmation_error")
        print(f"Código de confirmación ingresado: {confirmation_element.get_attribute('value')}")
        self._click_element(self.next_button_card, "botón 'Siguiente' en el formulario de tarjeta", "next_button_error")
        self._click_element(self.exit_button, "botón de salida del submenú", "exit_button_error")
        message_field = self.wait.until(EC.visibility_of_element_located(self.message_field), message="El campo 'comment' no es visible")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", message_field)
        self._take_screenshot("after_scroll")

    def set_message(self, message):
        message_element = self.wait.until(EC.element_to_be_clickable(self.message_field), message="No se encontró el campo 'comment'")
        try:
            message_element.send_keys(message)
        except ElementClickInterceptedException:
            print("Clic interceptado en 'comment', intentando ocultar el label...")
            try:
                label = self.driver.find_element(By.XPATH, "//label[@for='comment']")
                self.driver.execute_script("arguments[0].style.display = 'none';", label)
            except:
                print("No se encontró el label para ocultar, continuando...")
            self.driver.execute_script("arguments[0].value = arguments[1];", message_element, message)
            self._take_screenshot("message_field_error")

    def _ensure_requirements_menu_open(self):
        """Asegura que el menú de requisitos esté abierto."""
        try:
            reqs_open = self.wait.until(EC.presence_of_element_located(self.reqs_open_class), message="El menú de requisitos no está abierto")
            if not reqs_open.is_displayed():
                self._click_element(self.reqs_button, "botón de requisitos", "after_reqs_button_open")
        except TimeoutException:
            self._click_element(self.reqs_button, "botón de requisitos", "after_reqs_button")

    def request_blanket_tissues(self):
        self._ensure_phone_modal_closed()
        self._ensure_requirements_menu_open()
        slider = self.wait.until(EC.element_to_be_clickable(self.blanket_tissues_slider), message="No se encontró el slider de mantas/pañuelos")
        try:
            actions = ActionChains(self.driver)
            initial_position = slider.location['x']
            actions.drag_and_drop_by_offset(slider, 50, 0).perform()
            time.sleep(1)
            if slider.location['x'] <= initial_position:
                raise Exception("El slider no se movió")
        except Exception:
            for _ in range(3):
                try:
                    slider.click()
                    print("Clic realizado en el slider como alternativa.")
                    break
                except ElementClickInterceptedException:
                    time.sleep(1)
            self._take_screenshot("blanket_tissues_error")
        self._take_screenshot("after_blanket_tissues")

    def request_ice_creams(self, quantity=2):
        self._ensure_phone_modal_closed()
        self._ensure_requirements_menu_open()
        ice_cream_plus = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus), message="No se encontró el botón de agregar helados")
        for i in range(quantity):
            try:
                ice_cream_plus.click()
                print(f"Helado agregado, cantidad actual: {i + 1}")
                time.sleep(1)
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", ice_cream_plus)
                print(f"Helado agregado con JavaScript, cantidad actual: {i + 1}")
                self._take_screenshot(f"ice_cream_error_{i + 1}")
        self._take_screenshot("after_ice_creams")

    def request_taxi(self):
        self._ensure_phone_modal_closed()
        order_element = self._click_element(self.order_button, "botón de ordenar el taxi", "after_order_button_click")
        try:
            self.wait.until(EC.visibility_of_element_located(self.modal_search), message="No se encontró el modal 'order-header'")
            print("Modal 'order-header' encontrado.")
        except TimeoutException:
            print("Timeout esperando el modal 'order-header'.")
            self._take_screenshot("modal_search_timeout")
            with open("page_source_after_timeout.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print("Fuente de la página guardada como page_source_after_timeout.html")

    def validate_taxi_order(self):
        """Valida que el pedido de taxi se haya completado correctamente."""
        try:
            modal = self.wait.until(EC.visibility_of_element_located(self.modal_search), message="No se encontró el modal 'order-header'")
            order_status = modal.text.lower()
            if "buscar" in order_status or "buscar automovil" in order_status:
                print("Validación exitosa: El pedido de taxi está en proceso.")
                self._take_screenshot("order_validation_success")
                return True
            else:
                print(f"Validación fallida: Estado del pedido no esperado ({order_status}).")
                self._take_screenshot("order_validation_failed")
                return False
        except TimeoutException:
            print("Validación fallida: No se encontró el modal de confirmación del pedido.")
            self._take_screenshot("order_validation_timeout")
            return False