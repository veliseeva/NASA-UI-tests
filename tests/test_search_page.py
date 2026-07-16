import allure
from allure_commons.types import Severity

from pages.search_page import search_page
from pages.filters_component import filters
from pages.results_component import results


@allure.epic('Web-UI NASA')
@allure.feature('Search field')
@allure.link('https://images.nasa.gov', name='NASA')
class TestSearch:

    @allure.title('Find value through search')
    @allure.story('Search')
    @allure.tag('web')
    @allure.severity(Severity.CRITICAL)
    @allure.label('owner', 'eliseeva')
    def test_search_field(self):
        search_page.open()
        search_page.type_name_for_searching(search_name='Orion')
        search_page.checking_search_result(result='Results for "Orion"')

    @allure.title('Check for a non-existent value')
    @allure.story('Search non-existent')
    @allure.tag('web')
    @allure.severity(Severity.NORMAL)
    @allure.label('owner', 'eliseeva')
    def test_non_existent_request(self):
        search_page.open()
        search_page.type_name_for_searching(search_name='Nibiru')
        search_page.checking_empty_search_result(no_results='Based on your selections, no results were found.')

    @allure.title('Check the filter logic')
    @allure.story('Filter logic')
    @allure.tag('web')
    @allure.severity(Severity.CRITICAL)
    @allure.label('owner', 'eliseeva')
    def test_filter_logic(self):
        search_page.open()
        filters.uncheck_images()
        filters.uncheck_videos()
        search_page.type_name_for_searching(search_name='Apollo')
        results.should_have_only_audio()
