import allure
from selene import browser, be, by


class MobilePage:

    def convert_to_mobile_size(self):
        with allure.step('Открыть мобильное разрешение.'):
            browser.driver.set_window_size(430, 932)

    def should_have_mobile_menu(self):
        with allure.step('Проверить отображение мобильного меню.'):
            browser.element('#mobile-menu').should(be.existing)

    def should_have_mobile_filter_button(self):
        with allure.step('Проверить отображение мобильных фильтров.'):
            browser.element(by.text('Filter Search Results')).should(be.existing)


mobile_page = MobilePage()
