import time
import sys
from pathlib import Path
import json
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class CompanyManager:
  def __init__(self):
    self.url = 'https://www.ai-startups.se/'
    self.data_path = 'output/companies.json'
    self.companies = self.load_companies()

  def company_summary(self):
    n_companies = len(self.companies)

    summary = []
    companies = dict(
      sorted(self.companies.items(), key=lambda item: item[1]['first_seen']))

    for company_name, company in companies.items():
      summary.append(
        f"{company_name}: {company['website']}, First seen: {company['first_seen']}"
      )

    summary.append(f'Number of companies: {n_companies}')
    return '\n'.join(summary)

  def save_companies(self):
    with open(self.data_path, 'w') as f:
      json.dump(self.companies, f, indent=2)

  def load_companies(self):
    with open(self.data_path) as f:
      return json.load(f)

  def scrape_companies(self):
    driver_path = get_driver_path()
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    with webdriver.Chrome(driver_path, options=chrome_options) as driver:
      WebDriverWait(driver, timeout=5)
      driver.get(self.url)

      time.sleep(5)  # Wait for table to get populated

      companies = {}
      company_elements = driver.find_elements_by_class_name("table-responsive")
      companies_info = company_elements[0].text.splitlines()[1:]
      for company_info in companies_info:
        try:
          # print(company_info)
          company_name, website = company_info.split(' Sweden ')
          company_name = ' '.join(company_name.split()[1:])
          website = website.split()[0]
          companies[company_name] = dict(name=company_name, website=website)
        except Exception as e:
          print(f"Error: {company_info}", e)
      return companies

  def add_companies(self, companies):
    for company_name, company in companies.items():
      if company_name not in self.companies:
        first_seen = last_seen = datetime.now().date().isoformat()
        company['first_seen'] = first_seen
        company['last_seen'] = last_seen
        self.companies[company_name] = company
      else:
        last_seen = datetime.now().date().isoformat()
        self.companies[company_name]['last_seen'] = last_seen

  def get_location(self, company_name):
    company = self.companies[company_name]
    return company.get('location')

  def add_location(self, company_name, location):
    self.companies[company_name]['location'] = location
    self.save_companies()


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


if __name__ == '__main__':
  company_manager = CompanyManager()
  companies = company_manager.scrape_companies()
  company_manager.add_companies(companies)
  company_manager.save_companies()
  print(company_manager.company_summary())
