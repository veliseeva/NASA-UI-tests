import allure
import re
from selene import browser, be, query, have


class ResultsComponent:
    def __init__(self):
        self.container = browser.element('#search-results_container')

    def should_have_only_audio(self):
        with allure.step('Проверить, что активен только аудио чекбокс.'):
            self.container.element('.audio-asset').should(be.existing)
            self.container.element('.video-asset').should(be.absent)
            self.container.element('.image-asset').should(be.absent)

    def should_have_year_in_image_alt(self, item_index, regex_pattern):
        with allure.step('Проверить, что год виден в alt.'):
            img_element = browser.all('.image-asset')[item_index].element('img').should(be.visible)
            alt_text = img_element.get(query.attribute('alt'))
            year_pattern = re.search(regex_pattern, alt_text)

            assert year_pattern, f"ОШИБКА: Год не найден в alt! Текст: '{alt_text}'"

    def should_have_pagination_text(self, text):
        with allure.step('Проверить работу пагинации.'):
            browser.element('#results-returned_page span').should(have.text(text))

    def should_have_header_text(self, text):
        with allure.step('Проверить отображение результатов.'):
            browser.element('#results-returned h2').should(have.text(text))


results = ResultsComponent()
