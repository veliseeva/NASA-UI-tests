import allure
from allure_commons.types import Severity

from NASA_ui_project.pages.search_page import search_page
from NASA_ui_project.pages.mobile_page import mobile_page


@allure.epic('Web-UI NASA')
@allure.feature('Mobile view functionality')
@allure.link('https://images.nasa.gov', name='NASA')
class TestResolution:

    @allure.title('Mobile menu functionality at mobile resolution')
    @allure.story('Mobile menu')
    @allure.tag('web')
    @allure.severity(Severity.CRITICAL)
    @allure.label('owner', 'eliseeva')
    def test_mobile_view(self, mobile_browser):
        search_page.open()
        search_page.type_name_for_searching(search_name='Mars')
        mobile_page.should_have_mobile_menu()
        mobile_page.should_have_mobile_menu()
