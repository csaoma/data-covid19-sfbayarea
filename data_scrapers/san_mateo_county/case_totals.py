from typing import Dict, List

from assertions import Assertions
from charts import Charts

class CaseTotals:
    """
    Gets case totals and death totals grouped by:
    - Age
    - Race
    - Gender
    """
    def __init__(self, charts) -> None:
        self.charts = charts
        self.assertions = Assertions()


    def extract_data(self) -> Dict:
        return {
            'case_totals': {
                'age_group': self.__parse_case_data()
            },
            'death_totals': {
                'age_group': self.__parse_death_data()
            }
        }

    def __parse_case_data(self) -> Dict[str, int]:
        case_data_chart = self.charts[Charts.CASE_DATA]
        self.assertions.age_labels_are_present(case_data_chart)

        return dict(self.__extract_numbers(case_data_chart))

    def __parse_death_data(self) -> Dict[str, int]:
        death_data_chart = self.charts[Charts.DEATH_DATA]
        self.assertions.age_labels_are_present(death_data_chart)

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
