import time
import sys
from pathlib import Path
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.ai-startups.se/'


def main():
  driver_path = get_driver_path()
  chrome_options = Options()
  chrome_options.add_argument("--headless")

  #This example requires Selenium WebDriver 3.13 or newer
  with webdriver.Chrome(driver_path, options=chrome_options) as driver:
    WebDriverWait(driver, timeout=5)
    driver.get(URL)

    time.sleep(1)  # Wait for table to get populated

    companies = {}
    company_elements = driver.find_elements_by_class_name("table-responsive")
    companies_info = company_elements[0].text.splitlines()[1:]
    for company_info in companies_info:
      print(company_info)
      # TODO: Crashes on some company names. I'm guessing not all companies are loaded every time
      company_name, website = company_info.split(' Sweden ')
      company_name = ' '.join(company_name.split()[1:])
      website = website.split()[0]
      companies[company_name] = dict(name=company_name, website=website)

    save_companies(companies)


def get_driver_path():
  platforms = dict(
    darwin='web_drivers/chromedriver_mac64',
    win32='web_drivers/chromedriver.exe',
  )
  if sys.platform in platforms:
    driver_path = Path(platforms[sys.platform]).resolve()
    assert driver_path.exists()
    return str(driver_path)

  raise RuntimeError(f'Unsupported platform: {sys.platform}')


def save_companies(companies):
  with open('output/companies.json', 'w') as f:
    json.dump(companies, f, indent=2)


if __name__ == '__main__':
  main()
