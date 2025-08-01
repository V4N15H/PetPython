import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    service.page_load_strategy = "eager"
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def wait_and_click(wait, by, locator, driver=None, use_js=False):
    try:
        element = wait.until(EC.element_to_be_clickable((by, locator)))
        if use_js and driver:
            driver.execute_script("arguments[0].click();", element)
        else:
            element.click()
        return element
    except Exception as e:
        print(f"Ошибка при клике по элементу: {locator}. {str(e)}")
        return None


def set_search_options(driver, wait):
    print("Устанавливаем параметры поиска...")
    try:
        # Указываем тип квартиры
        wait_and_click(
            wait,
            By.XPATH,
            "//span[text()='Студия']",
            driver,
            use_js=True,
        )
        # Вводим максимальную цену
        price_input = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@data-marker='price-to/input']")
            )
        )
        price_input.send_keys("20 000")
        # Применяем фильтры
        wait_and_click(
            wait,
            By.XPATH,
            "//button[@data-marker='search-filters/submit-button']",
            driver,
            use_js=True,
        )
        # Сортируем самые актуальные предложения
        wait_and_click(
            wait,
            By.XPATH,
            "//span[@data-marker='sort/title']",
            driver,
            use_js=True,
        )
        wait_and_click(
            wait,
            By.XPATH,
            "//div[text()='По дате']",
            driver,
            use_js=True,
        )
        print("Параметры поиска заданы")
    except Exception as e:
        print(f"Не удалось установить параметры поиска: {str(e)}")


def get_links(driver):
    try:
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        # собираем ссылки с карточек
        all_publications = soup.find_all("a", {"data-marker": "item-title"})[:10]
        # форматируем результат
        for article in all_publications:
            print(article["href"])
    except Exception:
        print(f"Ошибка при обработке ссылки {article}")


def main():
    driver = setup_driver()
    driver.delete_all_cookies()
    driver.get("chrome://settings/clearBrowserData")
    wait = WebDriverWait(driver, 10)
    try:
        print("Идет подготовка сайта...")
        driver.get(
            "https://www.avito.ru/izhevsk/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?context=H4sIAAAAAAAA_wEtANL_YToxOntzOjg6ImZyb21QYWdlIjtzOjE2OiJzZWFyY2hGb3JtV2lkZ2V0Ijt9F_yIfi0AAAA"
        )
        set_search_options(driver, wait)
        get_links(driver)

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
