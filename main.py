import logging
import sys
import time

from pathlib import Path
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ValidationError
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc  # type: ignore[import-untyped]


# Make a new class from uc.Chrome and redefine __del__ function to suppress exception
# https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/955
class Chrome(uc.Chrome):  # type: ignore[misc]
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def __del__(self) -> None:
        try:
            self.service.process.kill()
            self.quit()
        except:
            pass


logging.basicConfig(level=logging.INFO)


def non_empty_str(x: str) -> str:
    if len(x) == 0:
        raise ValidationError("Empty string passed")
    return x


NonEmptyString = Annotated[str, BeforeValidator(non_empty_str)]

CONFIG_FILE = Path("config.json")


class Config(BaseModel):
    username: NonEmptyString = ""
    password: NonEmptyString = ""


def main(config: Config) -> None:
    # Go to login page
    LOGIN_PAGE = "https://www.publix.com/login?redirectUrl=/savings/digital-coupons"
    driver = Chrome(headless=False)
    driver.get(LOGIN_PAGE)

    wait = WebDriverWait(driver, 30)
    shorter_wait = WebDriverWait(driver, 5)

    username_input = wait.until(EC.visibility_of_element_located((By.ID, "signInName")))
    username_input.send_keys(config.username)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(config.password)
    password_input.send_keys(Keys.ENTER)

    # Wait for 'page loaded' selector
    PAGE_LOADED_SELECTOR = 'button[data-qa-automation="back-to-top-button"]'
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PAGE_LOADED_SELECTOR)))
    logging.info("Page redirected!")

    # Load all buttons
    LOAD_MORE_BUTTON = 'button[data-qa-automation="button-Load more"]'
    while True:
        try:
            load_more = shorter_wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, LOAD_MORE_BUTTON))
            )
            driver.execute_script("arguments[0].scrollIntoView();", load_more)
        except TimeoutException:
            logging.info("Loaded all coupons")
            break

        load_more.click()

    # Click all the coupons
    CLIP_BUTTON = 'button[data-qa-automation="button-Clip coupon"]'
    for element in driver.find_elements(By.CSS_SELECTOR, CLIP_BUTTON):
        try:
            shorter_wait.until(EC.element_to_be_clickable(element))
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
        except TimeoutException:
            logging.warning("Failed to wait for a click!")

    # Idle a bit, then done!
    logging.info("Finished clicking all coupons, idling for a second")
    time.sleep(5)
    driver.quit()
    logging.info("See ya!")


if __name__ == "__main__":
    if not CONFIG_FILE.exists():
        logging.error(f"{CONFIG_FILE} not found, generating one")
        CONFIG_FILE.write_text(Config().model_dump_json(indent=2))
        sys.exit(1)

    config = Config.model_validate_json(CONFIG_FILE.read_text())
    main(config)
