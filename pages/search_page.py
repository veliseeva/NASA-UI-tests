import allure
from selene import browser, have, be


class SearchPage:
    def open(self, path='/'):
        with allure.step('Открыть сайт.'):
            browser.open(path)

    def type_name_for_searching(self, search_name):
        with allure.step(f'Ввести в поиск значение "{search_name}".'):
            browser.element('#search-input').should(be.blank).type(search_name).press_enter()
            browser.should(have.url_containing(f'q={search_name}'))

    def checking_search_result(self, result):
        with allure.step(f'Проверить в поиске значение "{result}".'):
            browser.all('.container body-content').should(have.text(result))

    def checking_empty_search_result(self, no_results):
        with allure.step(f'Проверить, что результат пуст.'):
            browser.element('#search-noMatches').should(have.text(no_results))


search_page = SearchPage()
