# test_tripadvisor.py

import json
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

@pytest.fixture(scope="module")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.automation_name = "UiAutomator2"
    options.app_activity = "com.tripadvisor.android.ui.onboarding.OnboardingActivity"
    options.app_package = "com.tripadvisor.tripadvisor"
    options.no_reset = True
    options.new_command_timeout = 300

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()

def select_date_range(driver, wait, start_day, end_day):
    # Открытие выбора даты
    date_picker_trigger = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/txtDate")))
    date_picker_trigger.click()

    # Убедиться, что появился date picker
    wait.until(EC.visibility_of_element_located((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.LinearLayout").instance(1)'
    )))

    # Клик по дате начала
    start_day_el = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().text("{start_day}")'
    )))
    start_day_el.click()
    sleep(0.5)

    # Клик по дате окончания
    end_day_el = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().text("{end_day}")'
    )))
    end_day_el.click()
    sleep(0.5)

    # Клик по кнопке подтверждения
    confirm_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/btnPrimary")))
    confirm_btn.click()
    sleep(1)

def search_and_collect_prices(driver, wait, hotel_name, start_day, end_day, label):
    # Поле поиска
    search_box = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")))
    search_box.click()
    sleep(1)

    # Вводим название отеля
    search_input = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")))
    search_input.clear()
    search_input.send_keys(hotel_name)
    sleep(2)

    # Кликаем по первому результату
    first_result = wait.until(EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.tripadvisor.tripadvisor:id/typeaheadResult").instance(0)'
    )))
    first_result.click()
    sleep(2)

    # Выбираем диапазон дат
    select_date_range(driver, wait, start_day, end_day)

    # Сбор цен
    prices_elements = wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/txtPrice")))

    prices = {}
    for idx, el in enumerate(prices_elements):
        prices[f"provider_{idx+1}"] = el.text

    screenshot_name = f"{hotel_name.replace(' ', '_')}_{label}.png"
    driver.save_screenshot(screenshot_name)

    return {
        label: {
            "prices": prices,
            "screenshot": screenshot_name
        }
    }

def test_search_hotel_with_multiple_date_ranges(driver):
    wait = WebDriverWait(driver, 20)
    hotel_name = "The Grosvenor Hotel"

    date_ranges = [
        ("23", "24"),
        ("25", "26"),
        ("27", "28"),
        ("29", "30"),
    ]

    results = {hotel_name: {}}

    for start_day, end_day in date_ranges:
        label = f"2025-05-{start_day}_to_2025-05-{end_day}"
        result = search_and_collect_prices(driver, wait, hotel_name, start_day, end_day, label)
        results[hotel_name].update(result)

        driver.back()  # вернуться на главный экран
        sleep(2)

    with open("tripadvisor_prices_by_dates.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
