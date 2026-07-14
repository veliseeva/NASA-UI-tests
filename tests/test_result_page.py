import allure
from allure_commons.types import Severity

from NASA_ui_project.pages.search_page import search_page
from NASA_ui_project.pages.filters_component import filters
from NASA_ui_project.pages.result_page import result_page
from NASA_ui_project.pages.results_component import results


@allure.epic('Web-UI NASA')
@allure.feature('Functionality of the results page')
@allure.link('https://images.nasa.gov', name='NASA')
class ResultTest:

    @allure.title('Testing date slider functionality')
    @allure.story('Date sliders')
    @allure.tag('web')
    @allure.severity(Severity.CRITICAL)
    @allure.label('owner', 'eliseeva')
    def test_sliders(self):
        search_page.open()
        search_page.type_name_for_searching(search_name='Earth')
        filters.move_start_year_slider(steps_right=40)
        filters.move_end_year_slider(steps_left=56)
        filters.apply()
        result_page.should_have_url_parameters('1960', '1970')
        results.should_have_year_in_image_alt(item_index=1, regex_pattern=r'\b(196[0-9]|1970)\b')

    @allure.title('The download link is opening')
    @allure.story('Downloading link')
    @allure.tag('web')
    @allure.severity(Severity.CRITICAL)
    @allure.label('owner', 'eliseeva')
    def test_downloading_link(self):
        search_page.open()
        search_page.type_name_for_searching('Mars')
        result_page.click_video_result()
        result_page.check_download_link()

    @allure.title('Loading results via a direct link with parameters')
    @allure.story('Deep linking')
    @allure.tag('web')
    @allure.severity(Severity.CRITICAL)
    @allure.label('owner', 'eliseeva')
    def test_deep_linking(self):
        search_page.open('/search?q=Orion&page=2&media=image,video,audio&yearStart=1920&yearEnd=2026')
        results.should_have_pagination_text(text='Displaying page 2')
        results.should_have_header_text(text='Showing results for "Orion":')
