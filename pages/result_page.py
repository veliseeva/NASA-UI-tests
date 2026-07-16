import allure
from selene import browser, have, command


class ResultPage:

    def should_have_url_parameters(self, *params):
        with allure.step('Проверить, что годы установлены верно.'):
            for param in params:
                browser.should(have.url_containing(param))

    def click_video_result(self):
        with allure.step('Кликнуть на видео-результат.'):
            browser.all('.video-asset').second.element('.play').perform(command.js.click)

    def check_download_link(self):
        with allure.step('Проверить, что ссылка для скачивания существует.'):
            browser.element('#video-large-dl a').should(
                have.attribute('href').value_containing('images-assets.nasa.gov/video'))


result_page = ResultPage()
