import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

class SanMateoCounty:
    """
    San Mateo Data Scraper

    Starts on a page with multiple dashboards, progresses to a single dashboard
    using BeautifulSoup, then uses Selenium to read the page.

    Currently gets data by age group.

    TODO: There is a second dashboard with testing data.
    TODO: There is gender data on this dashboard.
    TODO: There is ethnicity data on this dashboard.
    TODO: There is timeseries data on this dashboard.
    """
    LANDING_PAGE = 'https://www.smchealth.org/post/san-mateo-county-covid-19-data-1'

    def __init__(self) -> None:
        with open('./data_models/data_model.json') as template_json:
            self.output = json.load(template_json)
        self.output['name'] = 'San Mateo County'
        self.output['source_url'] = self.LANDING_PAGE


    def get_county(self) -> Dict:
        soup = self.__get_landing_page()
        iframes = soup('iframe')
        self.__assert_iframes_match(iframes)

        cases_dashboard_url = iframes[0]['src']
        charts = self.__get_charts_with_selenium(cases_dashboard_url)
        self.output['case_totals']['age_group'] = self.__parse_case_data(charts)
        self.output['death_totals']['age_group'] = self.__parse_death_data(charts)
        return self.output

    def __get_landing_page(self) -> BeautifulSoup:
        response = requests.get(self.LANDING_PAGE)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html5lib')

    def __assert_iframes_match(self, iframes) -> None:
        if len(iframes) != 5:
            raise FutureWarning('The number of dashboards on the start page has changed. It was 5.')

        if sum('https://app.powerbigov.us' in iframe['src'] for iframe in iframes) != 4:
            raise FutureWarning('iframes no longer recognized, check contents of page at START_URL.')

    def __get_charts_with_selenium(self, url) -> List[webdriver.firefox.webelement.FirefoxWebElement]:
        driver = webdriver.Firefox()
        driver.get(url)
        WebDriverWait(driver, 30).until(
            expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, 'setFocusRing'), '0 to 19')
        )
        sleep(1)

        charts = driver.find_elements_by_class_name('svgScrollable')
        if len(charts) != 7:
            raise FutureWarning('This page has changed. There were previously seven bar charts.')

        return charts

    def __parse_case_data(self, charts) -> Dict[str, int]:
        case_data_chart = charts[0]
        self.__assert_age_labels_are_present(case_data_chart)

        return dict(self.__extract_numbers(case_data_chart))

    def __parse_death_data(self, charts) -> Dict[str, int]:
        death_data_chart = charts[4]
        self.__assert_age_labels_are_present(death_data_chart)

        return { f'Death_{label}': number for label, number in self.__extract_numbers(death_data_chart) }

    def __extract_numbers(self, chart) -> List[int]:
        data = list(map(lambda age_range: int(age_range.text), chart.find_elements_by_class_name('label')))
        if len(data) != 9:
            raise FutureWarning(f'Expected nine age ranges, but received {len(data)}.')

        return zip(self.__age_group_labels(), data)

    def __age_group_labels(self) -> List[str]:
        return [
            'Age_LT20',
            'Age_20_29',
            'Age_30_39',
            'Age_40_49',
            'Age_50_59',
            'Age_60_69',
            'Age_70_79',
            'Age_80_89',
            'Age_90_Up',
        ]


    def __assert_age_labels_are_present(self, chart) -> None:
        text = list(map(lambda title: title.get_attribute('innerHTML'), chart.find_elements_by_tag_name('title')))
        expected_text = ['0 to 19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
        if text != expected_text:
            raise FutureWarning('Did not find the age range labels on one of the charts.')


if __name__ == '__main__':
    """ When run as a script, prints the data to stdout"""
    print(json.dumps(SanMateoCounty().get_county(), indent=4))
