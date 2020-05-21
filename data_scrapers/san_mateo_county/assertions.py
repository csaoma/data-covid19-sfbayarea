class Assertions:
    """
    Class to encapsulate assertions.

    These are mostly designed to ensure the webpage hasn't changed and was loaded correctly.
    """
    def iframes_match(self, iframes) -> None:
        if len(iframes) != 5:
            raise FutureWarning('The number of dashboards on the start page has changed. It was 5.')

        if sum('https://app.powerbigov.us' in iframe['src'] for iframe in iframes) != 4:
            raise FutureWarning('iframes no longer recognized, check contents of page at START_URL.')

    def age_labels_are_present(self, chart) -> None:
        text = list(map(lambda title: title.get_attribute('innerHTML'), chart.find_elements_by_tag_name('title')))
        expected_text = ['0 to 19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
        if text != expected_text:
            raise FutureWarning('Did not find the age range labels on one of the charts.')

    def dates_match(self, cumulative_cases, daily_cases) -> None:
        if [day['date'] for day in cumulative_cases] != [day['date'] for day in daily_cases]:
            raise(FutureWarning('Cumulative and daily cases have inconsistent dates.'))
