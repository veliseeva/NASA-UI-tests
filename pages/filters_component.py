import allure
from selene import browser, command
from selenium.webdriver.common.keys import Keys


class FiltersComponent:
    def uncheck_images(self):
        with allure.step('Снять галку с чекбокса изображений.'):
            browser.all('.mdc-checkbox__native-control').first.click()

    def uncheck_videos(self):
        with allure.step('Снять галку с чекбокса видео.'):
            browser.all('.mdc-checkbox__native-control').second.click()

    def move_start_year_slider(self, steps_right):
        with allure.step('Передвинуть первый слайдер с датой.'):
            browser.element('.ngx-slider-pointer-min').click().send_keys(Keys.ARROW_RIGHT * steps_right)

    def move_end_year_slider(self, steps_left):
        with allure.step('Передвинуть второй слайдер с датой.'):
            browser.element('.ngx-slider-pointer-max').click().send_keys(Keys.ARROW_LEFT * steps_left)

    def apply(self):
        with allure.step('Проверить, что годы установлены верно.'):
            browser.element('button:has(.desktop-label)').perform(command.js.click)


filters = FiltersComponent()
