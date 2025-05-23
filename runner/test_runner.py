# test_runner.py

import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def run_price_scraper(hotel_name: str, date_ranges: list[tuple[str, str]]):
    logger.info(f"Starting test for hotel: {hotel_name}")
    driver = get_driver()
    results = {hotel_name: {}}

    try:
        for start_date, end_date in date_ranges:
            logger.info(f"Testing date range: {start_date} to {end_date}")
            screenshot_name = f"{hotel_name.replace(' ', '_')}_{start_date}_{end_date}.png"
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)

            # TODO: Add Appium or Selenium interaction here to:
            # - Search hotel
            # - Select dates
            # - Scrape prices
            # - Save screenshot
            driver.save_screenshot(screenshot_path)

            results[hotel_name][f"{start_date}-{end_date}"] = {
                "prices": {"example_provider": "$100"},
                "screenshot": screenshot_name
            }

    finally:
        driver.quit()

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results
