import json
import time
from selenium.common.exceptions import WebDriverException


def retrieve_phone_code(driver) -> str:
    """Devuelve el código de confirmación de teléfono como string."""
    time.sleep(5)
    for _ in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
                if code:
                    return code
        except WebDriverException:
            time.sleep(1)
            continue
    raise Exception("No se encontró el código de confirmación del teléfono.")
